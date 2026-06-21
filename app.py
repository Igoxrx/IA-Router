"""Interface de Usuário do AI Router via Streamlit."""

import os
import streamlit as st
from dotenv import load_dotenv
from core.llm_service import analisar_problema

load_dotenv()


def validar_ambiente():
    """Garante que as variáveis de ambiente necessárias estejam configuradas."""
    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "Erro: Chave GROQ_API_KEY não encontrada. Verifique o arquivo .env."
        )
        st.stop()


def renderizar_ui():
    """Constrói a estrutura principal da interface Streamlit."""
    st.set_page_config(page_title="AI Router - Multi-Especialista", layout="wide")
    st.title("AI Router — Orquestrador Dinâmico")
    st.markdown(
        "Envie seu problema. O Roteador vai analisar, classificar a complexidade e "
        "**definir o fluxo ideal** (seja um passo único ou um pipeline completo)."
    )

    prompt_bruto = st.text_area("Descreva o problema ou tarefa:", height=100)

    if st.button("Desenhar Fluxo e Distribuir"):
        if not prompt_bruto.strip():
            st.warning("Por favor, insira um problema válido antes de continuar.")
            return

        with st.spinner("Analisando a complexidade e desenhando o pipeline..."):
            try:
                dados = analisar_problema(prompt_bruto)

                if not dados:
                    st.error("A IA retornou um formato inválido. Tente novamente.")
                    return

                exibir_resultados(dados, prompt_bruto)

            except RuntimeError as e:
                st.error(f"Falha de comunicação: {e}")


def exibir_resultados(dados: dict, prompt_bruto: str):
    """Renderiza as estratégias e etapas retornadas pelo serviço de LLM."""
    tipo_tarefa = dados.get("tipo_de_tarefa", "Desconhecida")

    if "Simples" in tipo_tarefa:
        st.success("Tarefa de execução direta detectada!")
    else:
        st.info("Tarefa complexa! Pipeline de múltiplos passos gerado.")

    st.markdown(f"**Estratégia:** {dados.get('estrategia_geral', 'Não definida')}")

    with st.expander("Reflexão do Gerente de IA"):
        st.write(dados.get("reflexao_estrategica", "Sem reflexão gerada."))

    etapas = dados.get("ordem_de_execucao", [])
    num_ias = len(etapas)

    if num_ias == 0:
        st.warning(
            "Nenhuma IA foi selecionada. Tente detalhar mais o problema."
        )
        return

    cols = st.columns(num_ias)
    for i, etapa in enumerate(etapas):
        renderizar_card_ia(cols[i], i + 1, etapa, num_ias, prompt_bruto)


def renderizar_card_ia(
    coluna, passo: int, etapa: dict, total_ias: int, prompt_bruto: str
):
    """Renderiza o card individual contendo as atribuições de cada IA."""
    with coluna:
        ia_nome = etapa.get("ia", "IA Genérica")
        objetivo = etapa.get("objetivo", "Objetivo não definido")

        titulo = f"Passo {passo}" if total_ias > 1 else "Ação Única"
        st.subheader(titulo)
        st.markdown(f"**{ia_nome}**")
        st.write(objetivo)

        prompt_completo = (
            f"Contexto do Projeto:\n{prompt_bruto}\n\n---\n\n"
            f"Sua Missão:\n{objetivo}"
        )
        with st.expander(f"Prompt ({ia_nome})"):
            st.code(prompt_completo, language="markdown")


if __name__ == "__main__":
    validar_ambiente()
    renderizar_ui()