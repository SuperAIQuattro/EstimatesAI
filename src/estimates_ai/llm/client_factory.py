from datapizza.clients.openai import OpenAIClient
from estimates_ai.config.settings import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE


def create_openai_client(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    system_prompt: str = "",
) -> OpenAIClient:
    return OpenAIClient(
        api_key=OPENAI_API_KEY,
        model=model,
        temperature=temperature,
        system_prompt=system_prompt,
    )


# Istanza di default — usata dai tool
default_client = create_openai_client()
