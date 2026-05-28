from typing import List

from pydantic import BaseModel, Field


class TechChoiceEvaluation(BaseModel):
    technology: str = Field(default=..., description="The name of the technology being evaluated")
    rationale: str = Field(default=..., description="The rationale for choosing this technology")
    alternatives: List[str] = Field(default=..., description="A list of alternative technologies that could be used instead")


class TechAdvisorStructuredResponse(BaseModel):
    summary: str = Field(default=..., description="A brief summary of the overall tech stack evaluation")
    stack_evaluation: List[TechChoiceEvaluation] = Field(default=..., description="A detailed evaluation of each technology in the stack")
    architectural_patterns: List[str] = Field(default=..., description="A list of architectural patterns suited for this project")
    team_fit_assessment: str = Field(default=..., description="An assessment of how well the stack fits the team's knowledge and skill level")
    final_recommendation: str = Field(default=..., description="The final recommendation or conclusion for the tech stack")
