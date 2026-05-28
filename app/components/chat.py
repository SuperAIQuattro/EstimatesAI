import streamlit as st

from datapizza.type import ROLE, TextBlock
from estimates_ai.agent.orchestrator import default_orchestrator

MODEL_COSTS = {
  "gpt-5.4": {"cost_input": 2.50, "cost_output": 15.00},
  "gpt-5.4-nano": {"cost_input": 0.10, "cost_output": 0.625},
}


def total_cost(model: str, token_input: int, token_output: int) -> float:
  costs = MODEL_COSTS.get(model, {"cost_input": 0, "cost_output": 0})
  return (
    (token_input * costs["cost_input"]
    + token_output * costs["cost_output"]) / 10**6
  )


def render_chat(selected_model: str, temperature: float) -> None:
  """Render chat history and handle a new user message."""
  # HISTORY MANAGEMENT + FIRST MESSAGE
  if len(st.session_state["history"]) == 0:
    with st.chat_message("assistant"):
      st.write("Benvenuto")

  for messaggio in st.session_state["history"]:
    with st.chat_message(messaggio["role"]):
      st.write(messaggio["content"])

  prompt_utente = st.chat_input("Scrivi un messaggio...")

  if not prompt_utente:
    return

  # Show user message
  with st.chat_message("user"):
    st.write(prompt_utente)

  # Add message to history
  st.session_state["history"].append({"role": "user", "content": prompt_utente})

  with st.chat_message("assistant"):
    with st.spinner("Sto pensando..."):
      try:
        # Call Agent
        response = default_orchestrator.run(
          task_input=prompt_utente,
          memory=st.session_state["memory"],
        )

        response_text = response.text

        # Update memory
        st.session_state["memory"].add_turn(
          blocks=[TextBlock(content=prompt_utente)],
          role=ROLE.USER,
        )
        st.session_state["memory"].add_turn(
          blocks=response.content,
          role=ROLE.ASSISTANT,
        )

        # Token
        st.session_state["token_input"] += response.usage.prompt_tokens
        st.session_state["token_output"] += response.usage.completion_tokens

        st.session_state["token_total"] += (
          response.usage.prompt_tokens
          + response.usage.completion_tokens
        )

        # Costs
        st.session_state["cost"] = total_cost(
          selected_model,
          st.session_state["token_input"],
          st.session_state["token_output"],
        )

      except Exception as errore:
        response_text = f"Errore nella chiamata al selected_model: {errore}"
        st.error(response_text)

    st.write(response_text)

  st.session_state["history"].append(
    {"role": "assistant", "content": response_text}
  )
  st.rerun()
