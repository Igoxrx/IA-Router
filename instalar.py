"""Script de instalação Universal.

Busca automaticamente qualquer versão do Python instalada no AppData do usuário.
"""

import os
from pathlib import Path
import sys
import time
from win32com.client import Dispatch
import winshell


def obter_pasta_real_do_projeto() -> Path:
    """Retorna o caminho absoluto do diretório do projeto."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.absolute()
    return Path(__file__).parent.absolute()


def encontrar_python_no_appdata() -> Path | None:
    """Varre a pasta AppData do usuário procurando por qualquer versão do Python."""
    appdata_programs = Path(os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python"))

    if not appdata_programs.exists():
        return None

    pastas_python = [
        d
        for d in appdata_programs.iterdir()
        if d.is_dir() and d.name.lower().startswith("python")
    ]

    if not pastas_python:
        return None

    pastas_python.sort(reverse=True)

    for pasta in pastas_python:
        pythonw = pasta / "pythonw.exe"
        python_normal = pasta / "python.exe"

        if pythonw.exists():
            return pythonw
        if python_normal.exists():
            return python_normal

    return None


def criar_atalho_appdata():
    """Valida o ambiente e cria o atalho de inicialização na Área de Trabalho."""
    pasta_projeto = obter_pasta_real_do_projeto()
    script_background = pasta_projeto / "rodar_background.py"
    python_exe = encontrar_python_no_appdata()

    print("--- VERIFICAÇÃO SISTEMA ---")
    print(f"Pasta do Projeto: {pasta_projeto}")
    print(f"Python detectado no AppData: {python_exe if python_exe else 'NENHUM'}")
    print("---------------------------\n")

    if not python_exe:
        print("Erro crítico: Nenhuma instalação do Python foi encontrada no seu AppData.")
        print("Por favor, instale o Python antes de rodar o instalador.")
        input("\nPressione Enter para sair...")
        return

    area_de_trabalho = Path(winshell.desktop())
    caminho_atalho = area_de_trabalho / "AI Router.lnk"

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(caminho_atalho))

    shortcut.Targetpath = str(python_exe)
    shortcut.Arguments = f'"{str(script_background)}"'
    shortcut.WorkingDirectory = str(pasta_projeto)
    shortcut.Description = "Iniciar AI Router - Roteador de Prompts"
    shortcut.IconLocation = "shell32.dll, 13"

    shortcut.Save()
    print("\nConfiguração concluída! Atalho gerado com sucesso na Área de Trabalho.")


if __name__ == "__main__":
    try:
        criar_atalho_appdata()
        time.sleep(3)
    except Exception as e:
        print(f"\nErro na instalação: {e}")
        input("\nPressione Enter para fechar...")