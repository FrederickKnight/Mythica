from mythica.core import BaseCreature, BaseAbility

CREATURES: dict[str,BaseCreature] = {}

def register_creature(name:str,health:float,velocity:float,energy:float):
    if name in CREATURES:
        raise ValueError(f"Creature {name} already exist.")
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