# Stuttz: Uma Jornada na Aprendizagem de Python

*Desvendando os segredos da programação através das páginas do tempo*

## O Grimório Digital

Stuttz não é apenas um aplicativo de aprendizado - é um grimório interativo que transporta o estudante para uma jornada através do conhecimento de Python. Cada página deste livro antigo revela segredos da programação, desafios arcanos e sabedoria ancestral da arte do código.

## A Estética do Pergaminho

A interface do Stuttz é meticulosamente desenhada para evocar a sensação de estar folheando um livro antigo:

- **Textura de Pergaminho**: O plano de fundo apresenta uma textura suave de papel envelhecido, com bordas levemente desgastadas e manchas sutis que contam histórias de séculos passados.

- **Tipografia Clássica**: Os textos são apresentados em fontes que remetem a manuscritos antigos, com capitulares ornamentadas iniciando cada nova seção.

- **Ilustrações Vintage**: Pequenos desenhos a traço decoram as margens, representando conceitos de programação como serpentes (Python), estruturas de dados e algoritmos.

- **Encadernação Virtual**: As transições entre telas simulam o virar de páginas de um livro físico, completas com o som suave de papel.

## Capítulos da Jornada

O conhecimento no Stuttz é organizado em capítulos (fases) que progridem de forma natural:

1. **O Despertar do Código**: Introdução aos conceitos básicos de Python
2. **Encantamentos Primitivos**: Variáveis, tipos de dados e operações simples
3. **Pergaminhos Condicionais**: Estruturas de decisão e lógica
4. **Ciclos Arcanos**: Laços e iterações
5. **Invocações e Rituais**: Funções e módulos
6. **Tomos do Conhecimento**: Estruturas de dados
7. **A Guilda dos Objetos**: Programação orientada a objetos
8. **Magia Avançada**: Tópicos especializados e bibliotecas

## A Magia em Ação

Quando um aprendiz abre o Stuttz, encontra-se diante de um mapa antiquado que revela seu progresso na jornada. Cada capítulo é representado por um local místico conectado por caminhos sinuosos desenhados à mão.

### Elementos Mágicos

- **Pergaminhos de Desafio**: Os quizzes surgem como pergaminhos que se desenrolam, revelando questões arcanas sobre Python.

- **Tinta Animada**: As respostas corretas fazem a tinta brilhar com uma luz dourada suave, enquanto explicações surgem como se escritas por uma pena invisível.

- **Medidor de Experiência**: Um frasco de poção que se enche gradualmente à medida que o aprendiz ganha conhecimento (XP).

- **Amuleto de Sequência**: Um talismã que brilha mais intensamente a cada dia consecutivo de estudo.

### O Oráculo de Gemini

O assistente de IA não aparece como uma entidade moderna, mas como um oráculo antigo que emerge das páginas quando invocado. Suas sugestões e explicações são apresentadas como sabedoria ancestral, embora o conteúdo seja tecnicamente preciso e atualizado.

## Ritual de Uso Diário

1. O aprendiz abre o grimório (inicia o aplicativo)
2. Consulta o mapa para escolher seu próximo destino (fase de estudo)
3. Absorve conhecimento através de textos antigos (material de estudo)
4. Enfrenta desafios mágicos (quizzes interativos)
5. Recebe revelações do oráculo (dicas personalizadas da IA)
6. Coletá seus troféus e poções (recompensas e XP)
7. Marca seu progresso no mapa do conhecimento

## Encantamentos Técnicos (Especificações)

Por trás da fachada antiga, o Stuttz utiliza tecnologia moderna:

- Construído com Python e o framework Flet
- Alimentado pela sabedoria da API Google Gemini
- Conhecimento armazenado em pergaminhos digitais (arquivos JSON)
- Arquitetura secreta que segue os princípios místicos do MVC

## O Pacto com o Aprendiz

Stuttz estabelece um compromisso mágico com seus usuários:

- **Consistência**: O ritual diário é recompensado
- **Progressão**: Cada página virada revela novo conhecimento
- **Adaptação**: O oráculo compreende as necessidades de cada aprendiz
- **Imersão**: A experiência estética transporta o estudante para um mundo onde aprender é uma aventura



---
#Versão séria
---



  # Stuttz - Plataforma de Aprendizado Multidisciplinar

Stuttz é uma aplicação educacional versátil que oferece uma jornada de aprendizado em diversas disciplinas, incluindo Python, através de uma interface gráfica interativa e gamificada. O aplicativo utiliza a biblioteca Flet para criar uma experiência de usuário agradável e a API do Google Gemini para gerar dicas de estudo e explicações personalizadas.

## 📋 Características

- **Trilha de Aprendizado**: Progresso visual através de fases de estudo
- **Quiz Interativo**: Teste seus conhecimentos com perguntas desafiadoras
- **Dicas de Estudo**: Recomendações personalizadas geradas por IA
- **Explicações Detalhadas**: Explicações didáticas para respostas de quiz
- **Sistema de Gamificação**: Ganhe XP, suba de nível e mantenha sequências diárias
- **Interface Amigável**: Design intuitivo e agradável visualmente
- **Flexibilidade Educacional**: Adaptável a múltiplas disciplinas e áreas de conhecimento

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

## 🗓️ Próximos Desenvolvimentos

- Telas de cadastro de usuário
- Sistema de informações acadêmicas
- Suporte a mais disciplinas e áreas de conhecimento

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

Desenvolvido com ❤️ para ajudar pessoas a aprenderem diversas disciplinas de forma divertida e eficiente.


---

*Este grimório digital está em constante evolução, com novos feitiços (features) sendo adicionados pelos mestres arcanos (desenvolvedores) a cada lua nova.* 
