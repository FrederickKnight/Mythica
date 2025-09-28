import pytest
from mythica.core.context import ContextAbility
from mythica.core import BaseCreature, BaseEcosystem, BaseAbility
import numpy as np

base_creature_1_health = 50
base_creature_1_energy = 100
base_creature_1_velocity = 10

json_creature_1 = {
    "name" : "Dinosaurio",
    "genes": np.array([
        [
            base_creature_1_health,
            base_creature_1_energy,
            base_creature_1_velocity
        ]
    ],dtype=float)
}

base_creature_2_health = 200
base_creature_2_energy = 100
base_creature_2_velocity = 50

json_creature_2 = {
    "name" : "Alien",
    "genes": np.array([
        [
            base_creature_2_health,
            base_creature_2_energy,
            base_creature_2_velocity
        ]
    ],dtype=float)
}

base_creature_3_health = 800
base_creature_3_energy = 100
base_creature_3_velocity = 15

json_creature_3 = {
    "name" : "Alien",
    "genes": np.array([
        [
            base_creature_3_health,
            base_creature_3_energy,
            base_creature_3_velocity
        ]
    ],dtype=float)
}

creature_1 = BaseCreature(**json_creature_1)
creature_2 = BaseCreature(**json_creature_2)
creature_3 = BaseCreature(**json_creature_3)

message = "test message"

def effect_test_message(ctx:ContextAbility) -> str:
    return message

test_ability = BaseAbility(
    name = "test",
    cost = 0,
    category = "attack",
    effect = effect_test_message,
    objective = "single_target"
)

creature_1.add_ability(test_ability)

list_creatures = [creature_1,creature_2,creature_3]

json_ecosystem = {
    "name": "Pantano Xeno",
    "seed": 1998,
    "creatures": list_creatures
}

def test_ecosystem_create():
    ecosystem = BaseEcosystem(**json_ecosystem)

    assert ecosystem.name == json_ecosystem["name"], f"Name should be {json_ecosystem["name"]}, not {ecosystem.name}"
    assert ecosystem.seed == json_ecosystem["seed"], f"Seed should be {json_ecosystem["seed"]}, not {ecosystem.seed}"
    assert len(ecosystem.creatures) == len(list_creatures), f"Creatures should be the same lenght, not {len(ecosystem.creatures)}"

def test_ecosystem_simulate_simple_battle_turn():
        ecosystem = BaseEcosystem(**json_ecosystem)
        
        for turn in range(2):
            ecosystem.simulate_simple_battle_turn(turn)

        assert message in ecosystem.logger.get_log(), f"Message should be in the logger"