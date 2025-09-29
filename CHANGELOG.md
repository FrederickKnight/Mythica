# Changelog

## [1.0.1]

### Added

- "BaseCreatures" : heal and rest methods.

### Changed

- "BaseCreature" : take_damage and use_energy now use absolute values to the quantity.

## [1.0.0] - 28-09-2025

### Added

#### Mythica Core

- "BaseCreatures" : Class to create a fantasy-like creature with "abilities" (or not), and stats/genes.

- "BaseAbility" : Class to create "abilities" which can be simple or complicated using the "ContextAbility".

- "ContextAbility" : Class to provide context to the "abilities", like the user of the ability, the target, or even targets for mass/area "abilities".

- "BaseEcosystem": Class to create an "ecosystem" where the creatures will live, simulating turns in a battle.

#### Mythica Utils

- "EcosystemIO" : Class that is created or provided to the "ecosystem", as a log for the simulation.
- "load_abilities_from_yaml" to create an "ability"

#### Mythica Catalog

- A catalog of functions that are used (as a predefined example) as "effects", "creatures" and "abilties"