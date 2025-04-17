class InvalidPerceptionFormatError(Exception):
    def __init__(self):
        super().__init__("Invalid perception format")


class NoPossibleGuessError(Exception):
    def __init__(self):
        super().__init__("There are no more possible guesses based on the feedback")


class UnexpectedPerceptionError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Unexpected perception: {message}")


class RoleAlreadyAssignedError(UnexpectedPerceptionError):
    def __init__(self):
        super().__init__("Role is already assigned")
