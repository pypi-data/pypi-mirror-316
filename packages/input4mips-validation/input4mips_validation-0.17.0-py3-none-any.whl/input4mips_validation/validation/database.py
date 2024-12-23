"""
Database validation
"""

from __future__ import annotations

import concurrent.futures
from pathlib import Path
from typing import Any, Optional, Union

import tqdm
from attrs import define, evolve
from loguru import logger

import input4mips_validation.logging_config
from input4mips_validation.cvs import Input4MIPsCVs, load_cvs
from input4mips_validation.database.database import Input4MIPsDatabaseEntryFile
from input4mips_validation.exceptions import NonUniqueError
from input4mips_validation.hashing import get_file_hash_sha256
from input4mips_validation.inference.from_data import BoundsInfo, FrequencyMetadataKeys
from input4mips_validation.logging import (
    LOG_LEVEL_INFO_DB_ENTRY,
    LOG_LEVEL_INFO_DB_ENTRY_ERROR,
    setup_logging,
)
from input4mips_validation.logging_config import (
    LoggingConfigSerialisedType,
    deserialise_logging_config,
    serialise_logging_config,
)
from input4mips_validation.validation.error_catching import (
    ValidationResultsStore,
)
from input4mips_validation.validation.file import (
    get_validate_file_result,
)
from input4mips_validation.xarray_helpers.variables import (
    XRVariableHelper,
    XRVariableProcessorLike,
)


def validate_tracking_ids_are_unique(
    db: tuple[Input4MIPsDatabaseEntryFile, ...],
) -> None:
    """
    Validate that the tracking IDs in the database are unique

    Parameters
    ----------
    db
        Database to validate

    Raises
    ------
    NonUniqueError
        The tracking IDs in the database are not unique
    """
    tracking_ids = [e.tracking_id for e in db]
    if len(set(tracking_ids)) != len(db):
        raise NonUniqueError(
            description="Tracking IDs for all entries should be unique",
            values=tracking_ids,
        )


