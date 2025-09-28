from typing import Literal, Union
from mythica.core import BaseAbility
from mythica.core.context import ContextAbility
from mythica.schema import AbilityCategoryEnum,AbilityObjectiveEnum
from mythica.catalog import EFFECTS

ABILITIES: dict[str,BaseAbility] = {}

AbilityCategories = Union[AbilityCategoryEnum,Literal["attack","defense"]]
AbilityObjectives = Union[AbilityObjectiveEnum,Literal["all","all_except_user","single_target"]]

def register_ability(name:str,category:AbilityCategories,cost:int,effect:dict[str, (ContextAbility)],objective:AbilityObjectives):
    if name in ABILITIES:
        raise ValueError(f"Ability {name} already exist.")
    ability = BaseAbility(
        name = name,
        category = category,
        cost = cost,
        effect = effect,
        objective = objective
    )
    if ability:
        ABILITIES[name] = ability
    
    return ability

register_ability(
    name = "fire_ball",
    category = "attack",
    cost = 20,
    effect = EFFECTS["fire_ball"],
    objective = AbilityObjectiveEnum.SINGLE_TARGET
)

register_ability(
    name = "extreme_speed",
    category = "attack",
    cost = 20,
    effect = EFFECTS["extreme_speed"],
    objective = AbilityObjectiveEnum.SINGLE_TARGET
)

register_ability(
    name = "tsunami",
    category = AbilityCategoryEnum.ATTACK,
    cost = 30,
    effect = EFFECTS["tsunami"],
    objective = AbilityObjectiveEnum.ALL_EXCEPT_USER
)

register_ability(
    name = "tackle",
    category = AbilityCategoryEnum.ATTACK,
    cost = 1,
    effect = EFFECTS["tackle"],
    objective = AbilityObjectiveEnum.SINGLE_TARGET
)