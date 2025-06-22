"""
Configurações globais e constantes do aplicativo

Este módulo contém todas as configurações e constantes usadas em todo o aplicativo,
como cores, valores padrão, mensagens, etc.
"""

from typing import Dict, Any, Final, Union

class Config:
    """
    Classe com configurações globais do aplicativo
    
    Contém constantes e valores de configuração usados em todo o aplicativo.
    Todos os atributos são estáticos para facilitar o acesso.
    """
    
    # === CONFIGURAÇÕES GERAIS ===
    APP_NAME: Final[str] = "Stuttz"  # Nome do aplicativo
    APP_VERSION: Final[str] = "1.0.0"  # Versão do aplicativo
    
    # === CONFIGURAÇÕES DE INTERFACE ===
    TITLE_FONT: Final[str] = "Workbench"  # Fonte para títulos
    INTERFACE_FONT: Final[str] = "Roboto"  # Fonte para interface (será usada como Bold)
    TEXT_FONT: Final[str] = "Roboto"  # Fonte para texto geral
    
    # === TAMANHOS DE FONTE ===
    FONT_SIZE_TITLE: Final[int] = 28     # Títulos principais
    FONT_SIZE_SUBTITLE: Final[int] = 22  # Subtítulos
    FONT_SIZE_BUTTON: Final[int] = 18    # Botões
    FONT_SIZE_BODY: Final[int] = 16      # Texto normal
    FONT_SIZE_CAPTION: Final[int] = 14   # Texto secundário
    
    # === CONFIGURAÇÕES DE IA ===
    AI_MODEL: Final[str] = "models/gemini-2.0-flash"  # Modelo do Gemini a ser usado
    
    # === CONFIGURAÇÕES DE GAMIFICAÇÃO ===
    XP_PER_LEVEL: Final[int] = 100  # XP necessário para subir de nível
    XP_PER_CORRECT_ANSWER: Final[int] = 25  # XP ganho por resposta correta
    XP_PER_TASK: Final[int] = 10  # XP ganho por tarefa concluída
    
    # === TÍTULOS DOS NÍVEIS ===
    LEVEL_TITLES: Final[Dict[int, str]] = {
        1: "Aprendiz Curioso",
        2: "Estudante Dedicado",
        3: "Explorador do Saber",
        4: "Conhecedor Experiente",
        5: "Mestre do Aprendizado"
    }
    
    # === CORES DO TEMA ===
    COLORS: Final[Dict[str, str]] = {
        # Cores principais
        "primary_blue": "#2E5090",  # Azul escuro para elementos principais
        "secondary_blue": "#4A6DB5",  # Azul médio para elementos secundários
        "accent_gold": "#D4AF37",  # Dourado para elementos de destaque
        
        # Cores de fundo
        "parchment": "#F9F5E9",  # Cor de pergaminho para o fundo principal
        "background_dark": "#1A1A2E",  # Fundo escuro para a página
        "wood_brown": "#8B4513",  # Marrom madeira para bordas
        
        # Cores de texto
        "text_dark": "#333333",  # Texto escuro principal
        "text_light": "#E0E0E0",  # Texto claro para fundos escuros
        
        # Cores de status
        "success_green": "#28A745",  # Verde para sucesso
        "success_bg": "#E6F4EA",  # Fundo verde claro para sucesso
        "error_red": "#DC3545",  # Vermelho para erro
        "error_bg": "#FDECEA",  # Fundo vermelho claro para erro
        "warning_yellow": "#FFC107",  # Amarelo para avisos
        "info_blue": "#17A2B8",  # Azul para informações
        
        # Cores de estado
        "locked": "#AAAAAA",  # Cinza para itens bloqueados
        "unlocked": "#4A6DB5",  # Azul para itens desbloqueados
        "completed": "#28A745",  # Verde para itens completados
    }
    
    # === ARQUIVOS E CAMINHOS ===
    DEFAULT_ROADMAP_FILE: Final[str] = "roadmap_data.json"  # Arquivo com dados do roadmap
    USER_DATA_FILE: Final[str] = "user_data.json"  # Arquivo com dados do usuário

class Messages:
    """
    Mensagens usadas em todo o aplicativo
    
    Centraliza todas as mensagens exibidas ao usuário para facilitar
    a manutenção e possível internacionalização futura.
    """
    
    # === MENSAGENS DE GAMIFICAÇÃO ===
    LEVEL_UP: Final[str] = "🎉 Parabéns! Você alcançou o nível {level}!"
    XP_GAINED: Final[str] = "💫 Você ganhou {xp} pontos de experiência!"
    STREAK_CONTINUED: Final[str] = "🔥 Sequência de {days} dias! Continue assim!"
    
    # === MENSAGENS DE QUIZ ===
    QUIZ_CORRECT: Final[str] = "✅ Resposta correta! Você ganhou {xp} XP!"
    QUIZ_INCORRECT: Final[str] = "❌ Resposta incorreta. A resposta correta é: {correct}"
    NO_ANSWER_SELECTED: Final[str] = "⚠️ Selecione uma resposta antes de confirmar."
    
    # === MENSAGENS DE ERRO ===
    API_KEY_MISSING: Final[str] = "⚠️ Chave de API não configurada. Algumas funcionalidades estarão limitadas."
    DATA_LOAD_ERROR: Final[str] = "❌ Erro ao carregar dados. Usando configurações padrão."
    
    # === OUTRAS MENSAGENS ===
    WELCOME: Final[str] = "👋 Bem-vindo ao Stuttz, sua jornada de aprendizado em Python!"
    TASK_COMPLETED: Final[str] = "✅ Tarefa concluída! Você ganhou {xp} XP!"
    PHASE_UNLOCKED: Final[str] = "🔓 Nova fase desbloqueada: {phase}!"
