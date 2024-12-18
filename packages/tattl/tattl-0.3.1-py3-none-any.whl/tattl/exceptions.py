class ValidationException(Exception):
    """Raised when the data given does not conform to the ``dataclass``.

    Indicates that the type of a field in the data differs from the type of the ``dataclass`` field
    with the same name.
    """

    pass
