from mythica.core import BaseAbility, BaseCreature, BaseEcosystem
from mythica.schema import AbilityCategoryEnum
from mythica.utils import EcosystemIO

if __name__ == "__main__":
    from mythica.core.context import ContextAbility
    from mythica.catalog import (
        effect_extreme_speed,
        effect_fire_ball,
        effect_tackle,
        effect_tsunami,
        effect_testicular_torsion
    )

    ### ABILITIES ##
    fire_ball = BaseAbility(
        name="fire ball",
        category=AbilityCategoryEnum.ATTACK,
        cost=20,
        effect=effect_fire_ball
    )

    testicular_torsion = BaseAbility(
        name="testicular torcion",
        category=AbilityCategoryEnum.ATTACK,
        cost=10,
        effect=effect_testicular_torsion
    )

    extreme_speed = BaseAbility(
        name = "Extreme Speed",
        category = AbilityCategoryEnum.ATTACK,
        cost = 20,
        effect = effect_extreme_speed
    )

    tsunami = BaseAbility(
        name = "Tsunami",
        category = AbilityCategoryEnum.ATTACK,
        cost = 30,
        effect = effect_tsunami
    )

    tackle = BaseAbility(
        name = "Tackle",
        category = AbilityCategoryEnum.ATTACK,
        cost = 1,
        effect = effect_tackle
    )

    ### CREATURES ###
    creature_1 = BaseCreature(
        name = "Dinosaurio",
        health = 500,
        velocity = 10,
        energy = 100
    )

    creature_1.add_abilities([fire_ball,tackle,testicular_torsion])

    creature_2 = BaseCreature(
        name = "Pajaro",
        health = 200,
        velocity = 50,
        energy = 100
    )
    creature_2.add_abilities([extreme_speed,tackle])

    creature_3 = BaseCreature(
        name = "Alien",
        health = 800,
        velocity = 15,
        energy = 100
    )

    creature_3.add_abilities([tsunami,tackle])


    ## ECOSYSTEM ##
    logger = EcosystemIO()

    ecosystem = BaseEcosystem(
        name = "Pantano Xeno",
        seed = 1998,
        creatures = [
            creature_1,
            creature_2,
            creature_3
        ],
        logger = logger
    )

    for turn in range(5):
        logger.log(f"-------Turn {turn + 1}------------")
        ecosystem.simulate_simple_battle_turn()

    for message in logger.get_log():
        print(message)