from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = [
    ROOT / "notebooks" / "01_tfim_trotter_ed_vqe.ipynb",
    ROOT / "notebooks" / "02_fermi_hubbard_opcional.ipynb",
]
OUTPUT_DIR = ROOT / "executed_notebooks"
SKIP_TAGS = {"skip-vqe"}

parser = argparse.ArgumentParser(
    description="Execute Track 3 notebooks while omitting VQE cells."
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="List notebooks and skipped VQE cells without executing anything.",
)
args = parser.parse_args()

if args.dry_run:
    print("Dry run: no notebooks will be executed.")
    print("VQE cells tagged with 'skip-vqe' will be omitted in normal execution.")
    for notebook in NOTEBOOKS:
        nb_json = json.loads(notebook.read_text(encoding="utf-8"))
        code_cells = 0
        skipped_vqe = 0
        for cell in nb_json.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            code_cells += 1
            tags = set(cell.get("metadata", {}).get("tags", []))
            if tags & SKIP_TAGS:
                skipped_vqe += 1
        print(
            f"- {notebook.relative_to(ROOT)}: "
            f"{code_cells} code cells, {skipped_vqe} VQE cells skipped"
        )
else:
    import nbformat
    from nbclient import NotebookClient

    OUTPUT_DIR.mkdir(exist_ok=True)
    for notebook in NOTEBOOKS:
        print(f"Executing {notebook.relative_to(ROOT)}")
        nb = nbformat.read(notebook, as_version=4)
        cleaned_cells = []
        for cell in nb.cells:
            tags = set(cell.get("metadata", {}).get("tags", []))
            if tags & SKIP_TAGS:
                cleaned_cells.append(
                    nbformat.v4.new_markdown_cell(
                        "> Celda VQE omitida durante `run_all.py` para evitar "
                        "ejecutar optimizaciones variacionales. El código queda "
                        "en el notebook fuente para ejecución manual."
                    )
                )
            else:
                cleaned_cells.append(cell)
        nb.cells = cleaned_cells
        client = NotebookClient(
            nb,
            timeout=1200,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        )
        client.execute()
        output_path = OUTPUT_DIR / notebook.name
        nbformat.write(nb, output_path)
        print(f"Saved {output_path.relative_to(ROOT)}")
