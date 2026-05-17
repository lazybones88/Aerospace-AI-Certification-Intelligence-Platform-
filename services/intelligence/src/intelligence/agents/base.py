from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from domain.evidence import AgentResult


class AgentContext(BaseModel):
    program_id: str
    user_id: str
    entity_ids: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """Specialized certification agent with auditable tool use."""

    agent_id: str
    task_type: str

    @abstractmethod
    async def run(self, context: AgentContext) -> AgentResult:
        """Execute agent task and return grounded, validated result."""
