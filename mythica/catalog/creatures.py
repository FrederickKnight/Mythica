from mythica.core import BaseCreature, BaseAbility
from mythica.catalog import EFFECTS

CREATURES: dict[str,BaseCreature] = {}

def register_creature(name:str,health:float,velocity:float,energy:float):
    creature = BaseCreature(
        name = name,
        health = health,
        velocity = velocity,
        energy = energy
    )

    if creature:
        CREATURES[name] = creature

    return creature

register_creature(
    name = "dinosaur",
    health = 60,
    velocity = 10,
    energy = 100
)

register_creature(
    name = "bird",
    health = 20,
    velocity = 50,
    energy = 100
)

register_creature(
    name = "alien",
    health = 50,
    velocity = 15,
    energy = 100
)