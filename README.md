# 📈 Fin: Agente Financeiro Inteligente com IA Local

O **Fin** é um agente financeiro proativo e consultivo projetado para transformar a gestão de finanças pessoais. Diferente de chatbots tradicionais, o Fin utiliza IA Generativa local para analisar dados reais, antecipar necessidades e educar o usuário de forma personalizada, garantindo 100% de privacidade dos dados.

---

## 🎯 Caso de Uso: O Problema e a Solução

### Problema
Muitas pessoas sofrem com a **invisibilidade financeira**: a dificuldade de enxergar para onde o dinheiro vai em tempo real e o quão longe estão de suas metas de longo prazo. Planilhas manuais são cansativas e apps bancários são, muitas vezes, apenas listas de números frios.

### Solução
O **Fin** resolve isso ao atuar como um mentor de bolso que:
- **Analisa Proativamente:** Monitora gastos e avisa antes que o orçamento estoure.
- **Planeja Metas:** Foca na conclusão da Reserva de Emergência e visualiza metas futuras (como a entrada de um apartamento).
- **Educa no Contexto:** Envia dicas financeiras baseadas nos hábitos atuais do usuário.
- **Privacidade Total:** Utiliza o Ollama para processar tudo localmente, sem enviar dados para a nuvem.

---

## 📁 Estrutura do Repositório

```text
lab-agente-financeiro-fin/
│
├── 📄 README.md                 # Visão geral e instruções (este arquivo)
│
├── 📁 data/                     # Base de Conhecimento (Dados Mockados)
│   ├── extrato_transacoes.csv   # Histórico de gastos e receitas
│   ├── dicas_educativas.csv     # Banco de pílulas de conhecimento
│   ├── categorias_limites.json  # Tetos de gastos por categoria
│   └── metas_poupanca.json      # Perfil, Reserva e Metas de longo prazo
│
├── 📁 docs/                     # Documentação Detalhada
│   ├── 01-documentacao-agente.md # Persona, Arquitetura e Segurança
│   ├── 02-base-conhecimento.md   # Estratégia de integração de dados
│   ├── 03-prompts.md             # Engenharia de prompts (System Prompt)
│   ├── 04-metricas.md            # Avaliação de assertividade e métricas
│   └── 05-pitch.md               # Roteiro do pitch de apresentação
│
├── 📁 src/                      # Código Fonte da Aplicação
│   └── app.py                   # Interface Streamlit integrada ao Ollama
Use o código com cuidado.
```
## 🛠️ Tecnologias Utilizadas

| Categoria | Ferramenta |
|---|---|
| LLM Local | Ollama (Modelo: gpt-oss:20b) |
| Interface | Streamlit |
| Processamento | Python e Pandas (Cálculos Determinísticos) |
| Integração | Requests (API Local do Ollama) |

------------------------------
## ⚙️ Como Executar o Projeto## 1. Pré-requisitos

* Ter o Ollama instalado e rodando.
* Ter o modelo carregado no seu terminal:

ollama pull gpt-oss:20b

## 2. Instalação de Dependências
Na raiz do projeto, instale as bibliotecas necessárias:

pip install streamlit pandas requests

## 3. Execução
Navegue até a pasta src/ e inicie a interface:

python -m streamlit run app.py

------------------------------
## 🛡️ Segurança e Estratégia Anti-Alucinação
Para garantir que o Fin seja confiável no setor financeiro, adotamos:

* Cálculos via Pandas: A IA não faz somas complexas "de cabeça". O código Python calcula os gastos e entrega os valores mastigados no contexto.
* System Prompt de Especialista: Instruções rígidas que impedem o agente de falar sobre temas fora do escopo (esportes, clima, etc).
* Contexto Dinâmico: O agente só responde com base no que está nos arquivos da pasta /data. Se não está lá, ele admite que não sabe.

------------------------------
## 📊 Métricas de Sucesso
O agente é avaliado por:

   1. Assertividade: Comparação dos saldos calculados com os dados do CSV.
   2. Taxa de Recusa: Capacidade de negar perguntas fora de contexto.
   3. Engajamento: Eficácia das dicas educativas enviadas durante a conversa.

------------------------------
## 🎤 Pitch
O roteiro para o vídeo de apresentação de 3 minutos, cobrindo o problema, a solução técnica e o impacto social, pode ser encontrado em docs/05-pitch.md.
------------------------------
Projeto desenvolvido para o Desafio de Agentes Financeiros Inteligentes da DIO.
