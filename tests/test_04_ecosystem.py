import pytest
from mythica.core.context import ContextAbility
from mythica.core import BaseCreature, BaseEcosystem, BaseAbility

creature_1 = BaseCreature(
    name = "Dinosaurio",
    health = 500,
    velocity = 10,
    energy = 100
)

creature_2 = BaseCreature(
    name = "Pajaro",
    health = 200,
    velocity = 50,
    energy = 100
)

creature_3 = BaseCreature(
    name = "Alien",
    health = 800,
    velocity = 15,
    energy = 100
)

message = "test message"

def effect_test_message(ctx:ContextAbility) -> str:
    return message

test_ability = BaseAbility(
    name = "test",
    cost = 0,
    category = "attack",
    effect = effect_test_message
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
            ecosystem.simulate_simple_battle_turn(
                 ability_context = ContextAbility(
                      alive_creatures = [
                           creature_1,
                           creature_2,
                           creature_3
                      ]
                 ),
                 turn = turn
            )

        assert message in ecosystem.logger.get_log(), f"Message should be in the logger"