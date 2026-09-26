class EnergyOSError(Exception):
    """A domain or application error that maps to an API response."""

    def __init__(self, *, code: str, message: str, status_code: int) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


class OrganizationNotFound(EnergyOSError):
    def __init__(self) -> None:
        super().__init__(
            code="organization_not_found",
            message="Organization not found",
            status_code=404,
        )


class AssessmentNotFound(EnergyOSError):
    def __init__(self) -> None:
        super().__init__(
            code="assessment_not_found",
            message="Assessment not found",
            status_code=404,
        )


class InvalidCursor(EnergyOSError):
    def __init__(self) -> None:
        super().__init__(
            code="invalid_cursor",
            message="Cursor is invalid",
            status_code=400,
        )


class DomainValidationError(EnergyOSError):
    def __init__(self, message: str) -> None:
        super().__init__(code="validation_error", message=message, status_code=422)


class ConfigurationError(EnergyOSError):
    def __init__(self, message: str) -> None:
        super().__init__(code="configuration_error", message=message, status_code=500)
