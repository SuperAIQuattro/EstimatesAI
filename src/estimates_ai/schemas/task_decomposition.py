from enum import Enum
from pydantic import BaseModel, Field

class ActivityType(str, Enum):
    FEATURE = "feature"
    BUG = "bug"
    REFACTOR = "refactor"
    DOCUMENTATION = "documentation"
    TESTING = "testing"

class ProjectIdea(BaseModel):
    description: str = Field(
        default=...,
        description="A brief description of the project idea"
    )

class Activity(BaseModel):
    name: str = Field(
        default=...,
        description="The name of the activity"
    )
    description: str = Field(
        default=...,
        description="A brief description of the activity"
    )
    activity_type: ActivityType = Field(
        default=...,
        description="The type of the activity, e.g., 'feature', 'bug', 'refactor', etc."
    )
    acceptance_criteria: list[str] = Field(
        default=...,
        description="A list of acceptance criteria for the activity"
    )

class ActivityList(BaseModel):
    activities: list[Activity] = Field(
        default=...,
        description="A list of activities"
    )
