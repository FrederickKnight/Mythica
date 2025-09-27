from typing import Literal, Union
from mythica.core import BaseAbility
from mythica.core.context import ContextAbility
from mythica.schema import AbilityCategoryEnum
from mythica.catalog import EFFECTS

ABILITIES: dict[str,BaseAbility] = {}

AbilityCategories = Union[AbilityCategoryEnum,Literal["attack","defense"]]

def register_ability(name:str,category:AbilityCategories,cost:int,effect:dict[str, (ContextAbility)]):
    if name in ABILITIES:
        raise ValueError(f"Ability {name} already exist.")
    ability = BaseAbility(
        name = name,
        category = category,
        cost = cost,
        effect = effect
    )
    if ability:
        ABILITIES[name] = ability
    
    return ability

register_ability(
    name = "fire_ball",
    category = "attack",
    cost = 20,
    effect = EFFECTS["fire_ball"]
)

register_ability(
    name = "extreme_speed",
    category = "attack",
    cost = 20,
    effect = EFFECTS["extreme_speed"]
)

register_ability(
    name = "tsunami",
    category = AbilityCategoryEnum.ATTACK,
    cost = 30,
    effect = EFFECTS["tsunami"]
)

register_ability(
    name = "tackle",
    category = AbilityCategoryEnum.ATTACK,
    cost = 1,
    effect = EFFECTS["tackle"]
)