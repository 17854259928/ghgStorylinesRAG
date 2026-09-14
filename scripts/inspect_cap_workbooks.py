"""List sheets, dimensions and columns in downloaded CAP workbooks."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK_DIR = ROOT / "data" / "cap" / "raw" / "xlsx"

def main() -> None:
    files = sorted(WORKBOOK_DIR.glob("*.xlsx"))
    if not files:
        raise SystemExit(f"No .xlsx files found in {WORKBOOK_DIR}")
    for path in files:
        print(f"\n{path.name}")
        workbook = pd.ExcelFile(path)
        for sheet in workbook.sheet_names:
            frame = pd.read_excel(path, sheet_name=sheet)
            print(f"  {sheet}: {frame.shape[0]} rows x {frame.shape[1]} columns")
            print("   ", list(map(str, frame.columns)))

if __name__ == "__main__":
    main()

# TODO(CAP-RAG): Add deterministic mappings into interventions and outputs tables.
