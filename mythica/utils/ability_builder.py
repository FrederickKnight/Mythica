from asteval import Interpreter
import yaml
from pathlib import Path

from mythica.core import BaseAbility, BaseCreature
from mythica.core.context import ContextAbility
from mythica.schema import AbilityObjectiveEnum

eval_interpreter = Interpreter()

def load_abilities_from_yaml(path:str) -> dict[str,BaseAbility]:
    path_ab = Path(path).expanduser().resolve()

    if not path_ab.exists():
        raise FileNotFoundError(f"Ability file not found: {path_ab}")

    data = yaml.safe_load(path_ab.read_text())

    abilities = {}
    for key,ability in data.items():
        abilities[key] = BaseAbility(
            name = ability["name"],
            cost = ability["cost"],
            category = ability["category"],
            effect = make_effect(ability["effect"]),
            objective = ability["effect"]["objective"]
        )

    return abilities

def make_effect(effect_data:dict[str,any]):
    damage_expr = effect_data["damage"]

    #eval for now, to get a func
    damage_func = eval(f"lambda user:{damage_expr}")

    message_expr = effect_data.get("message","{user.name} hit doing {damage} damage.")
    objetive = objetives[effect_data["objective"]]

    def effect(ctx:ContextAbility) -> str:
        user = ctx.user
        target = ctx.target
        alive_creatures = ctx.alive_creatures

        damage = float(damage_func(user))

        objetive(
            ctx = ctx,
            damage = damage
        )

        return message_expr.format(
            user = user,
            target = target,
            damage = damage
        )

    return effect


## METHODS FOR OBJETIVES/TARGETS ##
def single_target(ctx:ContextAbility,damage:float = 0):
    ctx.target.take_damage(damage)

def all_except_user(ctx:ContextAbility,damage:float = 0):
    for target in ctx.alive_creatures:
        if target != ctx.user:
            target.take_damage(damage)

def all(ctx:ContextAbility,damage:float = 0):
    for target in ctx.alive_creatures:
        target.take_damage(damage)

objetives = {
    AbilityObjectiveEnum.SINGLE_TARGET:single_target,
    AbilityObjectiveEnum.ALL:all,
    AbilityObjectiveEnum.ALL_EXCEPT_USER:all_except_user,
}