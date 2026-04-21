

import re
import pandas as pd


def normalise_text(value):
    """Clean hidden spaces and repeated whitespace."""
    if pd.isna(value):
        return ""
    text = str(value).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_votes(value):
    """Convert vote values to integers."""
    if pd.isna(value):
        return 0
    text = re.sub(r"[^0-9]", "", str(value))
    return int(text) if text else 0


def clean_percentage(value):
    """Convert percentage strings such as 55.04% to floats."""
    if pd.isna(value):
        return 0.0
    text = str(value).replace("%", "").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def clean_election_dataframe(df):
    """Clean the Ghana election result dataset."""
    cleaned = df.copy()
    cleaned.columns = [normalise_text(c) for c in cleaned.columns]

    for col in ["Old Region", "New Region", "Code", "Candidate", "Party"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].apply(normalise_text)

    cleaned["Year"] = pd.to_numeric(cleaned["Year"], errors="coerce").fillna(0).astype(int)
    cleaned["Votes"] = cleaned["Votes"].apply(clean_votes)
    cleaned["Votes(%)"] = cleaned["Votes(%)"].apply(clean_percentage)
    cleaned = cleaned.drop_duplicates()
    return cleaned
