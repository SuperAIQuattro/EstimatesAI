from estimates_ai.schemas.task_decomposition import ProjectIdea
from estimates_ai.tools.task_decomposition import task_decomposition

idea = ProjectIdea(description="Piattaforma e-commerce con carrello, pagamenti Stripe e dashboard admin.")

result = task_decomposition(idea)
print(result)
