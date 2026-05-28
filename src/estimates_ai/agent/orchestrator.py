from datapizza.agents import Agent
from estimates_ai.llm.client_factory import create_openai_client
import streamlit as st

def build_client():
    return create_openai_client(
        model=st.session_state.get("selected_model", "gpt-4o-mini"),
        temperature=st.session_state.get("temperature", 0.7),
        system_prompt=st.session_state.get("system", ""),
    )

def build_estimates_agent():
    client = build_client()
    return Agent(
        name="estimates_agent",
        client=client,
        system_prompt=st.session_state.get("system", ""),
        tools=[],
    )
    
    
# Istanza di default — usata dai tool
default_orchestrator = build_estimates_agent()