from datapizza.tools import tool

from estimates_ai.llm.client_factory import default_client as client
from estimates_ai.schemas.estimation import EstimationResult
from estimates_ai.schemas.task_decomposition import Activity


# ── Tool ─────────────────────────────────────────────────────────────────────

@tool
def estimate_activity(activity: Activity) -> str:
    """Stima il carico di lavoro umano (in ore) per una User Story / attività software.

    Riceve un'attività ad alto livello (User Story in ottica Scrum) e produce una stima
    strutturata che include:
    - ore totali stimate con range min/max
    - confidence score e livello di rischio
    - complessità tecnica
    - scomposizione in sottotask implementativi
    - ruoli del team necessari
    - possibili bottleneck

    Il risultato viene poi utilizzato da team_allocation per assegnare i subtask al team.

    Args:
        activity: L'attività da stimare, con nome, descrizione e tipo.

    Returns:
        JSON con la stima completa in formato EstimationResult.
    """
    prompt = (
        f"User Story da stimare:\n"
        f"Nome: {activity.name}\n"
        f"Tipo: {activity.activity_type}\n"
        f"Descrizione: {activity.description}"
    )

    result = client.structured_response(
        input=prompt,
        output_cls=EstimationResult,
        system_prompt=(
            "Sei un senior engineering manager con 15+ anni di esperienza nella stima di progetti software. "
            "Ricevi una User Story in formato Scrum e devi produrre una stima realistica. "
            "Scomponi la User Story in sottotask implementativi concreti (es. design API, implementazione BE, test unitari, deploy). "
            "Stima le ore per ogni sottotask e calcola il totale con un range min/max. "
            "Considera overhead per code review, testing, fix e deploy. "
            "Indica i ruoli necessari e i possibili colli di bottiglia. "
            "Se le informazioni sono insufficienti, abbassa il confidence_score e spiega nelle note."
        ),
        temperature=0,
    )

    estimate: EstimationResult = result.structured_data[0]
    return estimate.model_dump_json(indent=2)
