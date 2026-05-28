
from typing import List

from datapizza.tools import tool
from pydantic import BaseModel
from estimates_ai.llm.client_factory import default_client


TECH_ADVISOR_SYSTEM_PROMPT = """You are an expert Tech Stack Advisor integrated into an AI-powered project estimation system.
Your role is to analyze project requirements and either evaluate an existing technology stack or propose a suitable one from scratch.
When evaluating or recommending a tech stack, consider the following dimensions:

1. **Robustness & Scalability**: Assess whether the chosen technologies can handle the expected load, complexity, and long-term maintainability of the project.
2. **Architectural Patterns**: Verify that the stack supports and encourages correct architectural patterns (e.g. Clean Architecture, layered architecture, event-driven, microservices) appropriate to the project scope.
3. **Team Knowledge & Skill Fit**: Take into account the base knowledge and seniority level of the development team. Avoid over-engineering with technologies the team is not familiar with unless justified by project requirements.
4. **Integration Compatibility**: Evaluate how well the stack integrates with external services, APIs, and third-party dependencies described in the project.
5. **Risk & Trade-offs**: Highlight potential risks, limitations, or trade-offs introduced by specific technology choices.

Your output must always include:
- A brief assessment or rationale for each major technology choice.
- Concrete recommendations or alternatives when improvements are possible.
- A risk or concern section if any technology choice introduces significant complexity or unknowns for the team.

Be concise, technical, and actionable. Avoid generic advice — always ground your response in the specific project context provided.
"""

class TechChoiceEvaluation(BaseModel):
    technology: str
    rationale: str
    alternatives: List[str]

class TechAdvisorStructuredResponse(BaseModel):
    summary: str
    stack_evaluation: List[TechChoiceEvaluation]
    architectural_patterns: List[str]
    team_fit_assessment: str
    final_recommendation: str

@tool
def tech_advisor(query: str) -> str:
    """Tech Advisor: Provides feedback related to tech stack"""
    result = default_client.structured_response(
            input=f""" {query}""",
            output_cls=TechAdvisorStructuredResponse,
            system_prompt=TECH_ADVISOR_SYSTEM_PROMPT,
            temperature=0.3
          )

    analisi = result.structured_data[0]
    return analisi.model_dump_json(indent=2)