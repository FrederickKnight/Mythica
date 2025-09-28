import random
from pydantic import BaseModel,Field, PrivateAttr, field_validator, model_validator
from .ability import BaseAbility
import numpy as np
import hashlib
import math

from typing import Self,TYPE_CHECKING
if TYPE_CHECKING:
    from mythica.core.context import ContextAbility

from mythica.schema import GeneEnum,GeneTypeEnum
len_genes = len(GeneEnum)
len_genes_type = len(GeneTypeEnum)
shape_genes = (len_genes,len_genes_type)

class BaseCreature(BaseModel):
    name:str
    genes:np.ndarray = Field(default=np.ndarray)
    abilities:list[BaseAbility] = Field(default_factory=list[BaseAbility])

    parents:tuple[Self,Self] = Field(default=None)
    children:list[Self] = Field(default_factory=list)
    generation:int = 0

    _gene_key:int = PrivateAttr(default=None)

    model_config = {
        "arbitrary_types_allowed": True
    }

    @field_validator("abilities",mode="before")
    @classmethod
    def validate_abilities(cls,abilities:list[BaseAbility]) -> list[BaseAbility]:

        if not all(isinstance(ability,BaseAbility) for ability in abilities):
            raise TypeError("Every ability must be from BaseAbility")

        unique_abilities = {a.name: a for a in abilities}.values()
        return sorted(unique_abilities, key=lambda a: a.name)
    
    @field_validator("genes",mode="before")
    @classmethod
    def validate_genes(cls,genes):
        if genes is None or not isinstance(genes,np.ndarray):
            genes = np.ceil(np.array([
                [np.random.uniform(50,200),  # MAX_HEALTH
                np.random.uniform(100,500),  # MAX_ENERGY
                np.random.uniform(5,20)],    # VELOCITY
                [0.0, 0.0, 0.0]              # CURRENT VALUES
            ], dtype=float))

        if genes.shape == (1,len_genes_type):
            genes = np.vstack([genes, genes.copy()])

        elif genes.shape != shape_genes:
            raise ValueError(f"Genes must should have a shape of {shape_genes}, not {genes.shape}")
        
        genes[GeneEnum.CURRENT_VALUES] = genes[GeneEnum.MAX_VALUES].copy()

        return genes
    
    @property
    def gene_key(self):
        if self._gene_key is None:
            data = f"{self.name}:{np.array([*self.genes[GeneEnum.MAX_VALUES]]).tobytes()}".encode()
            self._gene_key = int(hashlib.sha256(data).hexdigest(),16)
        return self._gene_key

    @property
    def max_health(self):
        return self.genes[GeneEnum.MAX_VALUES][GeneTypeEnum.HEALTH]
    
    @property
    def health(self):
        return self.genes[GeneEnum.CURRENT_VALUES][GeneTypeEnum.HEALTH]
    
    @health.setter
    def health(self, value: float) -> None:
        self.genes[GeneEnum.CURRENT_VALUES][GeneTypeEnum.HEALTH] = value
    
    @property
    def max_energy(self):
        return self.genes[GeneEnum.MAX_VALUES][GeneTypeEnum.ENERGY]
    
    @property
    def energy(self):
        return self.genes[GeneEnum.CURRENT_VALUES][GeneTypeEnum.ENERGY]
    
    @energy.setter
    def energy(self, value:float):
        self.genes[GeneEnum.CURRENT_VALUES][GeneTypeEnum.ENERGY] = value
    
    @property
    def max_velocity(self):
        return self.genes[GeneEnum.MAX_VALUES][GeneTypeEnum.VELOCITY]
    
    @property
    def velocity(self):
        return self.genes[GeneEnum.CURRENT_VALUES][GeneTypeEnum.VELOCITY]
    
    @velocity.setter
    def velocity(self, value:float):
        self.genes[GeneEnum.CURRENT_VALUES][GeneTypeEnum.VELOCITY] = value

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

    def use_ability(self,ability:BaseAbility,ctx:"ContextAbility") -> str:
        """
        Creature will use an ability and its energy will be drain.

        Args:
            ability (BaseAbility): ability to use.
            ctx (ContextAbility): context of the ability

        Returns:
            str: text of the ability used.
        """
        if not isinstance(ability,BaseAbility) or self.energy <= 0 or ability not in self.abilities:
            return
        
        if self.energy >= ability.cost:
            self.use_energy(ability.cost)
            return ability.effect(ctx)
        else:
            return f"{self.name} can't use {ability.name}"
        
    def act(self,ability_context:"ContextAbility",random:random.Random) -> str:
        """
        Creature will act using all in its capabilities.

        Args:
            ability_context (ContextAbility): context for the abilities of the creature. The 'user' and 'target' are selected whitin this method.
            random (random.Random, optional): random for choices in the act. Defaults to None.

        Returns:
            str: text of the result of the act.
        """
        
        ability:BaseAbility = self._choice_ability_(
            random = random
        )
        if not ability:
          return f"{self.name} can't act"

        self.use_energy(ability.cost)

        ability_context.user = self
        
        posible_targets = ability_context.alive_creatures
        ability_context.target = self._choice_target_(
            targets = posible_targets,
            random = random
        ) if len(posible_targets) >= 2 else None

        return ability.use(ability_context)
    
    def mutate(self,random:random.Random,mutation_rate:float = 0.08) -> None:
        max_genes:np.ndarray = self.genes[GeneEnum.MAX_VALUES]

        for i in range(len_genes_type):
            change = math.ceil(random.uniform(-mutation_rate,mutation_rate) * max_genes[i])
            max_genes[i] = max(1,max_genes[i] + change)

        self.genes[GeneEnum.CURRENT_VALUES] = max_genes.copy()
        self._gene_key = None
    
    def cross_genes(self,random:random.Random,other:Self,name:str = None):
        if not other:
            return

        if self.energy < 10 or other.energy < 10:
            return

        child_genes = np.zeros_like(self.genes)
        for i in range(len_genes_type):
            child_genes[GeneEnum.MAX_VALUES][i] = random.choice([
                self.genes[GeneEnum.MAX_VALUES][i],
                other.genes[GeneEnum.MAX_VALUES][i]
            ])

        child_genes[GeneEnum.CURRENT_VALUES] = child_genes[GeneEnum.MAX_VALUES].copy()

        child = BaseCreature(
            name = name or f"{self.name[:3]}{other.name[:3]}",
            genes = child_genes,
            abilities = list(set(self.abilities + other.abilities))
        )
        
        child.mutate(
            random = random,
            mutation_rate = 0.08
        )

        child.parents = (self,other)
        child.generation = max(self.generation,other.generation) + 1
        self.children.append(child)
        other.children.append(child)

        self.use_energy(10)
        other.use_energy(10)

        return child

    def choose_partner(self,random:random.Random,creatures:Self,probability_to_choose:float = 0.8) -> Self:
        if len(creatures) <= 1:
            return
        
        # Didn't choose a partner
        if random.uniform(0,1) < probability_to_choose:
            return

        while True:
            creature:Self = random.choice(creatures)
            if creature != self:
                break
        return creature

    ## HELPERS ##
    def _choice_target_(self,targets:list[Self],random:random.Random):
        while True:
           target =  random.choice(targets)
           if target != self:
               break
        
        return target
    
    def _choice_ability_(self,random:random.Random):
        while True:
            ability = random.choice(self.abilities)
            if ability.cost <= self.energy:
                break
        return ability

    ## DUNDER ##
    def __str__(self):
        return f"<{self.name.upper()}(Health:{self.health},Velocity:{self.velocity},Energy:{self.energy},generation:{self.generation},parents:{self.parents},children:{self.children})>"
    
    def __repr__(self):
        return f"<{self.name.upper()}(Health:{self.health}/{self.max_health},Velocity:{self.velocity}/{self.max_velocity},Energy:{self.energy}/{self.max_energy})>"
    
    def __eq__(self, other:Self):
        if not isinstance(other,BaseCreature):
            return False

        return self.gene_key == other.gene_key
    
    def __hash__(self):
        return hash(self.gene_key)