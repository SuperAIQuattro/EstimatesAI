import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))

from estimates_ai.tools.task_decomposition import task_decomposition
from estimates_ai.tools.estimation import estimate_activity
from estimates_ai.tools.team_allocation import team_allocation
from estimates_ai.tools.risk_analysis import risk_analysis
from estimates_ai.tools.tech_advisor import tech_advisor

# ─── INPUT TASK ────────────────────────────────────────────────────────────────

PROJECT_DESCRIPTION = """
Implementare una nuova funzionalità per la sezione Gestione Pagamenti
che consenta agli utenti di visualizzare lo storico delle transazioni,
con possibilità di filtro per stato pagamento, intervallo date e metodo di pagamento.

La funzionalità dovrà prevedere:
- aggiunta dei filtri nella UI;
- integrazione con endpoint backend per il recupero dati paginati.

File coinvolti:
Frontend:
  src/modules/payments/components/PaymentHistoryTable.tsx
  src/modules/payments/components/PaymentFiltersPanel.tsx
  src/modules/payments/pages/PaymentsDashboardPage.tsx
  src/modules/payments/hooks/usePaymentHistory.ts
  src/modules/payments/services/paymentApiClient.ts
  src/modules/payments/styles/payment-history.scss

Backend:
  server/modules/payments/controllers/paymentHistoryController.ts
  server/modules/payments/services/paymentHistoryService.ts
  server/modules/payments/repositories/paymentRepository.ts
  server/modules/payments/routes/paymentRoutes.ts
  server/modules/payments/dto/paymentHistoryFilter.dto.ts

I dati relativi allo storico pagamenti non vengono recuperati direttamente dal
database interno, ma tramite integrazione col servizio esterno DATABASE_BANKING.
""".strip()

TECH_STACK = """
Stack tecnologico:
- Frontend: TypeScript, React, SCSS
- Backend: Node.js, TypeScript
- Integrazione esterna: DATABASE_BANKING (servizio bancario esterno, API REST)
- Pattern: REST API con paginazione, DTO per validazione input
- Architettura: moduli separati per controller/service/repository

""" + PROJECT_DESCRIPTION

# ─── STEP 1: TASK DECOMPOSITION ────────────────────────────────────────────────

print("\n" + "="*60)
print("STEP 1 — TASK DECOMPOSITION")
print("="*60)

decomposition_result = task_decomposition(f"Progetto: {PROJECT_DESCRIPTION}")
print(decomposition_result)

activities = json.loads(decomposition_result).get("activities", [])

# ─── STEP 2: ESTIMATE EACH ACTIVITY ────────────────────────────────────────────

print("\n" + "="*60)
print("STEP 2 — ESTIMATION PER ACTIVITY")
print("="*60)

estimations = []
for activity in activities:
    criteria = "\n  - ".join(activity.get("acceptance_criteria", []))
    query = (
        f"Nome: {activity['name']}\n"
        f"Tipo: {activity['activity_type']}\n"
        f"Descrizione: {activity['description']}\n"
        f"Criteri di accettazione:\n  - {criteria}"
    )
    print(f"\n--- Estimating: {activity['name']} ---")
    result = estimate_activity(query)
    print(result)
    estimations.append(json.loads(result))

# ─── STEP 3: TEAM ALLOCATION (based on the most complex activity) ──────────────

print("\n" + "="*60)
print("STEP 3 — TEAM ALLOCATION")
print("="*60)

# Use the activity with the highest total estimated hours
most_complex = max(estimations, key=lambda e: e.get("total_estimated_hours", 0))
roles = ", ".join(most_complex.get("suggested_roles", []))
bottlenecks = ", ".join(most_complex.get("possible_bottlenecks", []))

team_query = (
    f"Totale ore stimate: {most_complex['total_estimated_hours']}\n"
    f"Range: {most_complex['minimum_hours']} - {most_complex['maximum_hours']} ore\n"
    f"Confidenza: {most_complex['confidence_score']}\n"
    f"Livello di rischio: {most_complex['risk_level']}\n"
    f"Complessità tecnica: {most_complex['technical_complexity']}\n"
    f"Ruoli suggeriti: {roles}\n"
    f"Possibili colli di bottiglia: {bottlenecks}\n"
    f"Note: {most_complex.get('notes', '')}"
)

team_result = team_allocation(team_query)
print(team_result)

# ─── STEP 4: RISK ANALYSIS ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("STEP 4 — RISK ANALYSIS")
print("="*60)

risk_result = risk_analysis(PROJECT_DESCRIPTION)
print(risk_result)

# ─── STEP 5: TECH ADVISOR ──────────────────────────────────────────────────────

print("\n" + "="*60)
print("STEP 5 — TECH ADVISOR")
print("="*60)

tech_result = tech_advisor(TECH_STACK)
print(tech_result)

print("\n" + "="*60)
print("DONE")
print("="*60)
