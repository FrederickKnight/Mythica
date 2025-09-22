import pytest
from mythica.core import BaseCreature

json_creature = {
    "name" : "Dinosaurio",
    "health" : 50,
    "velocity" : 10,
    "energy" : 100
}

def test_creature_create():
    """
    Test for the correct creation of a Creature.

    Verifies:
        - 'name', 'health', 'velocity' and 'energy' are asigned correctly to the class 'BaseCreature'.
    """

    creature = BaseCreature(**json_creature)

    assert creature.name == json_creature["name"], f"Name should be {json_creature['name']} not {creature.name}"
    assert creature.health == json_creature["health"], f"Health should be {json_creature['health']} not {creature.health}"
    assert creature.velocity == json_creature["velocity"], f"Velocity should be {json_creature['velocity']} not {creature.velocity}" 
    assert creature.energy == json_creature["energy"], f"Energy should be {json_creature['energy']} not {creature.energy}"

def test_creature_take_damage():
    """
    Test the method 'take_damage' of the class 'BaseCreature'.

    Verifies:
        - Damage is taken correctly from the health of the creature.
        - Health is not negative if the damage exceeds the health.
    """
    creature = BaseCreature(**json_creature)

    damage_taken = 40
    calculated_damage = max(0,json_creature["health"] - damage_taken)

    creature.take_damage(
        quantity = damage_taken
    )

    assert creature.health == calculated_damage, f"Health should be {calculated_damage}, not {creature.health}"

    creature.take_damage(
        quantity = creature.health + 1
    )

    assert creature.health == 0, f"Health should be 0 if taken more damage than health, not {creature.health}"

def test_creature_use_energy():
    creature = BaseCreature(**json_creature)

    energy_used = 30
    calculated_energy = max(0,json_creature["energy"] - energy_used)

    creature.use_energy(
        quantity = energy_used
    )

    assert creature.energy == calculated_energy, f"Energy should be {calculated_energy}, not {creature.energy}"

    creature.use_energy(
        quantity = creature.energy + 1
    )

    assert creature.energy == 0, f"Energy should be 0 if used more energy, not {creature.energy}"
