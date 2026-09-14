# ghgStorylinesRAG

Local, evidence-traceable extraction of EU Common Agricultural Policy (CAP)
design, implementation, expenditure, outputs and reported outcomes. The active
prototype uses Ollama with `qwen3.5:9b`; inherited JRC/EMM disaster code is under
`legacy/` for reference only.

## Start here

1. Select `.venv/Scripts/python.exe` in PyCharm.
2. Copy `.env.example` to `.env`.
3. Start Ollama and confirm `qwen3.5:9b` is installed.
4. Run `python scripts/smoke_test_ollama.py`.
5. Run `python scripts/inspect_cap_workbooks.py`.
6. Follow `docs/USAGE_GUIDE_CN.md`.

## Active structure

- `src/ghg_storylines_rag/`: new CAP pipeline code.
- `prompts/`: versioned extraction prompts.
- `data/cap/`: source registry and local data workspace.
- `scripts/`: explicit commands for each stage.
- `docs/`: user guide and inherited project documentation.
- `legacy/`: archived disaster/JRC implementation.

Search `TODO(CAP-RAG)` to find planned implementation points:

```powershell
rg -n "TODO\(CAP-RAG\)" .
```

The LLM extracts auditable variables and evidence. Official workbook counts and
financial totals are computed deterministically. Causal policy effects require
linked emissions, production, price and weather data.
