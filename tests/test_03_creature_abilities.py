import pytest
from mythica.core import BaseCreature,BaseAbility
from mythica.core.context import ContextAbility
from mythica.catalog import (
    effect_fire_ball,
    effect_tackle
)

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
        effect=effect_fire_ball
    )

    creature = BaseCreature(
        name = "Dinosaurio",
        health = 50,
        velocity = 10,
        energy = 100
    )

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
        effect = effect_fire_ball
    )

    ability_2 = BaseAbility(
        name = "Water Mountain",
        category = "defense",
        cost = 20,
        effect = effect_fire_ball
    )

    creature = BaseCreature(
        name = "Dinosaurio",
        health = 50,
        velocity = 10,
        energy = 100
    )

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
        effect=effect_fire_ball
    )

    tackle = BaseAbility(
        name = "Tackle",
        category = "attack",
        cost = 5,
        effect = effect_tackle
    )

    creature_1 = BaseCreature(
        name = "Dinosaurio",
        health = 50,
        velocity = 10,
        energy = 100
    )

    list_abilities = [fire_ball,tackle,tackle]

    creature_1.add_abilities(list_abilities)

    assert len(list_abilities) != len(creature_1.abilities),f"Abilities should not be repeated, got {[a.name for a in creature_1.abilities]}"

def test_creature_use_ability():
    fire_ball = BaseAbility(
        name="fire ball",
        category="attack",
        cost=50,
        effect=effect_fire_ball
    )

    tackle = BaseAbility(
        name = "Tackle",
        category = "attack",
        cost = 5,
        effect = effect_tackle
    )

    creature_1 = BaseCreature(
        name = "Dinosaurio",
        health = 50,
        velocity = 10,
        energy = 1000
    )

    creature_2 = BaseCreature(
        name = "Alien",
        health = 800,
        velocity = 15,
        energy = 1000
    )

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
    fire_ball = BaseAbility(
        name="fire ball",
        category="attack",
        cost=50,
        effect=effect_fire_ball
    )

    creature_1 = BaseCreature(
        name = "Dinosaurio",
        health = 50,
        velocity = 10,
        energy = 1000
    )

    creature_2 = BaseCreature(
        name = "Alien",
        health = 800,
        velocity = 15,
        energy = 1000
    )

    creature_1.add_ability(fire_ball)

    ability_context = ContextAbility(
        alive_creatures = [creature_1,creature_2]
    )

    base_energy = creature_1.energy

    result = creature_1.act(
        ability_context = ability_context
    )

    assert f"{creature_1.name} can't act" != result, f"Creature should be able to act, got {result}"
    assert creature_1.energy != base_energy, f"When act the energy should decrease, energy before : {base_energy} and energy after : {creature_1.energy}"