from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecosystem.core.context import ContextAbility

def effect_fire_ball(ctx:"ContextAbility") -> str:
    damage = 20
    ctx.target.take_damage(damage)
    return f"{ctx.user.name} used a ball of fire to burn {ctx.target.name} making {damage} damage."

def effect_extreme_speed(ctx:"ContextAbility") -> str:
    damage = ctx.user.velocity * 2
    ctx.target.take_damage(
        quantity = damage
    )
    return f"{ctx.user.name} used extreme velocity to tackle {ctx.target.name} making {damage} damage."

def effect_tsunami(ctx:"ContextAbility") -> str:
    damage = 30
    for target in [c for c in ctx.targets if c != ctx.user]:
        target.take_damage(damage)
    return f"{ctx.user.name} used a huge tsunami to drown everyone making {damage} damage."

def effect_tackle(ctx:"ContextAbility") -> str:
    damage = 5
    ctx.target.take_damage(5)
    return f"{ctx.user.name} tackle {ctx.target.name} making {damage} damage."

def effect_testicular_torsion(ctx:"ContextAbility") -> str:
    damage = 13 + (ctx.target.health * .2)
    ctx.target.take_damage(damage)
    return f"{ctx.target.name} AHHHHHHHH MIS HUEVOS, {damage} de daño recibido."