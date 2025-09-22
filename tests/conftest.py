import pytest


@pytest.fixture(scope="session", autouse=True)
def rebuild_models():
    """
    Rebuild models to ensure all references are correct.
    """

    from mythica.core import (
        BaseAbility,
        BaseCreature,
        BaseEcosystem
    )
    from mythica.core.context import ContextAbility


    ContextAbility.model_rebuild()
    BaseCreature.model_rebuild()
    BaseAbility.model_rebuild()
    BaseEcosystem.model_rebuild()