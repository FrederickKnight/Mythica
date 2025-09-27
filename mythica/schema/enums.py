from enum import StrEnum, IntEnum

class AbilityCategoryEnum(StrEnum):
    DEFENSE = "defense"
    ATTACK = "attack"

class GeneEnum(IntEnum):
    MAX_VALUES = 0
    CURRENT_VALUES = 1

class GeneTypeEnum(IntEnum):
    HEALTH = 0
    ENERGY = 1
    VELOCITY = 2