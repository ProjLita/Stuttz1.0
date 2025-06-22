"""
STUTTZ - ARQUIVO PRINCIPAL
Este arquivo inicia o aplicativo e configura a interface
"""

import flet as ft  # Importa a biblioteca Flet para criação da interface gráfica
from controllers.app_controller import AppController  # Importa o controlador principal do aplicativo
from config import Config  # Importa as configurações globais do aplicativo

def main(page: ft.Page):
    """
    Função principal que configura e inicia o app
    
    Args:
        page: Objeto Page do Flet que representa a janela principal do aplicativo
    """
    
    # === CONFIGURAÇÕES DA PÁGINA ===
    page.title = Config.APP_NAME  # Define o título da janela do aplicativo
    page.theme_mode = ft.ThemeMode.LIGHT  # Define o tema claro para o aplicativo
    page.bgcolor = Config.COLORS['background_dark']  # Define a cor de fundo da página
    page.vertical_alignment = ft.MainAxisAlignment.START  # Alinha os elementos no topo
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centraliza os elementos horizontalmente
    page.padding = 10  # Adiciona um espaçamento interno de 10 pixels
    
    # Configurar as fontes
    print("🔍 Configurando as fontes...")
    try:
        page.fonts = {
            "Workbench": "https://fonts.googleapis.com/css2?family=Workbench&display=swap",
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Roboto")
        print("✅ Fontes configuradas. Serão carregadas quando o aplicativo iniciar.")
    except Exception as e:
        print(f"⚠️ Erro ao configurar fontes: {e}")
    
    # Configurar tamanho da janela
    page.window.width = 480  # Define a largura da janela aumentada
    page.window.height = 800  # Define a altura da janela aumentada
    page.window.resizable = False  # Impede que o usuário redimensione a janela
    
    # === CRIAR O CONTROLADOR ===
    # O controlador é o "cérebro" que gerencia tudo
    controller = AppController(page)  # Instancia o controlador principal, passando a página
    
    # === ATUALIZAR STREAK DO USUÁRIO ===
    # Atualiza o streak (dias consecutivos) do usuário
    streak_increased = controller.update_streak()
    if streak_increased and controller.user_data["streak"] > 1:
        # Mostrar mensagem de streak apenas se aumentou e não é o primeiro dia
        controller.show_message(f"🔥 Sequência de {controller.user_data['streak']} dias!")
    
    # === CONTAINER PRINCIPAL ===
    # Este é o "livro" que contém toda a interface
    width = min(460, page.width * 0.95) if page.width else 440  # Calcula a largura responsiva
    height = page.height * 0.95 if page.height else 760  # Calcula a altura responsiva
    
    main_container = ft.Container(
        content=controller.get_current_view(),  # Obtém a view atual do controlador
        width=width,  # Define a largura calculada
        height=height,  # Define a altura calculada
        bgcolor=Config.COLORS['parchment'],  # Define a cor de fundo como papel antigo
        border_radius=15,  # Arredonda os cantos em 15 pixels
        border=ft.border.all(3, Config.COLORS['wood_brown']),  # Adiciona borda marrom
        shadow=ft.BoxShadow(  # Adiciona sombra para efeito 3D
            spread_radius=1,  # Raio de espalhamento da sombra
            blur_radius=15,  # Raio de desfoque da sombra
            color="#60000000",  # Cor da sombra (preto com 60% de opacidade)
            offset=ft.Offset(0, 5)  # Desloca a sombra 5 pixels para baixo
        ),
        padding=15  # Adiciona espaçamento interno de 15 pixels
    )
    
    # === ADICIONAR À PÁGINA ===
    page.add(main_container)  # Adiciona o container principal à página
    page.update()  # Atualiza a interface para exibir o conteúdo

# === EXECUTAR O APP ===
if __name__ == "__main__":
    print("🚀 Iniciando o Stuttz...")  # Mensagem de inicialização no console
    ft.app(target=main)  # Inicia o aplicativo Flet, chamando a função main
