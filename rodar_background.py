"""Gerenciador de execução em segundo plano para o AI Router.

Inicia o Streamlit em modo headless e cria um ícone na bandeja do sistema.
"""

import logging
import os
import subprocess
import time
import webbrowser
from PIL import Image, ImageDraw
import pystray

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_APP = os.path.join(PASTA_PROJETO, "app.py")
PORTA_STREAMLIT = 8501

logging.basicConfig(
    level=logging.INFO, filename=os.path.join(PASTA_PROJETO, "app_background.log")
)
processo_streamlit = None


def criar_imagem_icone() -> Image:
    """Gera o ícone dinamicamente."""
    image = Image.new("RGB", (64, 64), color=(31, 34, 42))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill=(29, 191, 115))
    return image


def iniciar_streamlit():
    """Inicia o servidor Streamlit em segundo plano."""
    global processo_streamlit

    streamlit_exe = os.path.join(
        os.getcwd(), "python_interno", "Scripts", "streamlit.exe"
    )
    if not os.path.exists(streamlit_exe):
        streamlit_exe = "streamlit"

    comando = [
        streamlit_exe,
        "run",
        CAMINHO_APP,
        "--server.port",
        str(PORTA_STREAMLIT),
        "--server.address",
        "127.0.0.1",
        "--server.headless",
        "true",
    ]

    processo_streamlit = subprocess.Popen(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def encerrar_aplicativo(icon: pystray.Icon, item: pystray.MenuItem):
    """Encerra a aplicação e finaliza os processos ativos."""
    global processo_streamlit

    icon.stop()

    if processo_streamlit:
        processo_streamlit.terminate()
        try:
            processo_streamlit.wait(timeout=2)
        except subprocess.TimeoutExpired:
            processo_streamlit.kill()

    os._exit(0)


def abrir_no_navegador(icon: pystray.Icon, item: pystray.MenuItem):
    """Abre o navegador padrão na porta configurada."""
    webbrowser.open(f"http://127.0.0.1:{PORTA_STREAMLIT}")


def main():
    """Fluxo principal de inicialização do servidor e da bandeja do sistema."""
    iniciar_streamlit()

    time.sleep(4)

    webbrowser.open(f"http://127.0.0.1:{PORTA_STREAMLIT}")

    menu_contexto = pystray.Menu(
        pystray.MenuItem("Abrir Interface", abrir_no_navegador, default=True),
        pystray.MenuItem("Desligar AI Router", encerrar_aplicativo),
    )

    icone = pystray.Icon(
        "AI_Router",
        criar_imagem_icone(),
        title="AI Router - Roteador de Prompts",
        menu=menu_contexto,
    )

    icone.run()


if __name__ == "__main__":
    main()