def get_validate_database_file_entry_result(  # noqa: PLR0913
    entry: Input4MIPsDatabaseEntryFile,
    cv_source: str | None = None,
    cvs: Input4MIPsCVs | None = None,
    xr_variable_processor: XRVariableProcessorLike = XRVariableHelper(),
    frequency_metadata_keys: FrequencyMetadataKeys = FrequencyMetadataKeys(),
    bounds_info: BoundsInfo | None = None,
    time_dimension: str = "time",
    allow_cf_checker_warnings: bool = False,
    vrs: Union[ValidationResultsStore, None] = None,
) -> ValidationResultsStore:
    """
    Get the result of validating an entry for a file in our database

    Parameters
    ----------
    entry
        Entry to validate

    cv_source
        Source from which to load the CVs

        Only required if `cvs` is `None`.

        For full details on options for loading CVs,
        see
        [`get_raw_cvs_loader`][input4mips_validation.cvs.loading_raw.get_raw_cvs_loader].

    cvs
        CVs to use when validating the file.

        If these are passed, then `cv_source` is ignored.

    xr_variable_processor
        Helper to use for processing the variables in xarray objects.

    frequency_metadata_keys
        Metadata definitions for frequency information

    bounds_info
        Metadata definitions for bounds handling

        If `None`, this will be inferred from the file.

    time_dimension
        The time dimension of the data

    allow_cf_checker_warnings
        Should warnings from the CF-checker be allowed?

        In otherwise, is a file allowed to pass validation,
        even if there are warnings from the CF-checker?

    vrs
        The validation results store to use for the validation.

        If not supplied, we instantiate a new
        [`ValidationResultsStore`][input4mips_validation.validation.error_catching.ValidationResultsStore]
        instance.

    Returns
    -------
    :
        The validation results store.

    Raises
    ------
    ValueError
        The hash of the file does not match what is in the database.

        This is a pure raise (i.e. things will not fail gracefully).
        This is done in purpose.
        If the hash doesn't match what is expected, something is really wrong.
    """
    logger.log(
        LOG_LEVEL_INFO_DB_ENTRY.name, f"Checking the SHA for file: {entry.filepath}"
    )
    # Check the sha to start.
    # If this is wrong, let things explode because something is really wrong.
    sha256 = get_file_hash_sha256(Path(entry.filepath))
    if sha256 != entry.sha256:
        msg = (
            f"{entry.sha256=}, but we calculated a sha256 of {sha256} "
            f"for {entry.filepath}"
        )

        raise ValueError(msg)

    logger.log(
        LOG_LEVEL_INFO_DB_ENTRY.name,
        f"Creating validation results for the entry for file: {entry.filepath}",
    )

    if vrs is None:
        logger.debug("Instantiating a new `ValidationResultsStore`")
        vrs = ValidationResultsStore()

    if cvs is None:
        # Load CVs, we need them for the following steps
        cvs = vrs.wrap(
            load_cvs,
            func_description="Load controlled vocabularies to use during validation",
        )(cv_source=cv_source).result

    elif cv_source is not None:
        logger.warning(f"Using provided cvs instead of {cv_source=}")

    # Use validate individual file to check file loading and metadata
    vrs.wrap(get_validate_file_result, func_description="Validate individual file")(
        entry.filepath,
        cvs=cvs,
        xr_variable_processor=xr_variable_processor,
        frequency_metadata_keys=frequency_metadata_keys,
        bounds_info=bounds_info,
        time_dimension=time_dimension,
        allow_cf_checker_warnings=allow_cf_checker_warnings,
        vrs=vrs,
    )

    vrs.wrap(
        cvs.DRS.validate_file_written_according_to_drs,
        func_description="Validate file written according to the DRS",
    )(
        Path(entry.filepath),
        frequency_metadata_keys=frequency_metadata_keys,
        time_dimension=time_dimension,
    )

    # TODO: all references to external variables (like cell areas) can be resolved
    #       within the tree in which the file exists

    logger.log(
        LOG_LEVEL_INFO_DB_ENTRY.name,
        f"Created validation results for the entry for file: {entry.filepath}",
    )
    return vrs


@define
class FileEntryValidationResult:
    """
    Container for holding the results of database file entry validation
    """

    entry: Input4MIPsDatabaseEntryFile
    """The entry being validated"""

    passed_validation: bool
    """`True` if the entry passed validation, `False` otherwise"""

    exception_type: Optional[str] = None
    """If an exception was raised, its type"""

    exception_msg: Optional[str] = None
    """If an exception was raised, its message"""


def database_file_entry_is_valid(
    logging_config_serialised: LoggingConfigSerialisedType,
    entry: Input4MIPsDatabaseEntryFile,
    **kwargs: Any,
) -> FileEntryValidationResult:
    """
    Determine if a database entry for a file is valid

    This is really a helper to avoid the parallel processes
    exploding if we use
    [`get_validate_database_file_entry_result`][input4mips_validation.validation.database.get_validate_database_file_entry_result]
    directly.

    Parameters
    ----------
    logging_config_serialised
        Logging configuration to use (serialised version thereof)

    entry
        Entry to validate

    **kwargs
        Passed to
        [`get_validate_database_file_entry_result`][input4mips_validation.validation.database.get_validate_database_file_entry_result]

    Returns
    -------
    :
        Result of the validation of `entry`.
    """
    logging_config = deserialise_logging_config(logging_config_serialised)
    if logging_config is not None:
        setup_logging(
            enable=True,
            logging_config=logging_config,
        )

    vrs = get_validate_database_file_entry_result(entry=entry, **kwargs)
    try:
        vrs.raise_if_errors()
        res = FileEntryValidationResult(entry=entry, passed_validation=True)

    except Exception as exc:
        res = FileEntryValidationResult(
            entry=entry,
            passed_validation=False,
            exception_type=type(exc).__name__,
            exception_msg=str(exc),
        )

    return res


