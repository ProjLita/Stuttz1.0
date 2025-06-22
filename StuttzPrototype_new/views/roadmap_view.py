"""
TELA DO MAPA DE FASES
Mostra o roadmap visual com todas as fases do curso
Implementa a visualização principal do aplicativo
"""

import flet as ft  # Biblioteca para construção da interface gráfica
import math  # Módulo para operações matemáticas
from typing import List, Tuple  # Tipos para anotações de tipo
from config import Config  # Importa configurações globais do aplicativo

class RoadmapView:
    """
    Classe que constrói a tela do mapa de fases
    
    Esta view é responsável por exibir:
    - Informações do curso
    - Cartão do usuário com nível e progresso
    - Lista de fases do roadmap com seus status
    """
    
    def __init__(self, controller):
        """
        Inicializa a view com uma referência ao controlador
        
        Args:
            controller: Instância do AppController que gerencia o estado do app
        """
        self.controller = controller  # Armazena referência ao controlador
    
    def build(self) -> ft.Control:
        """
        Constrói toda a interface do roadmap
        
        Organiza todos os componentes em uma coluna vertical com rolagem
        
        Returns:
            Componente Flet que representa a tela completa do roadmap
        """
        return ft.Column([
            self.build_header(),  # Cabeçalho com o nome do curso
            self.build_user_card(),  # Cartão com informações do usuário
            ft.Container(height=20),  # Espaçamento vertical
            self.build_roadmap_display(),  # Lista de fases do roadmap
        ], scroll=ft.ScrollMode.AUTO)  # Permite rolagem quando o conteúdo excede a tela
    
    def build_header(self) -> ft.Control:
        """
        Cabeçalho com o nome do curso
        
        Returns:
            Container com o título do curso centralizado
        """
        return ft.Container(
            content=ft.Text(
                self.controller.roadmap_data["course_name"],  # Nome do curso obtido dos dados
                size=Config.FONT_SIZE_TITLE,  # Tamanho da fonte aumentado
                weight=ft.FontWeight.BOLD,  # Fonte em negrito
                color=Config.COLORS['text_dark'],  # Cor do texto definida nas configurações
                text_align=ft.TextAlign.CENTER,  # Alinhamento centralizado
                font_family=Config.TITLE_FONT  # Usar a fonte para títulos
            ),
            alignment=ft.alignment.center,  # Centraliza o texto no container
            padding=ft.padding.symmetric(vertical=15)  # Espaçamento vertical aumentado
        )
    
    def build_user_card(self) -> ft.Control:
        """
        Card com informações do usuário
        
        Exibe:
        - Nome e avatar do usuário
        - Nível e título
        - Streak (dias consecutivos)
        - Barra de progresso de XP
        
        Returns:
            Card com informações do usuário
        """
        user = self.controller.user_data  # Obtém dados do usuário do controlador
        
        # Calcular progresso XP como porcentagem (0 a 1)
        progress_percent = user["xp"] / user["xp_to_next"] if user["xp_to_next"] > 0 else 0
        
        # Obter título do nível das configurações
        level_title = Config.LEVEL_TITLES.get(user["level"], "Aprendiz")
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    # Avatar circular com as iniciais do usuário
                    ft.CircleAvatar(
                        content=ft.Text(
                            user["name"][:2].upper(),  # Primeiras duas letras do nome em maiúsculas
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        radius=25,  # Raio do círculo
                        bgcolor=Config.COLORS['accent_gold'],  # Cor de fundo do avatar
                        color=Config.COLORS['text_dark']  # Cor do texto
                    ),
                    # Coluna com informações do usuário
                    ft.Column([
                        # Nome do usuário
                        ft.Text(
                            user["name"], 
                            size=Config.FONT_SIZE_SUBTITLE, 
                            weight=ft.FontWeight.BOLD,
                            color=Config.COLORS['text_dark'],
                            font_family=Config.INTERFACE_FONT
                        ),
                        # Título baseado no nível
                        ft.Text(
                            f"✨ {level_title}",
                            size=Config.FONT_SIZE_BODY,
                            color=Config.COLORS['primary_blue'],
                            font_family=Config.TEXT_FONT
                        ),
                        # Streak (dias consecutivos)
                        ft.Row([
                            ft.Text("🔥", size=Config.FONT_SIZE_BODY),  # Emoji de fogo
                            ft.Text(
                                f"{user['streak']} dias",
                                size=Config.FONT_SIZE_BODY,
                                color=Config.COLORS['error_red'],
                                font_family=Config.TEXT_FONT
                            )
                        ], spacing=5),
                        # Barra de progresso de XP
                        ft.ProgressBar(
                            value=progress_percent,  # Valor entre 0 e 1
                            height=6,  # Altura da barra
                            bgcolor="#E6E6E6",  # Cor de fundo
                            color=Config.COLORS['primary_blue']  # Cor da barra de progresso
                        ),
                        # Texto com valores de XP
                        ft.Text(
                            f"XP: {user['xp']}/{user['xp_to_next']}",
                            size=10,
                            color=Config.COLORS['text_light'],
                            font_family=Config.TEXT_FONT
                        )
                    ], spacing=3, expand=True)  # Espaçamento entre elementos e expansão para preencher espaço
                ], spacing=15),  # Espaçamento entre avatar e informações
                padding=15  # Espaçamento interno do container
            ),
            elevation=3  # Sombra do card para efeito 3D
        )
    
    def handle_phase_button_click(self, e):
        """
        Manipula o clique em um botão de fase
        
        Este método é passado como callback para os botões de fase
        e encaminha o evento para o controlador
        
        Args:
            e: Evento de clique contendo dados do botão
        """
        # Obter o ID da fase a partir do data do evento
        phase_id = e.control.data  # O ID da fase foi armazenado na propriedade data do botão
        # Chamar o método do controlador para lidar com o clique
        print(f"Botão de fase clicado: {phase_id}")
        self.controller.handle_phase_click(phase_id)
    
    def build_roadmap_display(self) -> ft.Control:
        """
        Exibição do roadmap - versão simplificada textual
        
        Cria uma lista de botões representando as fases do roadmap,
        cada um com status visual diferente baseado no progresso
        
        Returns:
            Coluna com título e lista de fases do roadmap
        """
        phases_list = []  # Lista que armazenará os botões de fase
        
        # Itera sobre todas as fases no roadmap
        for phase in self.controller.roadmap_data["phases"]:
            # Determinar ícone baseado no status da fase
            status_icons = {
                "completed": "✅",  # Fase completada
                "unlocked": "🔵",  # Fase desbloqueada
                "current": "⭐",   # Fase atual
                "locked": "🔒"     # Fase bloqueada
            }
            
            # Obtém o ícone correspondente ao status ou usa "❓" como fallback
            icon = status_icons.get(phase["status"], "❓")
            
            # Determinar se o botão é clicável (apenas fases não bloqueadas)
            is_clickable = phase["status"] != "locked"
            
            # Criar botão da fase
            phase_button = ft.Container(
                content=ft.Row([
                    ft.Text(icon, size=20),  # Ícone de status
                    ft.Column([
                        # Título da fase
                        ft.Text(
                            f"Fase {phase['id']}: {phase['title']}",
                            size=Config.FONT_SIZE_SUBTITLE,
                            weight=ft.FontWeight.BOLD,
                            color=Config.COLORS['text_dark'],
                            font_family=Config.TITLE_FONT
                        ),
                        # Descrição da fase
                        ft.Text(
                            phase['description'],
                            size=Config.FONT_SIZE_CAPTION,
                            color=Config.COLORS['text_dark'],
                            font_family=Config.TEXT_FONT
                        )
                    ], spacing=3, expand=True),  # Espaçamento entre título e descrição
                    
                    # Seta para direita (apenas para fases desbloqueadas)
                    ft.Text(
                        "➡️" if is_clickable else "",
                        size=20,
                        color=Config.COLORS['primary_blue'] if is_clickable else "transparent"
                    )
                ], spacing=10),
                
                # Definir o ID da fase como data do botão
                data=phase["id"],
                
                # Estilo do container
                bgcolor=Config.COLORS[phase["status"]] if phase["status"] in Config.COLORS else "#DDDDDD",
                border_radius=10,
                padding=15,
                margin=ft.margin.only(bottom=10),
                
                # Adicionar borda mais visível
                border=ft.border.all(
                    width=2,
                    color=Config.COLORS['primary_blue'] if is_clickable else Config.COLORS['locked']
                ),
                
                # Adicionar efeito de clique apenas para fases desbloqueadas
                on_click=self.handle_phase_button_click if is_clickable else None,
                
                # Cursor de mão para indicar que é clicável
                ink=is_clickable,
                
                # Adicionar sombra para efeito 3D
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color="#60000000",
                    offset=ft.Offset(0, 2)
                ) if is_clickable else None
            )
            
            phases_list.append(phase_button)
        
        # Retornar coluna com título e lista de fases
        return ft.Column([
            ft.Text(
                "📚 Fases do Curso",
                size=Config.FONT_SIZE_TITLE,
                weight=ft.FontWeight.BOLD,
                color=Config.COLORS['text_dark'],
                font_family=Config.TITLE_FONT
            ),
            ft.Container(height=10),  # Espaçamento vertical
            ft.Column(phases_list)  # Lista de botões de fase
        ], spacing=5)
