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

# 4 - CÓDIGO PARA MONTAR CONTEXTO (INCLUINDO METAS DE LONGO PRAZO)
def montar_contexto(df_t, df_d, metas, limites):
    df_t.columns = df_t.columns.str.lower()
    
    contexto = f"USUÁRIO: {metas['usuario']} | RENDA: R$ {metas['renda_mensal']}\n"
    
    # RESERVA ATUAL
    reserva = metas['reserva_emergencia']
    contexto += f"META ATUAL (PRIORIDADE): R$ {reserva['status_atual']} de R$ {reserva['valor_objetivo']} (Reserva de Emergência)\n"
    
    # METAS FUTURAS (LONGO PRAZO)
    contexto += "\nMETAS DE LONGO PRAZO (O QUE VEM DEPOIS DA RESERVA):\n"
    for m in metas.get('metas_longo_prazo', []):
        contexto += f"- {m['descricao']}: Necessário R$ {m['valor_necessario']:.2f} | Prazo: {m['prazo']}\n"
    
    contexto += "\nLIMITES VS GASTOS ATUAIS (VALORES REAIS):\n"
    for item in limites['limites_mensais']:
        cat_nome = item['categoria']
        limite_val = item['limite_maximo']
        filtro = df_t[
            (df_t['valor'] < 0) & 
            ((df_t['categoria'].str.contains(cat_nome, case=False, na=False)) | 
             (df_t['tipo_gasto'].str.contains(cat_nome, case=False, na=False)))
        ]
        gasto_real = abs(filtro['valor'].sum())
        porcentagem = (gasto_real / limite_val) * 100
        status = "⚠️ CRÍTICO" if porcentagem >= 80 else "✅ OK"
        contexto += f"- {cat_nome}: Gasto R$ {gasto_real:.2f} / Limite R$ {limite_val:.2f} ({porcentagem:.1f}% usado - {status})\n"
    
    dica = df_d.sample(1).iloc[0]
    contexto += f"\nDICA PARA O USUÁRIO: {dica['dica']}"
    return contexto

# 5 - CÓDIGO PARA SISTEMA DE PROMPT
def system_prompt(contexto):
    return f"""Você é o Fin, um assistente de planejamento financeiro pessoal empático e consultivo. 
Seu objetivo é ajudar o João Silva a controlar gastos e atingir sua meta de Reserva de Emergência e planos futuros.

DIRETRIZES DE COMPORTAMENTO:
1. ANÁLISE DE DADOS: Sempre consulte o contexto fornecido antes de responder.
2. CÁLCULOS: Se um limite ultrapassou 80%, emita um alerta amigável.
3. PLANEJAMENTO: Quando perguntarem sobre o "depois" ou "metas futuras", consulte a seção 'METAS DE LONGO PRAZO'. Explique que a prioridade é a reserva, mas cite o próximo objetivo (ex: entrada do apartamento).
4. VERACIDADE: Nunca invente transações. Use apenas o que está no contexto.

REGRAS DE SEGURANÇA:
- Não realize transações bancárias nem dê dicas de ações/cripto.
- Se o assunto fugir de finanças, decline educadamente explicando que você é o Fin, focado em ajudar com dinheiro, mencionando o assunto fora de escopo que o usuário trouxe.

ESTRUTURA DE RESPOSTA:
- Use bullet points e tom encorajador.

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

        if prompt := st.chat_input("Como estão minhas metas?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # ÍCONE DE CARREGAMENTO AQUI
                with st.spinner("O Fin está analisando seus dados..."):
                    res_sistema = system_prompt(contexto_real)
                    resposta = chamar_ollama(res_sistema, prompt)
                    st.markdown(resposta)
            
            st.session_state.messages.append({"role": "assistant", "content": resposta})

if __name__ == "__main__":
    main()
