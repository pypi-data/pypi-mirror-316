from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.aaveV3 import BaseAaveAction as BaseAaveAction
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.observations.aaveV3 import AAVEv3Observation as AAVEv3Observation
from dojo.policies import AAVEv3Policy as BaseAAVEv3Policy
from typing import Any

@dataclass
class _TokenAndAmount:
    token_name: str
    amount: Decimal
    def __init__(self, token_name, amount) -> None: ...

@dataclass
class _UserData:
    collaterals: list[_TokenAndAmount]
    borrows: list[_TokenAndAmount]
    def __init__(self, collaterals, borrows) -> None: ...

class _HistoricReplayPolicy(BaseAAVEv3Policy):
    DEFAULT_GAS: int
    def __init__(self, chain: Chain, block_range: tuple[int, int]) -> None: ...
    def predict(self, obs: AAVEv3Observation) -> list[BaseAaveAction]: ...

class HistoricReplayAgent(BaseAgent[Any]):
    def __init__(self, chain: Chain, block_range: tuple[int, int], name: str = 'MarketAgent') -> None: ...
    def reward(self, obs: Any) -> float: ...
