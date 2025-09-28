from mythica.core import BaseEcosystem
from mythica.utils import EcosystemIO
import time
import random

if __name__ == "__main__":
    from mythica.catalog import ABILITIES
    from mythica.catalog import CREATURES

    ### ABILITIES ##
    fire_ball = ABILITIES["fire_ball"]
    extreme_speed = ABILITIES["extreme_speed"]
    tsunami = ABILITIES["tsunami"]
    tackle = ABILITIES["tackle"]

    ### CREATURES ###
    creature_1 = CREATURES["dinosaur"]
    creature_2 = CREATURES["bird"]
    creature_3 = CREATURES["alien"]
    creature_4 = CREATURES["robot"]
    creature_5 = CREATURES["human"]
    creature_6 = CREATURES["dog"]

    creature_1.add_abilities([fire_ball,tackle])
    creature_2.add_abilities([extreme_speed,tackle])
    creature_3.add_abilities([tsunami,tackle])
    creature_4.add_abilities([fire_ball,tackle])
    creature_5.add_abilities([tsunami,tackle])
    creature_6.add_abilities([extreme_speed,tackle])

    ## ECOSYSTEM ##
    logger = EcosystemIO()

    ecosystem = BaseEcosystem(
        name = "Pantano Xeno",
        seed = 1998,
        creatures = [
            creature_1,
            creature_2,
            creature_3,
            creature_4,
            creature_5,
            creature_6
        ],
        logger = logger
    )

    start = time.perf_counter()

    ecosystem.simulate_season(
        seasons = 1000,
        turns_for_season = 5
    )

    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - start:.6f} segundos")

    for message in logger.get_log():
        print(message)