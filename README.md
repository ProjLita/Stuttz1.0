# Stuttz - Trilha de Aprendizado Python

Stuttz é uma aplicação educacional que oferece uma jornada de aprendizado em Python através de uma interface gráfica interativa e gamificada. O aplicativo utiliza a biblioteca Flet para criar uma experiência de usuário agradável e a API do Google Gemini para gerar dicas de estudo e explicações personalizadas.

## 📋 Características

- **Trilha de Aprendizado**: Progresso visual através de fases de estudo
- **Quiz Interativo**: Teste seus conhecimentos com perguntas desafiadoras
- **Dicas de Estudo**: Recomendações personalizadas geradas por IA
- **Explicações Detalhadas**: Explicações didáticas para respostas de quiz
- **Sistema de Gamificação**: Ganhe XP, suba de nível e mantenha sequências diárias
- **Interface Amigável**: Design intuitivo e agradável visualmente

## 🚀 Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/stuttz.git
   cd stuttz
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure a API do Google Gemini:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave de API: `GEMINI_API_KEY=sua_chave_aqui`

5. Execute o aplicativo:
   ```
   python main.py
   ```

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal
- **Flet**: Framework para criação de interfaces gráficas
- **Google Gemini API**: Geração de conteúdo personalizado com IA
- **JSON**: Armazenamento de dados do usuário e do roadmap

## 🏗️ Arquitetura

O projeto segue o padrão de arquitetura MVC (Model-View-Controller):

- **Models**: Estruturas de dados e lógica de negócios
- **Views**: Interface gráfica e componentes visuais
- **Controllers**: Gerenciamento de estado e lógica de controle

## 📁 Estrutura do Projeto

```
stuttz/
├── config.py           # Configurações globais e mensagens
├── controllers/        # Controladores do aplicativo
│   ├── __init__.py
│   └── app_controller.py
├── main.py             # Ponto de entrada do aplicativo
├── models/             # Modelos de dados
│   ├── __init__.py
│   └── data_models.py
├── requirements.txt    # Dependências do projeto
├── utils/              # Utilitários
│   └── ai_helper.py    # Integração com a API do Google Gemini
└── views/              # Interfaces visuais
    ├── __init__.py
    ├── phase_detail_view.py
    └── roadmap_view.py
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através de [seu-email@exemplo.com].

---

Desenvolvido com ❤️ para ajudar pessoas a aprenderem Python de forma divertida e eficiente.
