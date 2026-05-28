from pydantic import BaseModel, Field

class ProjectIdea(BaseModel):
    description: str = Field(default=..., description="A brief description of the project idea")

class Activity(BaseModel):
    name: str = Field(default=..., description="The name of the activity")
    description: str = Field(default=..., description="A brief description of the activity")
    activity_type: str = Field(default=..., description="The type of the activity, e.g., 'feature', 'bug', 'refactor', etc.")
