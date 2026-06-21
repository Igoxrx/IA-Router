"""
Módulo de serviço para orquestração do LLM.
Gerencia a comunicação com a API Groq via litellm e aplica as regras do roteador.
"""

import json
import logging
from typing import Dict, Any, Optional
from litellm import completion

# Configuração de log para rastreamento de erros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
Você é um Orquestrador de IA. Sua ÚNICA função é analisar o <problema_do_usuario> e delegar a solução.

🚨 REGRA 1: Foco 100% no problema. Não explique como escolher IAs.
🚨 REGRA 2: Escolha APENAS modelos comerciais reais (ChatGPT, Claude, Gemini, Perplexity, DeepSeek, Qwen, Llama).

MÉTODO DE ANÁLISE:
1. Simples: Escolha 1 IA.
2. Complexo: Escolha de 2 a 5 IAs para um fluxo.

Responda EXATAMENTE neste formato JSON:
{
    "tipo_de_tarefa": "Simples ou Complexa",
    "reflexao_estrategica": "Por que esta estratégia resolve.",
    "estrategia_geral": "Visão geral.",
    "ordem_de_execucao": [
        {"passo": 1, "ia": "Nome da IA", "objetivo": "Ação"}
    ]
}
"""

def analisar_problema(prompt_usuario: str) -> Optional[Dict[str, Any]]:
    """
    Envia o problema do usuário para o modelo de IA e retorna um plano de orquestração estruturado.

    Args:
        prompt_usuario (str): O problema descrito pelo usuário.

    Returns:
        Optional[Dict[str, Any]]: Dicionário contendo o JSON de resposta ou None em caso de falha.
    """
    if not prompt_usuario or not prompt_usuario.strip():
        logger.warning("Prompt vazio enviado para análise.")
        return None

    mensagem_usuario = f"<problema_do_usuario>\n{prompt_usuario}\n</problema_do_usuario>"

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": mensagem_usuario}
            ],
            response_format={"type": "json_object"}
        )
        conteudo_raw = response.choices[0].message.content
        return json.loads(conteudo_raw)
        
    except json.JSONDecodeError as e:
        logger.error(f"Falha ao decodificar JSON retornado pela IA: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro na comunicação com a API (litellm): {e}")
        raise RuntimeError(f"Erro de orquestração: {str(e)}")