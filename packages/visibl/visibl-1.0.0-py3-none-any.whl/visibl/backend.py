# python/visibl/backend.py

import os
from pathlib import Path

# Let's assume the Next.js docs folder is:
NEXTJS_DOCS_FOLDER = Path(__file__).parent.parent.parent / "frontend" / "next-app" / "docs"

def generate_docs():
    """
    Sample function that generates or updates documentation files
    in the next-app/docs folder.
    """
    NEXTJS_DOCS_FOLDER.mkdir(exist_ok=True)
    doc_file = NEXTJS_DOCS_FOLDER / "generated_docs.md"

    content = "# Generated Docs\n\nSome new documentation content."
    with open(doc_file, 'w') as f:
        f.write(content)
    
    return str(doc_file)

def auto_generate_docs():
    """
    Another function that automatically generates or modifies docs.
    """
    NEXTJS_DOCS_FOLDER.mkdir(exist_ok=True)
    doc_file = NEXTJS_DOCS_FOLDER / "auto_generated_docs.md"

    content = "# Auto-Generated Docs\n\nAuto content goes here."
    with open(doc_file, 'w') as f:
        f.write(content)

    return str(doc_file)