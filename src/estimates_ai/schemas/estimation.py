from typing import List, Literal

from pydantic import BaseModel, Field


class Subtask(BaseModel):
    name: str = Field(description="Nome del sottotask")
    description: str = Field(description="Descrizione breve del sottotask")
    estimated_hours: float = Field(description="Ore stimate per completare il sottotask")
    complexity: Literal["bassa", "media", "alta"] = Field(
        description="Complessità tecnica del sottotask"
    )
    dependencies: List[str] = Field(
        default_factory=list,
        description="Nomi di altri sottotask da cui dipende"
    )


class EstimationResult(BaseModel):
    total_estimated_hours: float = Field(
        description="Stima totale in ore lavorative per completare l'attività"
    )
    minimum_hours: float = Field(
        description="Stima ottimistica (caso migliore)"
    )
    maximum_hours: float = Field(
        description="Stima pessimistica (caso peggiore)"
    )
    confidence_score: float = Field(
        ge=0.0, le=1.0,
        description="Grado di confidenza nella stima (0.0 = molto incerto, 1.0 = molto sicuro)"
    )
    risk_level: Literal["basso", "medio", "alto", "critico"] = Field(
        description="Livello di rischio complessivo dell'attività"
    )
    technical_complexity: Literal["bassa", "media", "alta", "molto_alta"] = Field(
        description="Complessità tecnica stimata dell'implementazione"
    )
    subtasks: List[Subtask] = Field(
        description="Lista di sottotask in cui è stata scomposta la User Story"
    )
    suggested_roles: List[str] = Field(
        description="Ruoli del team necessari per completare l'attività (es. Backend Dev, DevOps, QA)"
    )
    possible_bottlenecks: List[str] = Field(
        description="Possibili colli di bottiglia che potrebbero allungare i tempi"
    )
    notes: str = Field(
        description="Note aggiuntive e raccomandazioni per il team"
    )
