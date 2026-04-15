# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `extrato_transacoes.csv` | CSV | Base principal para análise de gastos, categorização e cálculo de médias mensais |
| `metas_poupanca.json` | JSON | 	Contém os objetivos do usuário (ex: Reserva de Emergência) para guiar as sugestões proativas |
| `categorias_limites.json` | JSON | 	Define os tetos de gastos por categoria (Lazer, Alimentação, Saúde) para o sistema de alertas |
| `dicas_educativas.csv` | CSV | 	Pequenas pílulas de educação financeira usadas para enriquecer as respostas do agente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados foram padronizados para garantir a consistência entre os arquivos. O arquivo de transações foi expandido com a coluna tipo_gasto (Essencial, Impulsivo, Investimento), permitindo uma análise comportamental. As metas foram vinculadas diretamente aos limites de gastos, garantindo que o agente saiba que, se o usuário gastar menos em "Lazer", ele atingirá a "Reserva de Emergência" mais rápido.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

O agente carrega os arquivos metas_poupanca.json e categorias_limites.json diretamente na memória da sessão via Python. Já os arquivos CSV (extrato_transacoes e dicas_educativas) são processados pelo Pandas para filtragem rápida, enviando para a LLM apenas o recorte necessário para a pergunta atual.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são injetados dinamicamente no System Prompt. O agente não recebe o histórico inteiro de uma vez; ele utiliza uma função de busca que identifica a intenção do usuário (ex: "gastei muito com comida?") e traz apenas as linhas relevantes do CSV e o limite correspondente do JSON para o contexto imediato.


---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
[PERFIL DO USUÁRIO]
- Nome: João Silva
- Objetivo: Completar reserva de emergência (Faltam: R$ 5.000,00)
- Meta de economia este mês: R$ 500,00

[STATUS POR CATEGORIA]
- Categoria: Alimentação
- Gasto atual: R$ 635,00 | Limite: R$ 1.200,00 (53% utilizado)

[DICA EDUCACIONAL RELEVANTE]
- "Levar marmitas para o trabalho pode economizar até 40% do seu orçamento de alimentação mensal."

[ÚLTIMAS TRANSAÇÕES]
- 05/11: Restaurante Japonês - R$ 120,00 (Tipo: Impulsivo)
- 12/11: iFood - R$ 65,00 (Tipo: Impulsivo)
```
