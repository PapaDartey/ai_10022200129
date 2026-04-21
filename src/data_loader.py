

import os
import fitz
import pandas as pd
from .cleaning import clean_election_dataframe, normalise_text


def load_election_data(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Election CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)
    return clean_election_dataframe(df)


def load_budget_pdf(pdf_path):
    """Extract text from the Ghana 2025 Budget PDF if available."""
    if not os.path.exists(pdf_path):
        return []
    doc = fitz.open(pdf_path)
    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = normalise_text(page.get_text("text"))
        if text:
            pages.append({
                "page": page_number,
                "text": text
            })
    return pages
