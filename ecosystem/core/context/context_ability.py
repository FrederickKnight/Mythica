from pydantic import BaseModel
from ecosystem.core import BaseCreature

class ContextAbility(BaseModel):
    """
    Class used to provide context to an ability, 
    like the target or the creatur using it and more.
    """
    user:BaseCreature = None
    target:BaseCreature = None
    targets:list[BaseCreature] = None