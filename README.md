# Mythica

**Mythica**: is a library to create and simulate fantasy-like ecosystems.
Allows creatures to interact in turn-based seasons or battles.
These creatures can mutate, breed or kill eachother.

## Caracteristics

- **Creatures**: Has Genes that decide its stats and abilities to use in an "act".
- **Abilities**: Actions that can be a simple tackle or even summon a tsunami, it depends on effect and the context.
- **Ecosystems**: A "world" where the creatures can coexist or not
- **Logger**: Registry of the turns and actions of the creature in an ecosystem.

- **Load of Abilities**: Can be created from a class or a yaml file.
- **Catalog**: Predefined examples of "Abilities", "Effects" and "Creatures"

## Example

```python
from mythica.core import BaseEcosystem

from mythica.catalog import ABILITIES, CREATURES

fire_ball = ABILITIES["fire_ball"]
extreme_speed = ABILITIES["extreme_speed"]
tsunami = ABILITIES["tsunami"]
tackle = ABILITIES["tackle"]

creature_1 = CREATURES["dinosaur"]
creature_2 = CREATURES["bird"]
creature_3 = CREATURES["alien"]

ecosystem = BaseEcosystem(
    name = "Example Eco",
    seed = 2025,
    creatures = [
        creature_1,
        creature_2,
        creature_3
    ]
)

ecosystem.simulate_season(
    seasons = 10,
    turns_for_season = 5
)

for message in ecosystem.logger.get_log():
    print(message)
```