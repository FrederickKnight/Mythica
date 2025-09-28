from pydantic import BaseModel,PrivateAttr,field_serializer

from mythica.schema import AbilityCategoryEnum,AbilityObjectiveEnum
from typing import Literal, Union, Self, Callable, TYPE_CHECKING

AbilityCategories = Union[AbilityCategoryEnum,Literal["attack","defense"]]
AbilityObjectives = Union[AbilityObjectiveEnum,Literal["all","all_except_user","single_target"]]

if TYPE_CHECKING:
    from mythica.core.context import ContextAbility

class BaseAbility(BaseModel):
    name:str
    cost:int
    category:AbilityCategories
    objective:str
    effect:Callable[[any],str]

    @field_serializer("category")
    def serialize_category(self,category:AbilityCategories) -> str:
        if isinstance(category,AbilityCategoryEnum):
            return category.value
        return category
    
    def use(self,ability_context:"ContextAbility") -> str:
        if self.objective == AbilityObjectiveEnum.SINGLE_TARGET and not ability_context.target:
            return f"{ability_context.user.name} can't use {self.name} without target."
        return self.effect(ability_context)

    ## DUNDER ##
    def __str__(self):
        return f"<Ability(Name:{self.name},Cost:{self.cost},Category:{self.category})>"
    
    def __repr__(self):
        return f"<Ability(Name:{self.name},Cost:{self.cost},Category:{self.category})>"

    def __eq__(self, other:Self):
        if isinstance(other, BaseAbility):
            return self.name == other.name and self.cost == other.cost and self.category == other.category
        return False
    
    def __hash__(self):
        obj = self.name, self.cost ,self.category
        return hash(obj)