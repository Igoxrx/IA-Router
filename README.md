# AI Router — Orquestrador Dinâmico de Prompts

O **AI Router** é um orquestrador inteligente projetado para analisar a complexidade de problemas ou tarefas e definir o fluxo ideal de execução. O sistema classifica as demandas (Simples vs. Complexas) e distribui os fluxos de forma automática entre múltiplos modelos ou agentes de IA.

A aplicação foi desenvolvida para rodar localmente no Windows de forma transparente, contando com uma interface gráfica baseada em **Streamlit** e um gerenciador de execução que mantém o sistema ativo diretamente na bandeja do sistema (*System Tray*).

---

## 🚀 Funcionalidades Principais

* **Roteamento Inteligente:** Identifica o tipo de tarefa e desenha estratégias detalhadas com pipelines de múltiplos passos.
* **Interface Interativa (Streamlit):** Área de texto para inserção de problemas, visualização da reflexão estratégica e inspeção dos prompts gerados para cada etapa.
* **Execução em Segundo Plano:** Inicialização silenciosa (*headless*) com controle total (abrir interface ou encerrar processos) através de um ícone na barra de tarefas.
* **Instalação Automatizada:** Script utilitário que detecta o interpretador Python no `AppData` local e gera atalhos de inicialização rápida na Área de Trabalho.

---

## 📂 Estrutura do Repositório

```text
├── core/
│   └── llm_service.py       # Integração com os modelos e lógica de análise estratégica
├── app.py                   # Interface de usuário principal (Streamlit UI)
├── rodar_background.py      # Gerenciador de segundo plano (Pystray / System Tray)
├── instalador.py            # Script universal de instalação e criação de atalhos
├── .env.example             # Template para configuração das variáveis de ambiente
└── app_background.log      # Log gerado dinamicamente para o serviço em segundo plano

```

---

## 🛠️ Pré-requisitos e Instalação

### 1. Requisitos de Sistema

* **Sistema Operacional:** Windows
* **Linguagem:** Python 3.11 ou superior

### 2. Instalação das Dependências

Abra o terminal na pasta do projeto e instale os pacotes necessários via `pip`:

```bash
pip install streamlit python-dotenv pillow pystray winshell pywin32

```

### 3. Configuração das Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto (utilize o `.env.example` como referência) e adicione sua chave de API:

```env
GROQ_API_KEY=sua_chave_api_aqui

```

### 4. Geração do Atalho

Para gerar o atalho de inicialização automática na sua Área de Trabalho, execute:

```bash
python instalador.py

```

---

## 🕹️ Como Usar

### Modo Padrão (Bandeja do Sistema)

Dê um duplo clique no atalho **AI Router** criado na sua Área de Trabalho ou execute diretamente pelo terminal:

```bash
python rodar_background.py

```

* O servidor iniciará em modo oculto e abrirá automaticamente o seu navegador padrão em `http://127.0.0.1:8501`.
* Um ícone surgirá na bandeja do sistema (perto do relógio). Clique com o botão direito para acessar as opções **"Abrir Interface"** ou **"Desligar AI Router"** (que encerra todos os subprocessos com segurança).

### Modo Desenvolvimento

Caso queira rodar apenas a interface do Streamlit diretamente no terminal para depuração:

```bash
streamlit run app.py

```

---

## 🔍 Resolução de Problemas (Troubleshooting)

* **Erro de Chave Não Encontrada:** Certifique-se de que o arquivo `.env` foi criado corretamente na raiz e que o nome da variável é estritamente `GROQ_API_KEY`.
* **Python Não Detectado no AppData:** O `instalador.py` varre o caminho padrão local do Windows. Se o seu Python foi instalado globalmente, crie o atalho apontando manualmente para o seu executável `pythonw.exe`.
* **Navegador não abriu:** O script aguarda 4 segundos para o servidor Streamlit subir. Caso sua máquina demore um pouco mais, basta abrir o navegador e acessar manualmente `http://127.0.0.1:8501`.

```
