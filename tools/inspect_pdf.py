from pathlib import Path
import sys

from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pdf_path = Path(sys.argv[1] if len(sys.argv) > 1 else "output/pdf/NEXA-Agent-Workspace-技术文档.pdf")
if not pdf_path.exists():
    raise SystemExit(f"PDF not found: {pdf_path}")

reader = PdfReader(str(pdf_path))
print(f"pages={len(reader.pages)}")
for index, page in enumerate(reader.pages, start=1):
    text = (page.extract_text() or "").replace("\n", " | ")
    print(f"\n--- PAGE {index} ---\n{text}")
