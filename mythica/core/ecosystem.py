from pydantic import BaseModel,Field,PrivateAttr,field_validator, model_validator
from typing import Self
import random
from mythica.core import BaseCreature, BaseAbility
from mythica.core.context import ContextAbility
from mythica.utils import EcosystemIO

class BaseEcosystem(BaseModel):
    name:str
    creatures:list[BaseCreature] = []
    seed:int = None
    logger:EcosystemIO = Field(default_factory=EcosystemIO)
    
    _random:random.Random = PrivateAttr(default_factory=None)

    @field_validator("seed",mode="before")
    @classmethod
    def validate_seed(cls,seed:int) -> int:
        if seed == None:
            return random.SystemRandom().randint(0, 2**32 - 1)
            
        if not isinstance(seed,int):
            raise TypeError(f"Expected int, got {type(seed).__name__}")
        
        if seed <= 0:
            raise ValueError("Seed must be a positive integer.")
        
        return seed
    
    @model_validator(mode="after")
    def build_ecosystem(self) -> Self:
        self._random = random.Random(self.seed)
        return self
    
    def simulate_simple_battle_turn(self) -> None:
        """
        Simulation where the creatures battle between them, using only it's abilities.
        """
        alive_creatures = [c for c in self.creatures if c.is_alive()]
        if not alive_creatures:
            return
        
        for creature in alive_creatures:
            if not creature.is_alive() or creature.energy <= 0:
                continue

            ability:BaseAbility = self._random.choice(creature.abilities) if creature.abilities else None

            posible_targets = [c for c in alive_creatures if c != creature]
            if not posible_targets:
                continue

            target = self._random.choice(posible_targets)

            ability_context = ContextAbility(
                user = creature,
                target = target,
                targets = posible_targets,
                all_creatures = alive_creatures
            )

            try:
                if ability:
                    ability_result = creature.use_ability(
                        ability = ability,
                        ctx = ability_context
                    )
                    self.logger.log(ability_result)
                else:
                    self.logger.log(f"{creature.name} has no ability to use")

            except Exception as e:
                print(f"Error in the execution of the ability {ability.name}: {e}")