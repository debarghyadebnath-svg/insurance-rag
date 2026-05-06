import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('../.env')

import database
import embedder
import pdf_parser

for manual in database.get_all_manuals():
    pdf_path = Path('uploads') / f"{manual['id']}_{manual['filename']}"
    if pdf_path.exists():
        print(f"Re-indexing {manual['filename']}...")
        pages = pdf_parser.extract_pages(pdf_path)
        embedder.index_pdf_pages(pages, manual['id'], manual['insurer'], manual['category'], manual['filename'])
        database.set_manual_status(manual['id'], 'active')
        print("Done.")
