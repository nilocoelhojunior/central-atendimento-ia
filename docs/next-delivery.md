# Próxima entrega: comparar regras e modelo local

Objetivo: descobrir onde um modelo melhora a classificação e onde acrescenta latência, consumo ou respostas inválidas.

- Selecionar modelo pequeno com licença compatível e registrar versão/quantização/hardware.
- Medir memória e disco antes do download; manter o custo adicional zero.
- Implementar adaptador que preserve categoria, rota, motivo e evidências, sem inventar termos encontrados.
- Rejeitar/registrar JSON inválido, categoria fora do contrato e indisponibilidade do modelo.
- Ampliar casos de desenvolvimento e preparar novos casos reservados antes de ajustar prompts.
- Comparar precisão/recall/F1, abstenção, estrutura válida, latência e recursos nas mesmas entradas.
- Revisar erros semanticamente; não usar outro LLM como único avaliador.
- Documentar resultado negativo se o modelo não superar o baseline.

Concluído quando API, interface, testes, relatório comparativo e limitações estiverem reproduzíveis. Integração de LLM não deve ser anunciada antes de existir e ser validada.
