import pytest
from mythica.core import BaseCreature,BaseAbility
from mythica.core.context import ContextAbility
from mythica.catalog import EFFECTS, ABILITIES
import numpy as np
import random

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

base_creature_2_health = 800
base_creature_2_energy = 1000
base_creature_2_velocity = 15

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

def test_creature_add_ability():
    """
    Test the method add_ability from Creature class.

    Verifies:
        - Ability is added correctly in the Creature.
    """
    ability_1 = BaseAbility(
        name = "Fire Ball",
        category = "attack",
        cost = 10,
        effect=EFFECTS["fire_ball"],
        objective = "single_target"
    )

    creature = BaseCreature(**json_creature_1)

    creature.add_ability(
        ability = ability_1
    )

    assert ability_1 in creature.abilities, f"Ability {ability_1} should be in creature abilities {creature.abilities}"

def test_creature_add_abilities():
    """
    Test the method add_abilities from Creature class.

    Verifies:
        - Abilities are added correctly in the Creature.
        - Abilities are not duplicated in the Craeture.
    """
    ability_1 = BaseAbility(
        name = "Fire Ball",
        category = "attack",
        cost = 10,
        effect = EFFECTS["fire_ball"],
        objective = "single_target"
    )

    ability_2 = BaseAbility(
        name = "Water Mountain",
        category = "defense",
        cost = 20,
        effect = EFFECTS["fire_ball"],
        objective = "single_target"
    )

    creature = BaseCreature(**json_creature_1)

    list_abilities = [ability_1,ability_2]

    creature.add_abilities(list_abilities)

    assert ability_1 in creature.abilities, f"Ability {ability_1} should be in creature abilities {creature.abilities}"
    assert ability_2 in creature.abilities, f"Ability {ability_2} should be in creature abilities {creature.abilities}"
    
    assert len(creature.abilities) == len(list_abilities), f"Abilities should not be more repeated, got {creature.abilities}"

def test_creature_non_duplicated_abilities():
    fire_ball = BaseAbility(
        name="fire ball",
        category="attack",
        cost=50,
        effect=EFFECTS["fire_ball"],
        objective = "single_target"
    )

    tackle = BaseAbility(
        name = "Tackle",
        category = "attack",
        cost = 5,
        effect = EFFECTS["tackle"],
        objective = "single_target"
    )

    creature_1 = BaseCreature(**json_creature_1)

    list_abilities = [fire_ball,tackle,tackle]

    creature_1.add_abilities(list_abilities)

    assert len(list_abilities) != len(creature_1.abilities),f"Abilities should not be repeated, got {[a.name for a in creature_1.abilities]}"

def test_creature_use_ability():
    fire_ball = BaseAbility(
        name="fire ball",
        category="attack",
        cost=50,
        effect=EFFECTS["fire_ball"],
        objective = "single_target"
    )

    tackle = BaseAbility(
        name = "Tackle",
        category = "attack",
        cost = 5,
        effect = EFFECTS["tackle"],
        objective = "single_target"
    )

    creature_1 = BaseCreature(**json_creature_1)

    creature_2 = BaseCreature(**json_creature_2)

    creature_1.add_ability(fire_ball)

    ability_context = ContextAbility(
        user = creature_1,
        target = creature_2,
    )

    base_energy = creature_1.energy

    creature_1.use_ability(fire_ball,ability_context)
    assert creature_1.energy != base_energy, f"Ability that is in the creature should be used, energy didn't decreased"

    new_energy = creature_1.energy
    creature_1.use_ability(tackle,ability_context)
    assert creature_1.energy == new_energy, f"Ability that isn't the creature, should not be used, energy decreased"

def test_creature_act():
    fire_ball = ABILITIES["fire_ball"]

    creature_1 = BaseCreature(**json_creature_1)

    creature_2 = BaseCreature(**json_creature_2)

    creature_1.add_ability(fire_ball)

    ability_context = ContextAbility(
        alive_creatures = [creature_1,creature_2]
    )

    base_energy = creature_1.energy

    result = creature_1.act(
        ability_context = ability_context,
        random = random.Random()
    )

    assert f"{creature_1.name} can't act" != result, f"Creature should be able to act, got {result}"
    assert creature_1.energy != base_energy, f"When act the energy should decrease, energy before : {base_energy} and energy after : {creature_1.energy}"