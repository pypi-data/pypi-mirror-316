from pathlib import Path

docs_dir = Path(__file__).parent
readme = docs_dir.parent / "README.md"

with open(readme, "r") as f:
    readme_src = f.read()

index_src = f"""
---
pagetitle: "chatlas"
---

{readme_src}
"""

index = docs_dir / "index.qmd"

with open(index, "w") as f:
    f.write(index_src)
