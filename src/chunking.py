

from .cleaning import normalise_text


def election_rows_to_chunks(df):
    """Create one factual chunk per row of the structured election dataset."""
    chunks = []
    for idx, row in df.iterrows():
        text = (
            f"In the {row['Year']} Ghana election, in {row['New Region']}, "
            f"{row['Candidate']} of the {row['Party']} received {row['Votes']:,} votes, "
            f"representing {row['Votes(%)']:.2f}% of valid votes. "
            f"The old region classification is {row['Old Region']} and the code is {row['Code']}."
        )
        chunks.append({
            "chunk_id": f"election_row_{idx}",
            "source": "Election Dataset",
            "text": normalise_text(text),
            "metadata": {
                "chunk_type": "row_result",
                "year": int(row["Year"]),
                "old_region": row["Old Region"],
                "new_region": row["New Region"],
                "code": row["Code"],
                "candidate": row["Candidate"],
                "party": row["Party"],
                "votes": int(row["Votes"]),
                "percentage": float(row["Votes(%)"])
            }
        })
    return chunks


def election_summary_to_chunks(df):
    """Create summary chunks for questions such as 'who won the 2020 election?'.

    Row-level chunks are good for exact facts, but broad questions need aggregate chunks.
    These summaries are still built manually from the dataset, not from an external RAG framework.
    """
    chunks = []

    # National winner per election year
    national = df.groupby(["Year", "Candidate", "Party"], as_index=False)["Votes"].sum()
    for year, year_df in national.groupby("Year"):
        ranked = year_df.sort_values("Votes", ascending=False).reset_index(drop=True)
        winner = ranked.iloc[0]
        runner_up = ranked.iloc[1] if len(ranked) > 1 else None
        total_votes = int(ranked["Votes"].sum())
        margin_text = ""
        if runner_up is not None:
            margin = int(winner["Votes"] - runner_up["Votes"])
            margin_text = (
                f" The runner-up was {runner_up['Candidate']} of the {runner_up['Party']} "
                f"with {int(runner_up['Votes']):,} votes, so the winning margin was {margin:,} votes."
            )
        text = (
            f"National summary for the {int(year)} Ghana election: {winner['Candidate']} of the "
            f"{winner['Party']} won the national popular vote with {int(winner['Votes']):,} votes "
            f"out of {total_votes:,} votes in this dataset.{margin_text}"
        )
        chunks.append({
            "chunk_id": f"election_summary_national_{int(year)}",
            "source": "Election Dataset",
            "text": normalise_text(text),
            "metadata": {"chunk_type": "national_summary", "year": int(year)}
        })

    # Regional winner per year and new region
    regional = df.groupby(["Year", "New Region", "Candidate", "Party"], as_index=False)["Votes"].sum()
    for (year, region), region_df in regional.groupby(["Year", "New Region"]):
        ranked = region_df.sort_values("Votes", ascending=False).reset_index(drop=True)
        winner = ranked.iloc[0]
        runner_up = ranked.iloc[1] if len(ranked) > 1 else None
        extra = ""
        if runner_up is not None:
            extra = f" The runner-up was {runner_up['Candidate']} of the {runner_up['Party']} with {int(runner_up['Votes']):,} votes."
        text = (
            f"Regional summary for the {int(year)} Ghana election in {region}: "
            f"{winner['Candidate']} of the {winner['Party']} won in {region} with {int(winner['Votes']):,} votes."
            f"{extra}"
        )
        chunks.append({
            "chunk_id": f"election_summary_region_{int(year)}_{normalise_text(region).replace(' ', '_')}",
            "source": "Election Dataset",
            "text": normalise_text(text),
            "metadata": {"chunk_type": "regional_summary", "year": int(year), "new_region": region}
        })

    return chunks


def split_words_with_overlap(words, chunk_size, overlap):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(words[start:end])
        if end == len(words):
            break
        start = end - overlap
    return chunks


def budget_pages_to_chunks(pages, chunk_size=350, overlap=60):
    """Chunk budget pages manually using word count and overlap."""
    chunks = []
    for page in pages:
        text = normalise_text(page["text"])
        words = text.split()
        for i, word_chunk in enumerate(split_words_with_overlap(words, chunk_size, overlap)):
            chunk_text = " ".join(word_chunk)
            chunks.append({
                "chunk_id": f"budget_p{page['page']}_{i}",
                "source": "Budget Statement",
                "text": chunk_text,
                "metadata": {
                    "chunk_type": "budget_text",
                    "page": page["page"],
                    "chunk_size": chunk_size,
                    "overlap": overlap
                }
            })
    return chunks


def build_all_chunks(election_df, budget_pages=None):
    budget_pages = budget_pages or []
    chunks = []
    chunks.extend(election_summary_to_chunks(election_df))
    chunks.extend(election_rows_to_chunks(election_df))
    chunks.extend(budget_pages_to_chunks(budget_pages))
    return chunks
