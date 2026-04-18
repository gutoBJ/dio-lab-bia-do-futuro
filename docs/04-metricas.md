Avaliação e Métricas
Como Avaliar o Fin
A avaliação do Fin foca na precisão dos cálculos financeiros (extraídos do CSV) e na aderência às metas de poupança do usuário (extraídas do JSON).
Testes de Extração: Validar se o Fin lê corretamente as transações do extrato_transacoes.csv.
Verificação de Alertas: Avaliar se o Fin emite os avisos de 80% do limite configurados no categorias_limites.json.
Métricas de Qualidade
Métrica	O que avalia	Exemplo de teste
Assertividade de Dados	O Fin somou corretamente os gastos do CSV?	Perguntar "Quanto gastei no total?" e conferir com o extrato.
Fidelidade às Metas	As sugestões respeitam a Reserva de Emergência?	Verificar se ele prioriza a meta de R$ 15 mil do JSON.
Uso de Conhecimento	O Fin aplicou as dicas financeiras?	Checar se ele citou uma das frases do dicas_educativas.csv.
Segurança de Escopo	O Fin evitou inventar informações externas?	Perguntar sobre notícias de hoje e ele admitir que só trata de finanças.
Exemplos de Cenários de Teste
Teste 1: Consulta de Gastos (CSV)
Pergunta: "Quanto já gastei com alimentação este mês?"
Resposta esperada: Valor exato somado do arquivo extrato_transacoes.csv.
Resultado: [ ] Correto [ ] Incorreto
Teste 2: Alerta de Limite (JSON + CSV)
Pergunta: "Ainda tenho limite para lazer?"
Resposta esperada: O Fin deve comparar o gasto atual de Lazer com o limite do arquivo categorias_limites.json.
Resultado: [ ] Correto [ ] Incorreto
Teste 3: Meta de Longo Prazo
Pergunta: "Qual minha meta depois da reserva?"
Resposta esperada: Mencionar a "Entrada do apartamento" conforme definido no metas_poupanca.json.
Resultado: [ ] Correto [ ] Incorreto
Teste 4: Fora de Escopo
Pergunta: "Qual a previsão do tempo para amanhã?"
Resposta esperada: O Fin deve informar que é um especialista em finanças e não possui dados meteorológicos.
Resultado: [ ] Correto [ ] Incorreto
Resultados
Após os testes realizados com o modelo local (gpt-oss:latest), registramos:
O que funcionou bem:
A integração com a biblioteca Pandas permitiu que o Fin fizesse cálculos precisos sem alucinações matemáticas.
O tempo de resposta, apesar do modelo pesado, foi estável após o primeiro carregamento.
O que pode melhorar:
Adicionar suporte para múltiplos usuários no futuro.
Melhorar a formatação das tabelas de gastos no chat para facilitar a leitura.
Métricas Técnicas (Observabilidade)
Como o Fin roda localmente via Ollama, monitoramos:
Latência: Tempo entre a pergunta do usuário e a primeira palavra gerada.
Consumo de RAM: Impacto dos 13GB do modelo no hardware local.
Conectividade: Estabilidade da API local (endpoint /api/generate).
[!TIP]
Dica para os testadores: O Fin atua como mentor financeiro do João Silva. Para testá-lo, use os dados fictícios que estão na pasta data/.
