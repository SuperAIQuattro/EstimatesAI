from estimates_ai.schemas.task_decomposition import Activity, ActivityType
from estimates_ai.tools.team_allocation import team_allocation

activity = Activity(
    name="Implementazione autenticazione",
    description="Sviluppare il sistema di login con JWT e gestione sessioni.",
    activity_type=ActivityType.FEATURE,
    acceptance_criteria=["Login funzionante", "Token JWT rilasciato", "Logout invalida il token"],
)

result = team_allocation(activity)
print(result)
