class InvalidPerceptionFormatError(Exception):
    def __init__(self, message: str = "Invalid perception format"):
        super().__init__(message)


class NoPossibleGuessError(Exception):
    def __init__(
        self, message: str = "There are no more possible guesses based on the feedback"
    ):
        super().__init__(message)


class UnexpectedPerceptionError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Unexpected perception: {message}")


class RoleAlreadyAssignedError(UnexpectedPerceptionError):
    def __init__(self, message: str = "Role is already assigned"):
        super().__init__(message)
