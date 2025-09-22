import pytest


@pytest.fixture(scope="session", autouse=True)
def rebuild_models():
    """
    Rebuild models to ensure all references are correct.
    """

    from ecosystem.core import (
        BaseAbility,
        BaseCreature,
        BaseEcosystem
    )
    from ecosystem.core.context import ContextAbility


    ContextAbility.model_rebuild()
    BaseCreature.model_rebuild()
    BaseAbility.model_rebuild()
    BaseEcosystem.model_rebuild()