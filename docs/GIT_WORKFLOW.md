# Fluxo Git (exigência do Tech Challenge)

Este repositório usa branches por funcionalidade e integração via merge/PR na `main`.

## Branches criadas no desenvolvimento

| Branch | Escopo |
|--------|--------|
| `feat/scaffold` | Estrutura, requirements, mapa das aulas |
| `feat/bronze-ingest` | Amostras + carga Bronze + streaming producer |
| `feat/silver-quality` | Silver + validações |
| `feat/gold-analytics` | Camada Gold + previews |
| `feat/docs-entrega` | README, arquitetura, FinOps, roteiro do vídeo |

## Abrir PR no GitHub (quando o remote existir)

```bash
gh repo create fiap-alfabetiza-fase2 --public --source=. --remote=origin --push
git checkout -b feat/exemplo
# ... alterações ...
git push -u origin HEAD
gh pr create --title "feat: descrição" --body "## Summary
- ...
## Test plan
- [ ] python -m pipelines.run_pipeline --with-streaming
- [ ] python -m pipelines.monitor_health"
```

Merges locais `--no-ff` preservam o histórico de integração semelhante a PRs.
