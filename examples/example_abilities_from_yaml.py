from mythica.core import BaseEcosystem
from mythica.utils import EcosystemIO, load_abilities_from_yaml
import time

if __name__ == "__main__":
    from mythica.catalog import CREATURES
    from mythica.core.context import ContextAbility

    ABILITIES = load_abilities_from_yaml("./examples/abilities.yaml")

    ### ABILITIES ##
    fire_ball = ABILITIES["fire_ball"]
    extreme_speed = ABILITIES["extreme_speed"]
    tsunami = ABILITIES["tsunami"]
    tackle = ABILITIES["tackle"]

    ### CREATURES ###
    creature_1 = CREATURES["dinosaur"]
    creature_2 = CREATURES["bird"]
    creature_3 = CREATURES["alien"]

    creature_1.add_abilities([fire_ball,tackle])
    creature_2.add_abilities([extreme_speed,tackle])
    creature_3.add_abilities([tsunami,tackle])

    # context = ContextAbility(
    #     user = creature_1,
    #     target = creature_2,
    #     alive_creatures = [
    #         creature_1,
    #         creature_2,
    #         creature_3
    #     ]
    # )

    # print(creature_1)
    # print(creature_2)
    # print("-------------")

    # print(fire_ball.effect(context))

    # print("--------------")
    # print(creature_1)
    # print(creature_2)


    ## ECOSYSTEM ##
    logger = EcosystemIO()

    ecosystem = BaseEcosystem(
        name = "Pantano Xeno",
        seed = 1998,
        creatures = [
            creature_1,
            creature_2,
            creature_3,
            creature_1,
            creature_2,
            creature_3
        ],
        logger = logger
    )

    start = time.perf_counter()

    ecosystem.simulate_simple_battle(50000)

    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.6f} segundos")

    for message in logger.get_log():
        print(message)