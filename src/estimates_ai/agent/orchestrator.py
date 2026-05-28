from datapizza.agents import Agent
from estimates_ai.llm.client_factory import create_openai_client
from estimates_ai.tools.tech_advisor import tech_advisor
from estimates_ai.tools.risk_analysis import risk_analysis
from estimates_ai.tools.task_decomposition import task_decomposition
from estimates_ai.tools.team_allocation import team_allocation
from estimates_ai.tools.estimation import estimate_activity

TOOLS = [task_decomposition, estimate_activity, team_allocation, risk_analysis, tech_advisor]


def build_estimates_agent(model: str, temperature: float, system_prompt: str) -> Agent:
    client = create_openai_client(model=model, temperature=temperature, system_prompt=system_prompt)
    return Agent(
        name="estimates_agent",
        client=client,
        system_prompt=system_prompt,
        tools=[],
    )
