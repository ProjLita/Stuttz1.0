"""
MODELOS DE DADOS DO STUTTZ
Define como os dados são organizados e validados
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class UserData:
    """
    Dados do usuário
    """
    name: str = "Estudante"
    level: int = 1
    xp: int = 0
    xp_to_next: int = 500
    streak: int = 0
    last_activity: Optional[str] = None
    completed_phases: List[int] = []
    
    def __post_init__(self):
        if self.completed_phases is None:
            self.completed_phases = []

@dataclass  
class QuizData:
    """
    Dados de um quiz
    """
    question: str
    options: List[str]
    correct_answer_index: int
    explanation: str
    
    def is_valid(self) -> bool:
        """Verifica se o quiz é válido"""
        return (
            len(self.options) == 4 and
            0 <= self.correct_answer_index < 4 and
            len(self.question) > 0
        )

@dataclass
class PhaseData:
    """
    Dados de uma fase
    """
    id: int
    title: str
    description: str
    status: str  # "locked", "unlocked", "current", "completed"
    tasks: List[str]
    quiz: QuizData

@dataclass
class RoadmapData:
    """
    Dados do roadmap completo
    """
    course_name: str
    total_phases: int
    phases: List[PhaseData]
    
    def get_phase_by_id(self, phase_id: int) -> Optional[PhaseData]:
        """Encontra uma fase pelo ID"""
        for phase in self.phases:
            if phase.id == phase_id:
                return phase
        return None
    
    def get_unlocked_phases(self) -> List[PhaseData]:
        """Retorna apenas fases desbloqueadas"""
        return [p for p in self.phases if p.status != "locked"]
    
    def calculate_progress(self) -> float:
        """Calcula progresso em percentual"""
        completed = sum(1 for p in self.phases if p.status == "completed")
        return (completed / self.total_phases) * 100 if self.total_phases > 0 else 0

# === FUNÇÕES AUXILIARES ===

def create_default_roadmap() -> Dict[str, Any]:
    """
    Cria um roadmap padrão para o protótipo
    """
    return {
        "course_name": "Python para Iniciantes",
        "total_phases": 5,
        "phases": [
            {
                "id": 1,
                "title": "Fundamentos",
                "description": "Conceitos básicos do Python",
                "status": "unlocked",
                "tasks": [
                    "Instalar Python",
                    "Entender variáveis", 
                    "Primeiro programa"
                ],
                "quiz": {
                    "question": "Qual comando exibe texto em Python?",
                    "options": ["show()", "print()", "display()", "output()"],
                    "correct_answer_index": 1,
                    "explanation": "print() é a função padrão."
                }
            },
            {
                "id": 2,
                "title": "Estruturas de Dados",
                "description": "Listas, tuplas e dicionários",
                "status": "locked",
                "tasks": [
                    "Criar listas",
                    "Usar tuplas",
                    "Trabalhar com dicionários"
                ],
                "quiz": {
                    "question": "Como criar uma lista vazia?",
                    "options": ["list()", "[]", "new list()", "empty()"],
                    "correct_answer_index": 1,
                    "explanation": "[] é a sintaxe mais comum."
                }
            }
            # Adicione mais fases conforme necessário
        ]
    }

def validate_quiz_data(quiz: Dict[str, Any]) -> bool:
    """
    Valida se dados do quiz estão corretos
    """
    required_keys = ["question", "options", "correct_answer_index", "explanation"]
    
    # Verificar se todas as chaves existem
    if not all(key in quiz for key in required_keys):
        return False
    
    # Verificar se options tem exatamente 4 itens
    if len(quiz["options"]) != 4:
        return False
    
    # Verificar se correct_answer_index é válido
    if not 0 <= quiz["correct_answer_index"] < 4:
        return False
    
    return True
