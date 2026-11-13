def validate_citations(
    cited_chunk_ids: list[str],
    chunks: list[dict],
) -> list[dict]:

    chunks_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}

    sources = []
    seen_ids = set()

    for chunk_id in cited_chunk_ids:
        if chunk_id in seen_ids:
            continue

        chunk = chunks_by_id.get(chunk_id)

        if chunk is None:
            continue

        seen_ids.add(chunk_id)

        sources.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk.get("source"),
                "page_start": chunk.get("page_start"),
                "page_end": chunk.get("page_end"),
                "section_path": chunk.get("section_path", []),
            }
        )

    return sources
