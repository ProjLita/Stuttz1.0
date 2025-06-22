"""
TELA DE DETALHES DA FASE
Mostra informações detalhadas e quiz de uma fase
"""

import flet as ft
from config import Config, Messages

class PhaseDetailView:
    """
    Classe que constrói a tela de detalhes da fase
    """
    
    def __init__(self, controller, phase_id: int):
        self.controller = controller
        self.phase_id = phase_id
        self.phase_data = self.controller.get_phase_by_id(phase_id)
        # Adicionar referência ao container de dica de estudo
        self.study_tip_container = None
        self.study_tip_text = None
        # Adicionar referência ao container de explicação do quiz
        self.ai_explanation_container = None
        self.ai_explanation_text = None
        # Adicionar referências para o feedback
        self.feedback_container = None
        self.feedback_text = None
        self.explanation_button = None
        # Adicionar lista para armazenar referências aos containers das opções
        self.option_containers = []
    
    def build(self) -> ft.Control:
        """
        Constrói toda a interface de detalhes
        """
        if not self.phase_data:
            return ft.Text("❌ Fase não encontrada")
        
        return ft.Column([
            self.build_back_button(),
            self.build_phase_header(),
            ft.Divider(color="#D4B896"),
            self.build_tasks_section(),
            ft.Divider(color="#D4B896"),
            self.build_quiz_section()
        ], scroll=ft.ScrollMode.AUTO, spacing=15)
    
    def build_back_button(self) -> ft.Control:
        """
        Botão para voltar ao mapa
        """
        return ft.Container(
            content=ft.TextButton(
                content=ft.Row([
                    ft.Text("◀️", size=16),  # Emoji de seta para trás
                    ft.Text(
                        "Voltar ao Mapa", 
                        color=Config.COLORS['primary_blue'], 
                        size=14,
                        font_family=Config.INTERFACE_FONT,
                        weight=ft.FontWeight.BOLD
                    )
                ], spacing=5),
                on_click=lambda e: self.controller.handle_back_to_roadmap()
            ),
            alignment=ft.alignment.center_left
        )
    
    def build_phase_header(self) -> ft.Control:
        """
        Cabeçalho da fase com título e descrição
        """
        # Criar o texto para a dica de estudo
        self.study_tip_text = ft.Text(
            "",
            size=16,
            color=Config.COLORS['text_dark'],
            italic=True,
            font_family=Config.TEXT_FONT
        )
        
        # Criar o container para dica de estudo
        self.study_tip_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "💡 Dica de Estudo:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=Config.COLORS['accent_gold'],
                    font_family=Config.INTERFACE_FONT
                ),
                self.study_tip_text
            ], spacing=5),
            bgcolor="#F0F7FF",
            padding=15,
            border_radius=8,
            border=ft.border.all(2, "#D4B896")
        )
        
        return ft.Column([
            ft.Text(
                f"Fase {self.phase_id}: {self.phase_data['title']}",
                size=Config.FONT_SIZE_TITLE,
                weight=ft.FontWeight.BOLD,
                color=Config.COLORS['text_dark'],
                font_family=Config.TITLE_FONT
            ),
            ft.Text(
                self.phase_data['description'],
                size=Config.FONT_SIZE_BODY,
                color=Config.COLORS['accent_gold'],
                font_family=Config.TEXT_FONT
            ),
            # Botão para gerar dica de estudo
            ft.Container(
                content=ft.ElevatedButton(
                    "💡 Mostrar Dica de Estudo",
                    on_click=lambda e: self.show_study_tip(),
                    bgcolor=Config.COLORS['accent_gold'],
                    color=Config.COLORS['text_dark'],
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(15),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
                margin=ft.margin.only(top=15),
                alignment=ft.alignment.center
            ),
            # Container para exibir a dica (agora referenciado como self.study_tip_container)
            self.study_tip_container
        ], spacing=5)

    def show_study_tip(self):
        """
        Exibe uma dica de estudo gerada por IA
        """
        # Mostrar loading
        self.controller.show_message("⏳ Gerando dica de estudo...")
        
        # Gerar dica
        topic = self.phase_data['title']
        
        if 'tasks' in self.phase_data and len(self.phase_data['tasks']) > 0:
            # Usar a primeira tarefa como tópico específico
            specific_topic = self.phase_data['tasks'][0]
        else:
            specific_topic = "Python"
        
        # Tentar gerar a dica com a API
        tip = self.controller.generate_study_tip(topic, specific_topic)
        
        # Verificar se a dica contém mensagem de erro de API
        if "não está configurada" in tip.lower():
            # Usar dicas estáticas se a API não estiver disponível
            if topic == "Fundamentos":
                tip = "Pratique escrevendo pequenos programas Python todos os dias. Comece com scripts simples que usam print() e variáveis básicas."
            elif topic == "Estruturas de Dados":
                tip = "Experimente criar diferentes tipos de listas e dicionários. Tente converter entre eles para entender suas diferenças e semelhanças."
            else:
                tip = "Divida seu aprendizado em pequenas sessões diárias. Consistência é mais importante que sessões longas e esporádicas."
        
        print(f"Dica gerada: {tip}")
        
        # Atualizar o container de dica diretamente
        if self.study_tip_text and self.study_tip_container:
            self.study_tip_text.value = tip
            self.study_tip_container.visible = True
            print("✅ Container de dica atualizado")
            
            # Forçar atualização da interface
            self.controller.page.update()
        else:
            print("❌ Container de dica não encontrado")
    
    def build_tasks_section(self) -> ft.Control:
        """
        Seção com lista de tarefas
        """
        task_items = []
        
        for i, task in enumerate(self.phase_data['tasks'], 1):
            is_completed = self.phase_data['status'] == 'completed'
            
            task_item = ft.Container(
                content=ft.Row([
                    # Usando emojis em vez de ícones
                    ft.Text(
                        "✓" if is_completed else "○",
                        color=Config.COLORS['success_green'] if is_completed else Config.COLORS['locked'],
                        size=20
                    ),
                    ft.Text(
                        f"{i}. {task}",
                        size=Config.FONT_SIZE_BODY,
                        color=Config.COLORS['text_dark'],
                        expand=True,
                        font_family=Config.TEXT_FONT
                    )
                ], spacing=10),
                padding=ft.padding.symmetric(vertical=5)
            )
            task_items.append(task_item)
        
        return ft.Column([
            ft.Text(
                "📋 Tarefas desta Fase",
                size=Config.FONT_SIZE_SUBTITLE,
                weight=ft.FontWeight.BOLD,
                color=Config.COLORS['text_dark'],
                font_family=Config.TITLE_FONT
            ),
            ft.Column(task_items, spacing=5)
        ], spacing=10)
    
    def build_quiz_section(self) -> ft.Control:
        """
        Seção com quiz da fase
        """
        # Verificar se a fase tem quiz
        if not self.phase_data.get('quiz'):
            return ft.Container()  # Retorna container vazio se não tiver quiz
        
        quiz = self.phase_data['quiz']
        
        # Criar container para explicação da IA
        self.ai_explanation_text = ft.Text(
            "",
            size=16,
            color=Config.COLORS['text_dark'],
            font_family=Config.TEXT_FONT
        )
        
        self.ai_explanation_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "🤖 Explicação:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=Config.COLORS['primary_blue'],
                    font_family=Config.INTERFACE_FONT
                ),
                self.ai_explanation_text
            ]),
            bgcolor="#F0F7FF",
            padding=15,
            border_radius=8,
            border=ft.border.all(2, "#D4B896"),
            visible=False  # Inicialmente invisível
        )
        
        # Construir a seção de quiz
        return ft.Column([
            # Título da seção
            ft.Text(
                "🧠 Quiz da Fase",
                size=Config.FONT_SIZE_SUBTITLE,
                weight=ft.FontWeight.BOLD,
                color=Config.COLORS['text_dark'],
                font_family=Config.TITLE_FONT
            ),
            
            # Pergunta do quiz
            ft.Container(
                content=ft.Text(
                    quiz['question'],
                    size=Config.FONT_SIZE_BODY,
                    color=Config.COLORS['text_dark'],
                    font_family=Config.TEXT_FONT
                ),
                margin=ft.margin.symmetric(vertical=10)
            ),
            
            # Opções do quiz
            self.build_quiz_options(quiz),
            
            # Botão para confirmar resposta
            self.build_quiz_button(),
            
            # Feedback da resposta
            self.build_quiz_feedback(),
            
            # Container para explicação da IA
            self.ai_explanation_container
        ], spacing=10)
    
    def build_quiz_options(self, quiz) -> ft.Control:
        """
        Constrói as opções do quiz
        """
        options_list = []
        self.option_containers = []  # Limpar lista de containers
        
        for i, option in enumerate(quiz['options']):
            # Criar container para cada opção
            option_container = ft.Container(
                content=ft.Row([
                    ft.Text(
                        chr(65 + i),  # A, B, C, D...
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=Config.COLORS['primary_blue'],
                        font_family=Config.INTERFACE_FONT
                    ),
                    ft.Text(
                        option,
                        size=Config.FONT_SIZE_BODY,
                        color=Config.COLORS['text_dark'],
                        font_family=Config.TEXT_FONT
                    )
                ], spacing=10),
                padding=10,
                border_radius=5,
                border=ft.border.all(2, "#DDDDDD"),
                margin=ft.margin.only(bottom=8),
                ink=True,  # Efeito de tinta ao clicar
                on_click=lambda e, idx=i: self.handle_option_click(idx)
            )
            options_list.append(option_container)
            self.option_containers.append(option_container)  # Armazenar referência
        
        return ft.Column(options_list)
    
    def build_quiz_button(self) -> ft.Control:
        """
        Botão para confirmar resposta do quiz
        """
        return ft.Container(
            content=ft.ElevatedButton(
                "Confirmar Resposta",
                on_click=self.handle_quiz_submit,
                bgcolor=Config.COLORS['primary_blue'],
                color=Config.COLORS['text_light'],
                style=ft.ButtonStyle(
                    padding=ft.padding.all(15),
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            margin=ft.margin.symmetric(vertical=15),
            alignment=ft.alignment.center
        )
    
    def build_quiz_feedback(self) -> ft.Control:
        """
        Feedback para a resposta do quiz
        """
        # Criar texto para feedback
        feedback_text = ft.Text(
            "",  # Texto será definido dinamicamente
            size=16,
            weight=ft.FontWeight.BOLD,
            font_family=Config.INTERFACE_FONT
        )
        
        # Criar botão para explicação
        explanation_button = ft.Container(
            content=ft.ElevatedButton(
                "🤖 Gerar Explicação",
                on_click=lambda e: self.generate_ai_explanation(),
                bgcolor=Config.COLORS['secondary_blue'],
                color=Config.COLORS['text_light'],
                style=ft.ButtonStyle(
                    padding=ft.padding.all(12),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
            margin=ft.margin.only(top=10),
            alignment=ft.alignment.center,
            visible=False  # Inicialmente invisível
        )
        
        # Container para feedback (inicialmente invisível)
        feedback_container = ft.Container(
            content=ft.Column([
                feedback_text,
                explanation_button
            ]),
            bgcolor="#F0F7FF",
            padding=15,
            border_radius=8,
            border=ft.border.all(2, "#D4B896"),
            visible=False  # Inicialmente invisível
        )
        
        # Armazenar referência ao container e seus componentes
        self.feedback_container = feedback_container
        self.feedback_text = feedback_text
        self.explanation_button = explanation_button
        
        return feedback_container
    
    def generate_ai_explanation(self):
        """
        Gera uma explicação para a resposta do quiz usando IA
        """
        # Mostrar loading
        self.controller.show_message("⏳ Gerando explicação...")
        
        # Obter dados do quiz
        quiz = self.phase_data['quiz']
        question = quiz['question']
        correct_answer = quiz['options'][quiz['correct_answer_index']]
        
        # Tentar gerar explicação com a API
        explanation = self.controller.generate_explanation(question, correct_answer)
        
        # Verificar se a explicação contém mensagem de erro de API
        if "não está configurada" in explanation.lower():
            # Usar explicações estáticas se a API não estiver disponível
            explanation = f"A resposta correta é '{correct_answer}'. Esta é a opção que melhor responde à pergunta, considerando os conceitos abordados nesta fase do curso."
        
        # Atualizar o container de explicação
        if self.ai_explanation_text and self.ai_explanation_container:
            self.ai_explanation_text.value = explanation
            self.ai_explanation_container.visible = True
            
            # Forçar atualização da interface
            self.controller.page.update()
    
    def handle_option_click(self, option_index: int):
        """
        Manipula o clique em uma opção do quiz
        """
        # Armazenar a opção selecionada
        self.controller.selected_option = option_index
        print(f"Opção selecionada: {option_index}")
        
        # Atualizar o estilo visual das opções
        for i, container in enumerate(self.option_containers):
            if i == option_index:
                # Destacar a opção selecionada
                container.border = ft.border.all(2, Config.COLORS['primary_blue'])
                container.bgcolor = "#E3F2FD"  # Fundo azul claro
            else:
                # Restaurar estilo padrão das outras opções
                container.border = ft.border.all(2, "#DDDDDD")
                container.bgcolor = None
        
        # Atualizar a interface
        self.controller.page.update()
    
    def handle_quiz_submit(self, e):
        """
        Manipula o envio da resposta do quiz
        """
        # Verificar se há uma opção selecionada
        if self.controller.selected_option is None:
            self.controller.show_message(Messages.NO_ANSWER_SELECTED)
            return
        
        # Obter o índice da resposta correta
        correct_index = self.phase_data['quiz']['correct_answer_index']
        selected_index = self.controller.selected_option
        
        # Verificar se a resposta está correta
        is_correct = selected_index == correct_index
        
        # Preparar feedback
        if is_correct:
            # Resposta correta
            if self.feedback_text:
                self.feedback_text.value = Messages.QUIZ_CORRECT.format(xp=Config.XP_PER_CORRECT_ANSWER)
                self.feedback_text.color = Config.COLORS['success_green']
            if self.feedback_container:
                self.feedback_container.border = ft.border.all(2, Config.COLORS['success_green'])
            
            # Conceder XP
            self.award_xp_for_correct_answer()
            
            # Verificar se deve desbloquear a próxima fase
            self.check_and_unlock_next_phase()
        else:
            # Resposta incorreta
            correct_option = self.phase_data['quiz']['options'][correct_index]
            if self.feedback_text:
                self.feedback_text.value = Messages.QUIZ_INCORRECT.format(correct=correct_option)
                self.feedback_text.color = Config.COLORS['error_red']
            if self.feedback_container:
                self.feedback_container.border = ft.border.all(2, Config.COLORS['error_red'])
        
        # Exibir feedback e botão de explicação
        if self.feedback_container:
            self.feedback_container.visible = True
        if self.explanation_button:
            self.explanation_button.visible = True
        # Atualizar interface
        self.controller.page.update()
    
    def award_xp_for_correct_answer(self):
        """
        Concede XP ao usuário por resposta correta
        """
        # Verificar se o quiz já foi respondido corretamente antes
        if self.phase_data.get('quiz_completed', False):
            print("Quiz já foi completado anteriormente. Nenhum XP concedido.")
            return
        
        # Marcar o quiz como completado
        self.phase_data['quiz_completed'] = True
        
        # Adicionar XP
        xp_gained = Config.XP_PER_CORRECT_ANSWER
        user = self.controller.user_data
        
        # Atualizar XP do usuário
        user["xp"] += xp_gained
        
        # Verificar se subiu de nível
        if user["xp"] >= user["xp_to_next"]:
            # Subir de nível
            user["level"] += 1
            # Calcular XP excedente
            excess_xp = user["xp"] - user["xp_to_next"]
            # Definir novo limite de XP
            user["xp_to_next"] = Config.XP_PER_LEVEL * user["level"]
            # Definir XP atual como o excedente
            user["xp"] = excess_xp
            
            # Mostrar mensagem de level up
            self.controller.show_message(Messages.LEVEL_UP.format(level=user["level"]))
        
        # Salvar dados do usuário
        self.controller.save_user_data()
        
        print(f"✅ {xp_gained} XP concedidos ao usuário!")
    
    def check_and_unlock_next_phase(self):
        """
        Verifica se deve desbloquear a próxima fase
        """
        # Marcar a fase atual como completada
        self.phase_data['status'] = 'completed'
        
        # Obter todas as fases
        phases = self.controller.roadmap_data['phases']
        
        # Encontrar a fase atual
        current_phase_index = -1
        for i, phase in enumerate(phases):
            if phase['id'] == self.phase_id:
                current_phase_index = i
                break
        
        # Se encontrou a fase atual e não é a última
        if current_phase_index >= 0 and current_phase_index < len(phases) - 1:
            # Obter a próxima fase
            next_phase = phases[current_phase_index + 1]
            
            # Se a próxima fase estiver bloqueada, desbloqueá-la
            if next_phase['status'] == 'locked':
                next_phase['status'] = 'unlocked'
                
                # Mostrar mensagem de fase desbloqueada
                self.controller.show_message(
                    Messages.PHASE_UNLOCKED.format(phase=next_phase['title'])
                )
                
                print(f"✅ Fase {next_phase['id']} desbloqueada!")
        
        # Salvar dados do roadmap
        self.controller.save_roadmap_data()
