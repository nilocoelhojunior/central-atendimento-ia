# Arquitetura e evolução

## Implementado

```text
React/TypeScript -> POST /api/triage -> validação Pydantic -> regras lexicais
                                     <- categoria + rota + evidências

CLI de avaliação -> mesmos classificadores -> relatórios JSON com hashes
```

O domínio de triagem não depende de HTTP. A API rejeita campos desconhecidos, entradas vazias e textos acima dos limites. A UI mostra as evidências e informa quando o texto foi alterado depois da classificação. `/api/samples` expõe somente exemplos sintéticos; `/api/health` informa versão e modo.

## Planejado, ainda não implementado

1. Adaptador de modelo local usando o mesmo contrato e avaliação.
2. Rails e PostgreSQL para chamados persistidos, usuários, permissões e histórico.
3. Ingestão, busca e RAG com citações e avaliação por camada.
4. Ferramentas com autorização, aprovação humana, idempotência e limites.
5. MCP, observabilidade, filas e recuperação operacional.

Persistência não foi acrescentada à entrega atual porque ainda não há fluxo que precise salvar dados. Isso mantém o experimento inicial fácil de reproduzir. O servidor não oferece o produto completo, isolamento multiusuário nem proteção suficiente para exposição pública.

## Verificação

Testes de contrato e domínio, avaliação sintética com casos de falha, build TypeScript e validação no navegador. Relatórios de inferência/qualidade não equivalem a teste de carga ou aceite humano. Referências: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) e [avaliação de agentes](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
