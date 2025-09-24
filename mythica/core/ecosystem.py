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
    
    _alive_creatures:list[BaseCreature] = []
    _active_creatures:list[BaseCreature] = []
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

        self._alive_creatures = [creature for creature in self.creatures if creature.is_alive()]
        self._active_creatures = [creature for creature in self._alive_creatures if creature.energy > 0]
        return self
    
    def simulate_simple_battle_turn(self,ability_context:ContextAbility,turn:int = None) -> None:
        """
        Simulation where the creatures battle between them, using only it's abilities.
        """
        if not self._alive_creatures:
            return
        
        if not self._active_creatures:
            return

        if turn:
            self.logger.log(f"-------Turn {turn + 1}------------")

        for creature in self._alive_creatures:
            if not creature.is_alive():
                self._alive_creatures.remove(creature)
                self._active_creatures.remove(creature)
                self.logger.log(f"{creature.name} has died")
                continue

            if creature.energy <= 0:
                self._active_creatures.remove(creature)
                self.logger.log(f"{creature.name} can't act")
                continue
            
            try:
                act_result = creature.act(
                    ability_context = ability_context,
                    random = self._random
                )
                self.logger.log(act_result)

                if creature.energy <= 0:
                    self._active_creatures.remove(creature)

            except Exception as e:
                self.logger.log(f"Error in the execution of the act {creature.name}: {e}")


    def simulate_simple_battle(self,turns:int = 10) -> None:
        """
        Cycle in a range of turns given calling the method simulate_simple_battle_turn

        Args:
            turns (int, optional): turns to cycle for. Defaults to 10.
        """
        ability_context = ContextAbility(
            alive_creatures = self._alive_creatures
        )

        for turn in range(turns):
            if not self._alive_creatures or not self._active_creatures:
                break
            
            self.simulate_simple_battle_turn(
                ability_context = ability_context,
                turn = turn
            )