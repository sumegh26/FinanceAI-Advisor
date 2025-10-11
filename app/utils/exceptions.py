class ValidationError(Exception):
    """
    Custom exception to be raised when input validation fails.
    Carries a message and optional list of error details.
    """
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.message = message
        self.errors = errors if errors else []

    def to_dict(self):
        return {
            "error": self.message,
            "details": self.errors
        }
