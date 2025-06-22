"""
Utilitários para integração com IA
Este módulo gerencia a comunicação com a API do Google Gemini
"""

from google import genai  # Importa a biblioteca do Google Generative AI
import os  # Importa o módulo para interagir com o sistema operacional
from dotenv import load_dotenv  # Importa o módulo para carregar variáveis de ambiente de arquivos .env
from config import Config  # Importa as configurações globais do aplicativo

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env na raiz do projeto

# Configurar a API do Gemini obtendo a chave da API das variáveis de ambiente
API_KEY = os.getenv("GEMINI_API_KEY")  # Obtém a chave da API das variáveis de ambiente

# Verificar se a API_KEY foi definida e inicializar o cliente
if API_KEY:
    # Cria um cliente da API Gemini usando a chave fornecida
    client = genai.Client(api_key=API_KEY)
else:
    # Se a chave não estiver definida, exibe um erro e define o cliente como None
    print("❌ ERRO: GEMINI_API_KEY não encontrada no ambiente ou arquivo .env")
    client = None

def get_gemini_response(prompt: str, max_tokens: int = 1000) -> str:
    """
    Obtém uma resposta do modelo Gemini para um prompt específico
    
    Args:
        prompt: O texto de pergunta/prompt a ser enviado ao modelo
        max_tokens: Limite máximo de tokens na resposta (padrão: 1000)
        
    Returns:
        Uma string com a resposta do modelo ou uma mensagem de erro
    """
    # Verificar se o cliente foi inicializado corretamente
    if client is None:
        # Retorna uma mensagem de erro se o cliente não foi inicializado
        return "Não foi possível gerar uma resposta. A chave de API do Gemini não está configurada."
    
    try:
        # Tenta gerar uma resposta usando o modelo definido na configuração
        response = client.models.generate_content(
            model=Config.AI_MODEL,  # Usa o modelo definido nas configurações
            contents=prompt,  # Envia o prompt para o modelo
            config={
                'max_output_tokens': max_tokens,  # Limita o tamanho da resposta
                'temperature': 0.7,  # Define a temperatura (criatividade) da resposta
            }
        )
        
        # Retorna o texto da resposta, garantindo que seja uma string válida
        return response.text if response.text is not None else ""
    except Exception as e:
        # Captura e registra qualquer erro que ocorra durante a geração da resposta
        print(f"❌ Erro ao gerar resposta: {e}")
        # Retorna uma mensagem de erro amigável incluindo detalhes do erro
        return f"Desculpe, não consegui gerar uma resposta. Erro: {str(e)}"