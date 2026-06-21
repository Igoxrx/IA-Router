AI Router — Orquestrador Dinâmico de Prompts
O AI Router é um orquestrador inteligente que analisa a complexidade de problemas ou tarefas e define o fluxo ideal de execução, distribuindo as demandas de forma automática e integrada entre múltiplos modelos ou agentes de IA.

A aplicação foi projetada para rodar localmente no Windows de forma transparente, incluindo uma interface gráfica interativa baseada em Streamlit e um gerenciador que mantém o sistema ativo diretamente na bandeja do sistema (System Tray).

🚀 Funcionalidades
Roteamento Inteligente: Classifica a complexidade da tarefa (Simples vs. Complexa) e desenha uma estratégia detalhada com pipelines de múltiplos passos.

Interface Interativa: Interface web construída em Streamlit para inserção de prompts, visualização de estratégias de IA e inspeção dos prompts gerados para cada etapa.

Execução em Segundo Plano: Inicialização silenciosa (headless) com controle total através de um ícone dedicado na barra de tarefas do Windows.

Instalação Automatizada: Script de configuração universal que detecta o interpretador Python local e cria atalhos prontos para o usuário final.

📂 Estrutura do Projeto
Plaintext
├── core/
│   └── llm_service.py       # Integração com os modelos de linguagem e lógica de análise
├── app.py                   # Interface de usuário principal (Streamlit UI)
├── rodar_background.py      # Gerenciador de segundo plano (Pystray/System Tray)
├── instalador.py            # Script universal de instalação e criação de atalhos
├── .env                     # Arquivo de configuração de variáveis de ambiente
└── app_background.log      # Log gerado automaticamente na execução em segundo plano
🛠️ Requisitos de Sistema
Sistema Operacional: Windows

Linguagem: Python 3.11 ou superior

Dependências Principais: streamlit, pystray, pillow, python-dotenv, winshell, pywin32

🔧 Configuração e Instalação
1. Configurar Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto e insira a sua chave de API do provedor utilizado (como a Groq):

Snippet de código
GROQ_API_KEY=sua_chave_api_aqui
2. Instalar Dependências
Certifique-se de que o Python está instalado e configurado no seu ambiente. Em seguida, instale os pacotes necessários:

Bash
pip install streamlit pystray pillow python-dotenv winshell pywin32
3. Criar Atalho na Área de Trabalho
Execute o script de instalação para detectar automaticamente o ambiente e gerar o atalho de inicialização rápida na Área de Trabalho:

Bash
python instalador.py
🕹️ Como Utilizar
Após a instalação, você pode iniciar o ecossistema diretamente pelo atalho criado "AI Router" na Área de Trabalho.

Inicialização: O servidor Streamlit iniciará em modo oculto e uma guia será aberta automaticamente no seu navegador padrão no endereço http://127.0.0.1:8501.

Uso da Interface: Insira o problema que deseja resolver na área de texto e clique em "Desenhar Fluxo e Distribuir". O sistema irá expor a reflexão estratégica do modelo e os cards específicos de cada passo gerado.

Controle via Bandeja (System Tray): Um ícone verde será adicionado perto do relógio do Windows.

Clique duplo ou "Abrir Interface": Restaura a aba da interface no navegador.

"Desligar AI Router": Finaliza de forma segura todos os subprocessos ocultos do Streamlit e encerra o sistema.