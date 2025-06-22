"""
CONTROLADOR PRINCIPAL DO STUTTZ
Este arquivo gerencia todo o funcionamento do app, seguindo o padrão MVC (Model-View-Controller)
"""

import flet as ft  # Biblioteca para construção da interface gráfica
import json  # Módulo para manipulação de dados JSON
import os  # Módulo para interagir com o sistema operacional
from datetime import datetime  # Classe para manipulação de datas e horários
from typing import Optional, Dict, Any, List, cast  # Tipos para anotações de tipo
from config import Config, Messages  # Importa configurações e mensagens do sistema
from utils.ai_helper import get_gemini_response  # Importa função para comunicação com a API Gemini

class AppController:
    """
    Classe principal que controla todo o aplicativo
    
    Responsável por:
    - Gerenciar o estado da aplicação
    - Carregar e salvar dados do usuário
    - Controlar a navegação entre telas
    - Processar interações do usuário
    - Coordenar a comunicação com a IA
    """
    
    def __init__(self, page: ft.Page):
        """
        Inicializa o controlador com a página principal e carrega os dados necessários
        
        Args:
            page: Objeto Page do Flet que representa a janela principal do aplicativo
        """
        self.page = page  # Armazena referência à página principal do Flet
        
        # === ESTADOS DO APP ===
        self.current_view = "roadmap"  # Define a tela inicial como o roadmap
        self.active_phase_id: Optional[int] = None  # ID da fase ativa (None quando estiver no roadmap)
        
        # === ESTADO DO QUIZ ===
        # Dicionário que armazena o estado atual do quiz
        self.quiz_state = {
            "selected_answer": None,  # Índice da resposta selecionada pelo usuário
            "answered": False,  # Indica se o quiz já foi respondido
            "correct_answer": None  # Índice da resposta correta
        }
        # Variável para armazenar a opção selecionada no quiz atual
        self.selected_option = None
        
        # === CACHE DE DICAS E EXPLICAÇÕES ===
        # Armazena dicas já geradas para evitar chamadas repetidas à API
        self.study_tips_cache = {}  # Formato: {f"{phase_title}:{topic}": "dica gerada"}
        self.explanations_cache = {}  # Formato: {f"{question}:{answer}": "explicação gerada"}
        
        # === CARREGAR DADOS ===
        # Carrega os dados do usuário e do roadmap ao inicializar
        self.user_data = self.load_user_data()  # Dados do usuário (progresso, nível, etc.)
        self.roadmap_data = self.load_roadmap_data()  # Dados do roadmap (fases, quizzes, etc.)
        
        print("✅ Controlador inicializado com sucesso!")
    
    def load_user_data(self) -> Dict[str, Any]:
        """
        Carrega dados do usuário do arquivo JSON ou cria novos dados padrão
        
        Returns:
            Dicionário com os dados do usuário (nome, nível, XP, etc.)
        """
        # Tentar carregar dados salvos do arquivo user_data.json
        if os.path.exists("user_data.json"):
            try:
                # Abre o arquivo e carrega os dados JSON
                with open("user_data.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                # Erro específico para problemas de formatação JSON
                print(f"❌ Erro ao decodificar JSON: {e}")
            except PermissionError as e:
                # Erro específico para problemas de permissão de arquivo
                print(f"❌ Erro de permissão ao acessar o arquivo: {e}")
            except Exception as e:
                # Captura outros erros inesperados
                print(f"❌ Erro inesperado ao carregar dados do usuário: {e}")
        
        # Criar dados padrão se o arquivo não existir ou ocorrer erro na leitura
        print("ℹ️ Criando dados padrão do usuário")
        return {
            "name": "Estudante",  # Nome padrão do usuário
            "level": 1,  # Nível inicial
            "xp": 0,  # Experiência inicial
            "xp_to_next": Config.XP_PER_LEVEL,  # XP necessário para o próximo nível
            "streak": 0,  # Dias consecutivos de estudo
            "last_activity": None,  # Data da última atividade
            "completed_phases": []  # Lista de IDs das fases completadas
        }
    
    def load_roadmap_data(self) -> Dict[str, Any]:
        """
        Carrega dados do roadmap (para protótipo, usa dados fixos)
        
        Returns:
            Dicionário com os dados do roadmap (nome do curso, fases, etc.)
        """
        # Nesta versão do protótipo, os dados são definidos diretamente no código
        # Em uma versão completa, poderiam ser carregados de um arquivo ou banco de dados
        return {
            "course_name": "Python para Iniciantes",  # Nome do curso
            "total_phases": 5,  # Número total de fases
            "phases": [
                {
                    "id": 1,  # Identificador único da fase
                    "title": "Fundamentos",  # Título da fase
                    "description": "Aprenda os conceitos básicos do Python",  # Descrição da fase
                    "status": "unlocked",  # Estado inicial: desbloqueada (primeira fase)
                    "tasks": [  # Lista de tarefas da fase
                        "Instalar Python e configurar ambiente",
                        "Entender variáveis e tipos de dados",
                        "Criar seu primeiro programa"
                    ],
                    "quiz": {  # Quiz associado à fase
                        "question": "Qual comando exibe texto na tela em Python?",  # Pergunta
                        "options": ["show()", "print()", "display()", "output()"],  # Opções
                        "correct_answer_index": 1,  # Índice (0-based) da resposta correta
                        "explanation": "print() é a função padrão para exibir texto na tela."  # Explicação
                    }
                },
                {
                    "id": 2,
                    "title": "Estruturas de Dados",
                    "description": "Trabalhe com listas, tuplas e dicionários",
                    "status": "locked",  # Estado inicial: bloqueada (será desbloqueada após completar a fase 1)
                    "tasks": [
                        "Criar e manipular listas",
                        "Entender tuplas e suas características", 
                        "Trabalhar com dicionários"
                    ],
                    "quiz": {
                        "question": "Como criar uma lista vazia em Python?",
                        "options": ["list()", "[]", "new list()", "empty()"],
                        "correct_answer_index": 1,
                        "explanation": "[] é a sintaxe mais comum e simples."
                    }
                },
                # Adicione mais fases conforme necessário
            ]
        }
    
    def get_current_view(self) -> ft.Control:
        """
        Retorna a tela atual baseada no estado do controlador
        
        Este método é responsável por instanciar a view correta com base no valor
        de self.current_view, permitindo a navegação entre diferentes telas
        
        Returns:
            Componente Flet que representa a tela atual
        """
        if self.current_view == "roadmap":
            # Carrega a view do roadmap (mapa de fases)
            from views.roadmap_view import RoadmapView
            return RoadmapView(self).build()
        elif self.current_view == "phase_detail":
            # Carrega a view de detalhes da fase
            from views.phase_detail_view import PhaseDetailView
            # Garantir que temos um ID de fase válido antes de instanciar a view
            if self.active_phase_id is not None:
                return PhaseDetailView(self, self.active_phase_id).build()
            else:
                # Caso não tenha uma fase ativa, exibe mensagem de erro
                return ft.Text("Erro: ID de fase inválido")
        else:
            # Caso o nome da view não seja reconhecido
            return ft.Text("Erro: Tela não encontrada")
    
    def handle_phase_click(self, phase_id: int):
        """
        Gerencia quando o usuário clica em uma fase no roadmap
        
        Verifica se a fase está desbloqueada e, se estiver, navega para ela
        
        Args:
            phase_id: ID da fase clicada
        """
        print(f"🖱️ Clique na fase {phase_id}")
        
        # Encontrar a fase pelo ID
        phase = self.get_phase_by_id(phase_id)
        if not phase:
            print("Fase não encontrada!")
            return
        
        # Verificar se a fase está desbloqueada
        if phase["status"] == "locked":
            print("🔒 Fase bloqueada!")
            self.show_message("Esta fase ainda está bloqueada. Complete as fases anteriores primeiro.")
            return
        
        # Navegar para a fase (atualiza o estado e a interface)
        self.active_phase_id = phase_id  # Define a fase ativa
        self.current_view = "phase_detail"  # Muda para a view de detalhes
        self.reset_quiz_state()  # Reseta o estado do quiz
        self.update_view()  # Atualiza a interface
    
    def handle_back_to_roadmap(self):
        """
        Volta para o mapa principal (roadmap)
        
        Este método é chamado quando o usuário clica no botão "Voltar"
        """
        print("⬅️ Voltando ao mapa")
        self.active_phase_id = None  # Remove a fase ativa
        self.current_view = "roadmap"  # Muda para a view do roadmap
        self.reset_quiz_state()  # Reseta o estado do quiz
        self.update_view()  # Atualiza a interface
    
    def reset_quiz_state(self):
        """
        Reseta o estado do quiz para o estado inicial
        
        Chamado ao navegar entre telas para garantir que o quiz
        comece no estado correto
        """
        self.quiz_state = {
            "selected_answer": None,  # Remove a resposta selecionada
            "answered": False,  # Define como não respondido
            "correct_answer": None  # Remove a resposta correta
        }
        self.selected_option = None  # Reseta a opção selecionada
    
    def update_view(self):
        """
        Atualiza a interface para refletir o estado atual
        
        Este método é responsável por reconstruir a interface quando
        o estado do aplicativo muda
        """
        try:
            # Verifica se a página tem o container principal
            if not hasattr(self.page, 'controls') or not self.page.controls:
                print("Estrutura de controles não encontrada para atualizar!")
                return
                
            # Obtém o container principal (primeiro controle)
            if len(self.page.controls) == 0:
                print("A página não possui controles para atualizar")
                return
                
            container = self.page.controls[0]
            
            # Verifica se o controle é um Container
            if not isinstance(container, ft.Container):
                print(f"O controle principal não é um Container, é um {type(container).__name__}")
                return
                
            # Atualiza o conteúdo do container com a nova view
            container.content = self.get_current_view()
            
            # Registra informações sobre a atualização
            print(f"Atualizando para a view: {self.current_view}")
            if self.current_view == "phase_detail":
                print(f"Mostrando fase {self.active_phase_id}")
                
            # Atualiza a página para refletir as mudanças
            self.page.update()
            
        except Exception as e:
            # Captura qualquer erro durante a atualização
            print(f"Erro ao atualizar view: {e}")
    
    def get_phase_by_id(self, phase_id: int) -> Optional[Dict[str, Any]]:
        """
        Encontra uma fase pelo ID
        
        Args:
            phase_id: ID da fase a ser encontrada
            
        Returns:
            Dicionário com os dados da fase ou None se não encontrada
        """
        # Validar o tipo do ID
        if not isinstance(phase_id, int):
            print(f"❌ ID de fase inválido: {phase_id} não é um número inteiro")
            return None
            
        # Validar se o ID é positivo
        if phase_id <= 0:
            print(f"❌ ID de fase inválido: {phase_id} deve ser maior que zero")
            return None
            
        # Percorre todas as fases procurando pelo ID especificado
        for phase in self.roadmap_data["phases"]:
            if phase["id"] == phase_id:
                return phase
                
        # Fase não encontrada
        print(f"❌ Fase com ID {phase_id} não encontrada")
        return None
    
    def show_message(self, message: str):
        """
        Mostra uma mensagem para o usuário
        
        Exibe uma mensagem no console e, quando possível, 
        prepara a interface para exibir alertas em implementações futuras
        
        Args:
            message: Texto da mensagem a ser exibida
        """
        # Exibe no console para debug
        print(f"💬 {message}")
        
        # Em uma implementação futura, poderia exibir na interface gráfica
        # Por enquanto, apenas registra a mensagem
    
    def save_user_data(self):
        """
        Salva dados do usuário no arquivo JSON
        
        Persiste os dados do usuário para que possam ser
        recuperados em sessões futuras
        
        Returns:
            bool: True se os dados foram salvos com sucesso, False caso contrário
        """
        try:
            # Salva os dados no arquivo user_data.json
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=2, ensure_ascii=False)
            print("💾 Dados salvos com sucesso!")
            return True
        except PermissionError as e:
            # Erro específico para problemas de permissão de arquivo
            print(f"❌ Erro de permissão ao salvar dados: {e}")
            return False
        except IOError as e:
            # Erro específico para problemas de entrada/saída
            print(f"❌ Erro de I/O ao salvar dados: {e}")
            return False
        except Exception as e:
            # Captura outros erros inesperados
            print(f"❌ Erro inesperado ao salvar dados: {e}")
            return False

    def save_roadmap_data(self):
        """
        Salva dados do roadmap no arquivo JSON
        
        Persiste os dados do roadmap para que possam ser
        recuperados em sessões futuras
        
        Returns:
            bool: True se os dados foram salvos com sucesso, False caso contrário
        """
        try:
            # Salva os dados no arquivo roadmap_data.json
            with open(Config.DEFAULT_ROADMAP_FILE, "w", encoding="utf-8") as f:
                json.dump(self.roadmap_data, f, indent=2, ensure_ascii=False)
            print("💾 Dados do roadmap salvos com sucesso!")
            return True
        except PermissionError as e:
            # Erro específico para problemas de permissão de arquivo
            print(f"❌ Erro de permissão ao salvar dados do roadmap: {e}")
            return False
        except IOError as e:
            # Erro específico para problemas de entrada/saída
            print(f"❌ Erro de I/O ao salvar dados do roadmap: {e}")
            return False
        except Exception as e:
            # Captura outros erros inesperados
            print(f"❌ Erro inesperado ao salvar dados do roadmap: {e}")
            return False

    # Métodos relacionados à integração com IA

    def get_personalized_explanation(self, question: str, correct_answer: str) -> str:
        """
        Obtém uma explicação personalizada para uma resposta de quiz usando IA
        
        Utiliza a API do Gemini para gerar uma explicação didática sobre
        a pergunta e resposta correta do quiz. Implementa um sistema de cache
        para evitar chamadas repetidas à API para a mesma pergunta/resposta.
        
        Args:
            question: A pergunta do quiz
            correct_answer: A resposta correta do quiz
            
        Returns:
            Uma explicação didática gerada pela IA
        """
        # Criar chave de cache
        cache_key = f"{question}:{correct_answer}"
        
        # Verificar se já existe no cache
        if cache_key in self.explanations_cache:
            print(f"✅ Usando explicação em cache para '{question}'")
            return self.explanations_cache[cache_key]
            
        # Constrói o prompt para a IA com instruções específicas
        prompt = f"""
        Explique a seguinte pergunta e resposta de forma didática para um estudante:
        
        Pergunta: {question}
        Resposta correta: {correct_answer}
        
        Explicação (máximo 3 parágrafos, linguagem acessível):
        """
        
        # Envia o prompt para a API do Gemini e retorna a resposta
        explanation = get_gemini_response(prompt, max_tokens=300)
        
        # Armazenar no cache
        self.explanations_cache[cache_key] = explanation
        
        return explanation

    # Método de alias para manter compatibilidade
    def generate_explanation(self, question: str, correct_answer: str) -> str:
        """
        Alias para get_personalized_explanation para manter compatibilidade
        
        Args:
            question: A pergunta do quiz
            correct_answer: A resposta correta do quiz
            
        Returns:
            Uma explicação didática gerada pela IA
        """
        return self.get_personalized_explanation(question, correct_answer)

    def generate_study_tip(self, phase_title: str, topic: str) -> str:
        """
        Gera uma dica de estudo personalizada usando IA
        
        Utiliza a API do Gemini para criar uma dica de estudo
        relevante para o tópico específico que o usuário está estudando.
        Implementa um sistema de cache para evitar chamadas repetidas à API
        para o mesmo tópico.
        
        Args:
            phase_title: Título da fase atual (ex: "Fundamentos")
            topic: Tópico específico dentro da fase (ex: "Instalar Python")
            
        Returns:
            Uma dica de estudo curta e prática gerada pela IA
        """
        # Criar chave de cache
        cache_key = f"{phase_title}:{topic}"
        
        # Verificar se já existe no cache
        if cache_key in self.study_tips_cache:
            print(f"✅ Usando dica em cache para '{cache_key}'")
            return self.study_tips_cache[cache_key]
        
        # Constrói o prompt para a IA com instruções específicas
        prompt = f"""
        Por favor, forneça uma dica de estudo prática e curta para alguém 
        estudando '{phase_title}', especificamente sobre '{topic}'.
        
        A dica deve ter no máximo 2 frases e fornecer uma sugestão 
        concreta e útil para melhorar o aprendizado.
        """
        
        # Envia o prompt para a API do Gemini e retorna a resposta
        tip = get_gemini_response(prompt, max_tokens=150)
        
        # Armazenar no cache
        self.study_tips_cache[cache_key] = tip
        
        return tip

    def suggest_next_steps(self) -> str:
        """
        Sugere próximos passos baseado no progresso do usuário usando IA
        
        Analisa as fases completadas e atuais do usuário para gerar
        uma recomendação personalizada de recursos adicionais
        
        Returns:
            Uma sugestão de próximos passos gerada pela IA
        """
        # Identificar fases completas e atuais
        completed_phases = [p for p in self.roadmap_data["phases"] 
                            if p["id"] in self.user_data["completed_phases"]]
        current_phases = [p for p in self.roadmap_data["phases"] 
                        if p["status"] == "unlocked" and p["id"] not in self.user_data["completed_phases"]]
        
        # Obter títulos das fases para incluir no prompt
        completed_titles = [p["title"] for p in completed_phases]
        current_titles = [p["title"] for p in current_phases]
        
        # Construir prompt com o contexto do progresso do usuário
        prompt = f"""
        Um estudante de programação está aprendendo Python.
        
        Tópicos já concluídos: {', '.join(completed_titles) if completed_titles else 'Nenhum'}
        Tópicos atuais: {', '.join(current_titles) if current_titles else 'Introdução ao Python'}
        
        Forneça uma sugestão breve (máximo 3 frases) de que recurso adicional o estudante 
        pode consultar para melhorar seu aprendizado nos tópicos atuais.
        """
        
        # Envia o prompt para a API do Gemini e retorna a resposta
        return get_gemini_response(prompt, max_tokens=200)

    def update_streak(self):
        """
        Atualiza o streak (dias consecutivos) do usuário
        
        Verifica a data da última atividade e atualiza o streak
        de acordo com as seguintes regras:
        - Se for o primeiro acesso, inicia o streak em 1
        - Se o último acesso foi no dia anterior, aumenta o streak
        - Se o último acesso foi no mesmo dia, mantém o streak
        - Se o último acesso foi há mais de um dia, reseta o streak
        
        Returns:
            bool: True se o streak foi aumentado, False caso contrário
        """
        from datetime import datetime, timedelta
        
        # Obter data atual
        today = datetime.now().date()
        
        # Obter data da última atividade
        last_activity = self.user_data["last_activity"]
        
        # Converter para objeto date se não for None
        if last_activity:
            try:
                last_activity = datetime.fromisoformat(last_activity).date()
            except (ValueError, TypeError):
                # Se a data estiver em formato inválido, considerar como None
                last_activity = None
        
        # Atualizar data da última atividade
        self.user_data["last_activity"] = today.isoformat()
        
        # Caso seja o primeiro acesso
        if last_activity is None:
            self.user_data["streak"] = 1
            self.save_user_data()
            return True
            
        # Calcular diferença de dias
        days_diff = (today - last_activity).days
        
        # Mesmo dia: manter streak
        if days_diff == 0:
            return False
            
        # Dia seguinte: aumentar streak
        elif days_diff == 1:
            self.user_data["streak"] += 1
            self.save_user_data()
            return True
            
        # Mais de um dia: resetar streak
        else:
            self.user_data["streak"] = 1
            self.save_user_data()
            return False
