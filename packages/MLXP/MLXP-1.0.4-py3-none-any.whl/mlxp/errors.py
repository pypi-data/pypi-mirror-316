"""Errors raised by MLXP."""


class JobSubmissionError(Exception):
    """Raised when failed to submit a job using a scheduler."""

    pass


class InvalidKeyError(Exception):
    """Raised when the key is invalid."""

    pass


class MissingFieldError(Exception):
    """Raised when a Config_dict object is missing a required field."""

    pass


class InvalidArtifactError(Exception):
    """Raised when an object passed to the log_artifacts method of a Logger is not of
    type Artifact."""

    pass


class InvalidMapError(Exception):
    """Raised when a map is not an valid tuple of type Map."""

    pass


class InvalidShellPathError(Exception):
    """Raised when no shell path is specified."""

    pass


class UnknownSystemError(Exception):
    """Raised when system is different from Linux, Darwin or Windows."""

    pass


class InvalidSchedulerError(Exception):
    """Raised when system is different from Linux, Darwin or Windows."""

    pass


class InvalidConfigFileError(Exception):
    """Raised when the mlxp config file contains an invalid field."""

    pass
