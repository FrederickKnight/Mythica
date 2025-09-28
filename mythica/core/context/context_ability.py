from pydantic import BaseModel
from mythica.core import BaseCreature

class ContextAbility(BaseModel):
    """
    Class used to provide context to an ability, 
    like the target or the creature using it and more.
    """
    user:BaseCreature = None
    target:BaseCreature = None
    alive_creatures:list[BaseCreature] = None