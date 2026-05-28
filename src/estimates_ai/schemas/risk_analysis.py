from typing import List

from pydantic import BaseModel, Field

class RiskFactor(BaseModel):
    name: str = Field(default=..., description="The name of the risk factor")
    description: str = Field(default=..., description="A detailed description of the risk factor")
    likelihood: str = Field(default=..., description="The likelihood of this risk occurring (e.g., low, medium, high)")
    impact: str = Field(default=..., description="The potential impact of this risk if it occurs (e.g., low, medium, high)")
    mitigation_strategy: str = Field(default=..., description="A strategy for mitigating this risk")

class RiskFactorStructuredResponse(BaseModel):
    summary: str = Field(default=..., description="A brief summary of the overall risk analysis")
    risk_factors: List[RiskFactor] = Field(default=..., description="A list of identified risk factors with their details")
    overall_risk_assessment: str = Field(default=..., description="An overall assessment of the project's risk level based on the identified factors")


