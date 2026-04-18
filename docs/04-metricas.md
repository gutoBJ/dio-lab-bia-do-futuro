# 📊 Avaliação e Métricas do Agente Fin

Este documento descreve o processo de avaliação, as métricas de qualidade e os resultados obtidos durante os testes do agente **Fin**.

---

## 🎯 Como Avaliar o Fin

A avaliação do **Fin** foca na precisão dos cálculos financeiros e na aderência às metas de poupança do usuário, baseando-se nos dados reais fornecidos.

1. **Testes de Extração:** Validação da leitura das transações no arquivo `extrato_transacoes.csv`.
2. **Verificação de Alertas:** Avaliação da proatividade do agente ao identificar limites próximos do fim (80%+) conforme o `categorias_limites.json`.

---

## 📈 Métricas de Qualidade


| Métrica | O que avalia | Exemplo de Teste |
| :--- | :--- | :--- |
| **Assertividade de Dados** | Precisão matemática | O Fin somou corretamente os gastos do CSV? |
| **Fidelidade às Metas** | Alinhamento estratégico | As sugestões respeitam a Reserva de Emergência no JSON? |
| **Uso de Conhecimento** | Enriquecimento de resposta | O Fin aplicou as dicas do `dicas_educativas.csv`? |
| **Segurança de Escopo** | Filtro de alucinação | O Fin evitou inventar informações fora do contexto? |

---

## 🧪 Exemplos de Cenários de Teste

### Teste 1: Consulta de Gastos (CSV)
*   **Pergunta:** *"Quanto já gastei com alimentação este mês?"*
*   **Resposta esperada:** Valor (635) exato somado das linhas de categoria "Alimentação".
*   **Resultado:** `[ X ] Correto` `[ ] Incorreto`

### Teste 2: Alerta de Limite (JSON + CSV)
*   **Pergunta:** *"Ainda tenho limite para lazer?"*
*   **Resposta esperada:** Comparação entre o gasto real e o limite definido no JSON, com alerta se estiver acima de 80%.
*   **Resultado:** `[ X ] Correto` `[ ] Incorreto`

### Teste 3: Meta de Longo Prazo
*   **Pergunta:** *"Qual minha meta depois da reserva?"*
*   **Resposta esperada:** Menção à *"Entrada do apartamento"* conforme o `metas_poupanca.json`.
*   **Resultado:** `[ X ] Correto` `[ ] Incorreto`

### Teste 4: Fora de Escopo
*   **Pergunta:** *"Qual a previsão do tempo para amanhã?"*
*   **Resposta esperada:** Declaração de que o agente é especialista apenas em finanças.
*   **Resultado:** `[ X ] Correto` `[ ] Incorreto`

---

## 📝 Resultados

Após os testes realizados com o modelo local (**gpt-oss:latest**), as conclusões foram:

### ✅ O que funcionou bem
*   A integração com a biblioteca **Pandas** eliminou alucinações matemáticas.
*   O agente seguiu rigidamente o **System Prompt**, mantendo o tom empático.
*   A leitura de arquivos locais em pastas separadas (`/data`) funcionou corretamente.

### ⚠️ O que pode melhorar
*   **Tempo de Resposta:** Devido ao tamanho do modelo (13GB), a latência inicial pode ser otimizada.
*   **UX:** Implementar gráficos visuais no Streamlit para complementar as respostas de texto.

---

## ⚙️ Métricas Técnicas (Observabilidade)

Monitoramento realizado via interface do **Ollama**:

*   **Latência:** Tempo médio de resposta por token.
*   **Consumo de RAM:** Estabilidade do hardware durante o carregamento dos 13GB do modelo.
*   **Conectividade:** Taxa de sucesso das requisições via biblioteca `requests`.

> [!TIP]
> **Dica para os testadores:** O **Fin** atua como mentor financeiro do João Silva. Para realizar testes precisos, utilize os dados fictícios contidos na pasta `/data`.
