# 1 - IMPORTAÇÃO DAS BIBLIOTECAS
import streamlit as st
import pandas as pd
import json
import requests
import os

# 2 - CÓDIGO DE CONFIGURAÇÃO DO OLLAMA
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gpt-oss:20b" 

# 3 - CÓDIGO PARA CARREGAR OS DADOS
def carregar_dados():
    # Caminho para a pasta data (subindo um nível a partir de src/)
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    try:
        df_transacoes = pd.read_csv(os.path.join(DATA_PATH, 'extrato_transacoes.csv'))
        df_dicas = pd.read_csv(os.path.join(DATA_PATH, 'dicas_educativas.csv'))
        
        with open(os.path.join(DATA_PATH, 'metas_poupanca.json'), 'r', encoding='utf-8') as f:
            metas = json.load(f)
        with open(os.path.join(DATA_PATH, 'categorias_limites.json'), 'r', encoding='utf-8') as f:
            limites = json.load(f)
            
        return df_transacoes, df_dicas, metas, limites
    except FileNotFoundError as e:
        st.error(f"Erro: Arquivo não encontrado no caminho: {e.filename}")
        return None, None, None, None

# 4 - CÓDIGO PARA MONTAR CONTEXTO (ATUALIZADO PARA PRECISÃO)
def montar_contexto(df_t, df_d, metas, limites):
    # Padroniza nomes de colunas para minúsculo
    df_t.columns = df_t.columns.str.lower()
    
    contexto = f"USUÁRIO: {metas['usuario']} | RENDA: R$ {metas['renda_mensal']}\n"
    contexto += f"META: {metas['reserva_emergencia']['status_atual']} de {metas['reserva_emergencia']['valor_objetivo']} (Reserva)\n"
    
    contexto += "\nLIMITES VS GASTOS ATUAIS (VALORES REAIS):\n"
    
    for item in limites['limites_mensais']:
        cat_nome = item['categoria']
        limite_val = item['limite_maximo']
        
        # SOMA INTELIGENTE: Procura o termo na coluna 'categoria' OU na 'tipo_gasto'
        # Isso resolve o problema da Netflix estar como 'Assinaturas' mas ser do tipo 'Lazer'
        filtro = df_t[
            (df_t['valor'] < 0) & 
            ((df_t['categoria'].str.contains(cat_nome, case=False, na=False)) | 
             (df_t['tipo_gasto'].str.contains(cat_nome, case=False, na=False)))
        ]
        
        gasto_real = abs(filtro['valor'].sum())
        porcentagem = (gasto_real / limite_val) * 100
        
        status = "⚠️ CRÍTICO" if porcentagem >= 80 else "✅ OK"
        contexto += f"- {cat_nome}: Gasto R$ {gasto_real:.2f} / Limite R$ {limite_val:.2f} ({porcentagem:.1f}% usado - {status})\n"
    
    # Seleciona uma dica relevante
    dica = df_d.sample(1).iloc[0]
    contexto += f"\nDICA PARA O USUÁRIO: {dica['dica']}"
    
    return contexto

# 5 - CÓDIGO PARA SISTEMA DE PROMPT
def system_prompt(contexto):
    return f"""Você é o Fin, um assistente de planejamento financeiro pessoal empático e consultivo. 
Seu objetivo é ajudar o João Silva a atingir sua meta de Reserva de Emergência.

DIRETRIZES DE COMPORTAMENTO:
1. ANÁLISE DE DADOS: Sempre consulte o contexto de 'extrato_transacoes.csv' e 'categorias_limites.json' antes de responder.
2. CÁLCULOS: Para somas e porcentagens, descreva o raciocínio. Se notar que um limite de categoria ultrapassou 80%, emita um alerta amigável.
3. EDUCAÇÃO: Sempre que identificar um gasto "Impulsivo" recorrente, sugira uma dica do arquivo 'dicas_educativas.csv'.
4. VERACIDADE: Nunca invente transações ou saldos. Se os dados não estiverem no contexto, diga que não tem acesso a essa informação específica.
5. PLANEJAMENTO: Quando o usuário perguntar sobre o "depois" ou metas futuras, consulte a seção 'METAS DE LONGO PRAZO'. Lembre o usuário que a prioridade ainda é a Reserva, mas mostre entusiasmo pelos planos futuros (como a entrada do apartamento).


REGRAS DE SEGURANÇA:
- Não realize transações bancárias.
- Não forneça dicas de investimentos em renda variável (ações/cripto), foque em economia e renda fixa para reserva.
- Se o usuário sair do tema financeiro, use a mensagem de erro padrão, respondendo de forma educada explicando que você é o Fin, um especialista em finanças, e que seu objetivo é ajudá-lo com o dinheiro, não com outros assuntos (mencione o assunto dito pelo usuário).

ESTRUTURA DE RESPOSTA:
- Use bullet points para facilitar a leitura.
- Mantenha um tom encorajador, nunca julgador.

CONTEXTO DOS DADOS:
{contexto}
"""

# 6 - CÓDIGO PARA CHAMAR O OLLAMA
def chamar_ollama(prompt_sistema, pergunta_usuario):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{prompt_sistema}\n\nPergunta: {pergunta_usuario}\nResposta do Fin:",
        "stream": False
    }
    try:
        # Timeout aumentado para modelos pesados como o gpt-oss
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        return response.json().get("response", "Desculpe, tive um erro interno.")
    except Exception as e:
        return f"Erro de conexão com Ollama: {str(e)}"

# 7 - CÓDIGO PARA CRIAR A INTERFACE
def main():
    st.set_page_config(page_title="Fin - Consultor Local", page_icon="📈")
    st.title("📈 Fin - Seu agente financeiro!")

    df_t, df_d, metas, limites = carregar_dados()

    if df_t is not None:
        contexto_real = montar_contexto(df_t, df_d, metas, limites)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Como estão meus gastos?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                res_sistema = system_prompt(contexto_real)
                resposta = chamar_ollama(res_sistema, prompt)
                st.markdown(resposta)
            
            st.session_state.messages.append({"role": "assistant", "content": resposta})

if __name__ == "__main__":
    main()
