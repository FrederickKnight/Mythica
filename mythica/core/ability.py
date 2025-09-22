from pydantic import BaseModel,field_serializer

from mythica.schema import AbilityCategoryEnum
from typing import Literal, Union, Self, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from mythica.core.context import ContextAbility

AbilityCategories = Union[AbilityCategoryEnum,Literal["attack","defense"]]

class BaseAbility(BaseModel):
    name:str
    cost:int
    category:AbilityCategories
    effect:Callable[["ContextAbility"],str]

    @field_serializer("category")
    def serialize_category(self,category:AbilityCategories) -> str:
        if isinstance(category,AbilityCategoryEnum):
            return category.value
        return category
    
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