from pydantic import BaseModel,Field,PrivateAttr,field_validator, model_validator
from typing import Self
import random
from mythica.core import BaseCreature, BaseAbility
from mythica.core.context import ContextAbility
from mythica.utils import EcosystemIO

class BaseEcosystem(BaseModel):
    name:str
    creatures:set[BaseCreature] = Field(default_factory=set)
    seed:int = None
    logger:EcosystemIO = Field(default_factory=EcosystemIO)
    
    _alive_creatures:set[BaseCreature] = PrivateAttr(default_factory=set)
    _active_creatures:set[BaseCreature] = PrivateAttr(default_factory=set)
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

        self._alive_creatures = {creature for creature in self.creatures if creature.is_alive()}
        self._active_creatures = {creature for creature in self._alive_creatures if creature.energy > 0}
        return self
    
    def simulate_simple_battle_turn(self,turn:int = None) -> None:
        """
        Simulation where the creatures battle between them, using only it's abilities.
        """
        if not self._alive_creatures or not self._active_creatures:
            return
        
        if turn != None:
            self.logger.log(f"------------Turn {turn + 1}------------")

        ability_context = ContextAbility(
            alive_creatures = self._alive_creatures
        )

        _creatures_to_remove_alive:set[BaseCreature]  = set()
        _creatures_to_remove_active:set[BaseCreature]  = set()

        for creature in self._active_creatures:
            if not creature.is_alive():
                _creatures_to_remove_alive.add(creature)
                _creatures_to_remove_active.add(creature)
                continue

            if creature.energy <= 0:
                _creatures_to_remove_active.add(creature)
                self.logger.log(f"{creature.name} can't act")
                continue
            
            try:
                act_result = creature.act(
                    ability_context = ability_context,
                    random = self._random
                )
                self.logger.log(act_result)

                if creature.energy <= 0:
                    _creatures_to_remove_active.add(creature)

            except Exception as e:
                self.logger.log(f"Error in the execution of the act {creature.name}: {e}")
        
        for creature in self._alive_creatures:
            if not creature.is_alive():
                _creatures_to_remove_alive.add(creature)
                _creatures_to_remove_active.add(creature)
                self.logger.log(f"{creature.name} has died")

        self._alive_creatures -= _creatures_to_remove_alive
        self._active_creatures -= _creatures_to_remove_active


    def simulate_simple_battle(self,turns:int = 10) -> None:
        """
        Cycle in a range of turns given calling the method simulate_simple_battle_turn

        Args:
            turns (int, optional): turns to cycle for. Defaults to 10.
        """
        for turn in range(turns):
            if len(self._alive_creatures) <= 1 or not self._active_creatures:
                self.logger.log("Simulation ended: no alive or active creatures left.")
                break
            
            self.simulate_simple_battle_turn(turn)

    def simulate_turn_of_season(self,turn:int = None):
        if not self._alive_creatures or not self._active_creatures:
            return
        
        if turn != None:
            self.logger.log(f"------------Turn {turn + 1}------------")

        ability_context = ContextAbility(
            alive_creatures = self._alive_creatures
        )

        _creatures_to_remove_alive:set[BaseCreature]  = set()
        _creatures_to_remove_active:set[BaseCreature]  = set()

        for creature in self._active_creatures:
            if not creature.is_alive():
                _creatures_to_remove_alive.add(creature)
                _creatures_to_remove_active.add(creature)
                continue

            if creature.energy <= 0:
                _creatures_to_remove_active.add(creature)
                self.logger.log(f"{creature.name} can't act")
                continue
            
            try:
                act_result = creature.act(
                    ability_context = ability_context,
                    random = self._random
                )
                self.logger.log(act_result)

                if creature.energy <= 0:
                    _creatures_to_remove_active.add(creature)

            except Exception as e:
                self.logger.log(f"Error in the execution of the act {creature.name}: {e}")
        
        for creature in self._alive_creatures:
            if not creature.is_alive():
                _creatures_to_remove_alive.add(creature)
                _creatures_to_remove_active.add(creature)
                self.logger.log(f"{creature.name} has died")


        self._alive_creatures -= _creatures_to_remove_alive
        self._active_creatures -= _creatures_to_remove_active

    def simulate_season(self,seasons:int = 5, turns_for_season:int = 5) -> None:
        for season in range(seasons):
            if len(self._alive_creatures) <= 1 or not self._active_creatures:
                self.logger.log("Simulation ended: no alive or active creatures left.")
                break
            
            self.logger.log(f"------------Season {season + 1}------------")

            for turn in range(turns_for_season):
                self.simulate_turn_of_season(
                    turn = turn
                )
            
            # Cross creatures
            _creatures_to_cross:set[BaseCreature] = self._active_creatures.copy()

            self.logger.log("------------Mating Season--------------")
            self.logger.log(f"Creatures : {_creatures_to_cross}")

            if len(_creatures_to_cross) > 1:
                for creature in _creatures_to_cross:
                    partner = creature.choose_partner(
                        random = self._random,
                        creatures = list(_creatures_to_cross)
                    )
                    
                    child = creature.cross_genes(
                        random = self._random,
                        other = partner
                    )
                    if child:
                        self.logger.log(f"{creature.name} mate with {partner.name}")
                        self.logger.log(f"New Child: {child}")
                        self._alive_creatures.add(child)
                        self._active_creatures.add(child)
                    else:
                        self.logger.log(f"{creature.name} couldn't mate")

            self.logger.log("---------------------------------------")