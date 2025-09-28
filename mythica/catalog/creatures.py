from mythica.core import BaseCreature, BaseAbility
import numpy as np

CREATURES: dict[str,BaseCreature] = {}

def register_creature(name:str,genes:np.ndarray = None):
    if name in CREATURES:
        raise ValueError(f"Creature {name} already exist.")
    creature = BaseCreature(
        name = name,
        genes = genes
    )

    if creature:
        CREATURES[name] = creature

    return creature

register_creature(
    name = "dinosaur",
    genes = np.array([
        [500,100,10],
    ],dtype=float)
)

register_creature(
    name = "bird",
    genes = np.array([
        [120,100,50],
    ],dtype=float)
)

register_creature(
    name = "alien",
    genes = np.array([
        [300,100,15],
    ],dtype=float)
)

register_creature(
    name = "robot",
    genes = np.array([
        [380,200,8],
    ],dtype=float)
)

register_creature(
    name = "human",
    genes = np.array([
        [250,120,20],
    ],dtype=float)
)

register_creature(
    name = "dog",
    genes = np.array([
        [500,300,40],
    ],dtype=float)
)