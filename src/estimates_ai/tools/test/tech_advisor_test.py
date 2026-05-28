from estimates_ai.tools.tech_advisor import tech_advisor

result = tech_advisor("""Implementare una dashboard responsive con gestione autenticazione e integrazione con API esterne per visualizzare dati in tempo reale. """
                      """Il team ha Salvo che conosce solo fastapi e React. Michele conosce Springboot. Monica conosce Django. Christian conosce Angular. Il progetto richiede un'architettura a microservizi, con un carico previsto di 1000 utenti simultanei e necessità di scalabilità orizzontale. """)
print(result)