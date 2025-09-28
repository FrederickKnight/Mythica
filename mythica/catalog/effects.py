from mythica.core.context import ContextAbility
from typing import Callable

EFFECTS: dict[str,Callable[[ContextAbility],str]] = {}

def register_effect(name:str):
    def wrapper(func:Callable[[ContextAbility],str]):
        if name in EFFECTS:
            raise ValueError(f"Effect {name} already exist.")
        EFFECTS[name] = func
        return func
    return wrapper

@register_effect("fire_ball")
def effect_fire_ball(ctx:"ContextAbility") -> str:
    damage = 20
    ctx.target.take_damage(damage)
    return f"{ctx.user.name} used a ball of fire to burn {ctx.target.name} making {damage} damage."

@register_effect("extreme_speed")
def effect_extreme_speed(ctx:"ContextAbility") -> str:
    damage = ctx.user.velocity * 2
    ctx.target.take_damage(
        quantity = damage
    )
    return f"{ctx.user.name} used extreme velocity to tackle {ctx.target.name} making {damage} damage."

@register_effect("tsunami")
def effect_tsunami(ctx:"ContextAbility") -> str:
    damage = 30
    for target in ctx.alive_creatures:
        if target != ctx.user:
            target.take_damage(damage)
    
    return f"{ctx.user.name} used a huge tsunami to drown everyone making {damage} damage."

@register_effect("tackle")
def effect_tackle(ctx:"ContextAbility") -> str:
    damage = 5
    ctx.target.take_damage(5)
    return f"{ctx.user.name} tackle {ctx.target.name} making {damage} damage."