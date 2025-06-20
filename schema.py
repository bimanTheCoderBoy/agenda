from pydantic import BaseModel, Field
from typing import Optional, List, Any,Annotated
import operator

# For planning output structure
class PlanStep(BaseModel):
    step: str = Field(description="Description of task step")
    tool_hint: str = Field(description="Suggested tool for this step or 'none'")

class PlanOutput(BaseModel):
    plan: List[PlanStep]

# For full state
class AgentState(BaseModel):
    user_input: Optional[str]
    plan_json: Optional[PlanOutput] = None
    approval_given: Optional[bool] = None
    tools_selected: Optional[Any] = None
    tool_outputs: Optional[List[Any]] = None
    final_approval: Optional[bool] = None
    observer_decision: Optional[Any] = None
    chat_history:Annotated[ Optional[List[Any]] , operator.add]