def validate_database_entries(  # noqa: PLR0913
    entries_to_validate: tuple[Input4MIPsDatabaseEntryFile, ...],
    cv_source: str | None = None,
    cvs: Input4MIPsCVs | None = None,
    xr_variable_processor: XRVariableProcessorLike = XRVariableHelper(),
    frequency_metadata_keys: FrequencyMetadataKeys = FrequencyMetadataKeys(),
    bounds_info: BoundsInfo | None = None,
    time_dimension: str = "time",
    allow_cf_checker_warnings: bool = False,
    n_processes: int = 1,
) -> tuple[Input4MIPsDatabaseEntryFile, ...]:
    """
    Validate entries for files in our database

    Parameters
    ----------
    entries_to_validate
        Entries to validate

    cv_source
        Source from which to load the CVs

        Only required if `cvs` is `None`.

        For full details on options for loading CVs,
        see
        [`get_raw_cvs_loader`][input4mips_validation.cvs.loading_raw.get_raw_cvs_loader].

    cvs
        CVs to use when validating the file.

        If these are passed, then `cv_source` is ignored.

    xr_variable_processor
        Helper to use for processing the variables in xarray objects.

    frequency_metadata_keys
        Metadata definitions for frequency information

    bounds_info
        Metadata definitions for bounds handling

        If `None`, this will be inferred on a per-file basis.

    time_dimension
        The time dimension of the data

    allow_cf_checker_warnings
        Should warnings from the CF-checker be allowed?

        In otherwise, is a file allowed to pass validation,
        even if there are warnings from the CF-checker?

    n_processes
        Number of parallel processes to use while validating the entries.

    Returns
    -------
    :
        `entries_to_validate`, updated based on whether they passsed validation or not
    """
    if cvs is None:
        # Load CVs, we need them for the following steps
        cvs = load_cvs(cv_source=cv_source)

    elif cv_source is not None:
        logger.warning(f"Using provided cvs instead of {cv_source=}")

    logging_config_serialised = serialise_logging_config(
        input4mips_validation.logging_config.LOGGING_CONFIG
    )
    logger.info(
        f"Validating {len(entries_to_validate)} database "
        f"{'entries' if len(entries_to_validate) > 1 else 'entry'} in parallel using "
        f"{n_processes} {'processes' if n_processes > 1 else 'process'}"
    )

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        futures = [
            executor.submit(
                database_file_entry_is_valid,
                logging_config_serialised,
                entry,
                cvs=cvs,
                xr_variable_processor=xr_variable_processor,
                frequency_metadata_keys=frequency_metadata_keys,
                bounds_info=bounds_info,
                time_dimension=time_dimension,
                allow_cf_checker_warnings=allow_cf_checker_warnings,
            )
            for entry in tqdm.tqdm(
                entries_to_validate, desc="Submitting entries to the queue"
            )
        ]

        out_l = []
        for future in tqdm.tqdm(
            concurrent.futures.as_completed(futures),
            desc="Database file entries",
            total=len(futures),
        ):
            file_validation_result = future.result()
            passed_validation = file_validation_result.passed_validation
            out_l.append(
                evolve(
                    file_validation_result.entry,
                    validated_input4mips=passed_validation,
                )
            )
            if passed_validation:
                logger.log(
                    LOG_LEVEL_INFO_DB_ENTRY.name,
                    "Validation passed for the entry pointing to "
                    f"{file_validation_result.entry.filepath}",
                )

            else:
                logger.log(
                    LOG_LEVEL_INFO_DB_ENTRY_ERROR.name,
                    f"Validation failed with {file_validation_result.exception_type=} "
                    "for the entry pointing to "
                    f"{file_validation_result.entry.filepath}",
                )
                logger.debug(
                    f"Validation failed with {file_validation_result.exception_type=} "
                    f"for {file_validation_result.entry.filepath}.\n"
                    f"Details: {file_validation_result.exception_msg}"
                )

    return tuple(out_l)
