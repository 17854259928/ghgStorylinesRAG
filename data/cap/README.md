# CAP data workspace

- `source_registry.csv` is version controlled and records provenance.
- `raw/` stores downloaded HTML, PDF and XLSX files and is not committed.
- `extracted/` stores model-produced JSONL and is not committed.
- `final/` stores reviewed analytical tables and is not committed by default.

Never overwrite an official source silently. Record its retrieval date and create
a new version when the source changes.
