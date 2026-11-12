# Dados sintéticos de triagem

40 exemplos em português, escritos para este laboratório com assistência de agentes de IA. Nenhum chamado real, dado pessoal ou material de empregadores foi utilizado. Licença MIT, conforme a raiz do repositório.

- `id`: identificador sintético estável.
- `subject`, `body`: texto de entrada.
- `label`: classificação esperada por intenção, não a saída das regras.
- `split`: `dev` (24 exemplos) ou `holdout` (16 exemplos públicos).

Classes: `billing` (financeiro), `access` (acesso), `bug` (defeito), `feature` (pedido de melhoria), `unknown` (sem categoria suficiente) e `ambiguous` (múltiplas intenções sem prioridade definida).

Em negações, o rótulo considera a intenção ativa. Exemplo: "Não preciso de reembolso; só passei para agradecer" pertence a `unknown`, embora a palavra financeira esteja presente. As regras lexicais não compreendem essa distinção.

Este conjunto mede somente comportamento nos exemplos listados. Não tem revisão independente, representatividade estatística ou variedade suficiente para estimar generalização. A divisão pública ajuda a organizar o experimento, mas não substitui um teste cego. Novas iterações devem reservar novos exemplos e registrar quando o conjunto anterior foi consultado.
