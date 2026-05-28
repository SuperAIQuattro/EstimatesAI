from pydantic import BaseModel, Field

class Team(BaseModel):
    name: str = Field(default=..., description="The name of the team")
    members: list[str] = Field(default=..., description="The members of the team")
    kind: str = Field(default=..., description="The kind of the team")
