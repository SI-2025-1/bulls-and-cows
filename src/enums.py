from enum import Enum


class PlayerRole(Enum):
    CODE_MAKER = "N"
    CODE_BREAKER = "B"


class Perceptions(Enum):
    WHITE_PLAYER_PERCEPTION = "B"
    BLACK_PLAYER_PERCEPTION = "N"
    FIRST_GUESS_PERCEPTION = "L"
