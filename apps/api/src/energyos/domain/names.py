from energyos.domain.errors import DomainValidationError

MAX_NAME_LENGTH = 200


def require_name(value: str, *, field: str = "Name") -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise DomainValidationError(f"{field} is required")
    if len(cleaned) > MAX_NAME_LENGTH:
        raise DomainValidationError(f"{field} must be at most {MAX_NAME_LENGTH} characters")
    return cleaned
