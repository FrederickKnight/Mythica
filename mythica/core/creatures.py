from pydantic import BaseModel,Field, field_validator
from .ability import BaseAbility
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mythica.core.context import ContextAbility

class BaseCreature(BaseModel):
    name:str
    health:float
    velocity:float
    energy:float
    abilities:list[BaseAbility] = Field(default_factory=list[BaseAbility])

    @field_validator("abilities",mode="before")
    @classmethod
    def validate_abilities(cls,abilities:list[BaseAbility]) -> list[BaseAbility]:

        if not all(isinstance(ability,BaseAbility) for ability in abilities):
            raise TypeError("Every ability must be from BaseAbility")

        unique_abilities = {a.name: a for a in abilities}.values()
        return sorted(unique_abilities, key=lambda a: a.name)

    def is_alive(self) -> bool:
        """
        Check if the creature is still alive.

        Returns:
            bool: True if is alive and False if it doesn't.
        """
        return self.health > 0
    
    def take_damage(self,quantity:float) -> None:
        """
        Substract the health of the Creature with the quantity.

        Args:
            quantity (float): quantity to substract from the health.
        """
        if isinstance(quantity,int) or isinstance(quantity,float):
            self.health = max(0,self.health - quantity)

    def use_energy(self,quantity:float) -> None:
        """
        Substract the energy of the Creature with the quantity.

        Args:
            quantity (float): quantity to Substract from the energy.
        """
        if isinstance(quantity,int) or isinstance(quantity,float):
            self.energy = max(0,self.energy - quantity)

    def add_ability(self,ability:BaseAbility) -> None:
        """
        Add an ability to the creature.

        Args:
            ability (BaseAbility): the ability that will be added to the creature.
        """
        if not isinstance(ability,BaseAbility):
            return
        
        if ability not in self.abilities:
            self.abilities.append(ability)
        
    def add_abilities(self,abilities:list[BaseAbility]) -> None:
        """
        Add a list of abilities to the creature.

        Args:
            abilities (list[BaseAbility]): the abilities that will be added to the creature.
        """
        for ability in abilities:
            self.add_ability(ability)

    def use_ability(self,ability:BaseAbility,ctx:"ContextAbility"):
        if not isinstance(ability,BaseAbility) or self.energy <= 0 or ability not in self.abilities:
            return
        
        if self.energy >= ability.cost:
            self.use_energy(ability.cost)
            return ability.effect(ctx)
        else:
            return f"{self.name} can't use {ability.name}"

    ## DUNDER ##
    def __str__(self):
        return f"<{self.name.upper()}(Health:{self.health},Velocity:{self.velocity},Energy:{self.energy})>"
    
    def __repr__(self):
        return f"<{self.name.upper()}(Health:{self.health},Velocity:{self.velocity},Energy:{self.energy})>"