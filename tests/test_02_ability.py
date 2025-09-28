import pytest
from mythica.core import BaseAbility, BaseCreature
from mythica.core.context import ContextAbility
from mythica.schema import AbilityCategoryEnum, AbilityObjectiveEnum
import numpy as np

damage_fire_ball = 20

def effect_fire_ball(ctx:ContextAbility) -> str:
    ctx.user.take_damage(damage_fire_ball)
    return f"Casted Fire Ball and damage the user with {damage_fire_ball} damage"

json_ability = {
    "name":"Fire Ball",
    "cost":10,
    "category":AbilityCategoryEnum.ATTACK,
    "effect": effect_fire_ball,
    "objective" : AbilityObjectiveEnum.SINGLE_TARGET
}

base_creature_health = 50
base_creature_energy = 100
base_creature_velocity = 10

json_creature = {
    "name" : "Dinosaurio",
    "genes": np.array([
        [
            base_creature_health,
            base_creature_energy,
            base_creature_velocity
        ]
    ],dtype=float)
}

def test_ability_create():
    """
    Test the creation of the Ability.

    Verifies:
        - 'name', 'cost' and 'category' are asigned correctly to the class BaseAbility

    """
    ability = BaseAbility(**json_ability)

    assert ability.name == json_ability["name"], f"Name should be {json_ability["name"]},not {ability.name}"
    assert ability.cost == json_ability["cost"], f"Cost should be {json_ability["cost"]},not {ability.cost}"
    assert ability.category == json_ability["category"], f"Category should be {json_ability['category']}, not {ability.category}"

    creature = BaseCreature(**json_creature)

    calculated_health = max(0,base_creature_health - damage_fire_ball)

    context = ContextAbility(
        user = creature
    )

    ability.effect(context)

    assert creature.health == calculated_health, f"Health should be {calculated_health} from the taken damage of {damage_fire_ball} from fire ball, not {creature.health}"