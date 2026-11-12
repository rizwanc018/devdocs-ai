def filter_chunks(
    chunks: list[dict],
    metadata_filters: dict,
) -> list[dict]:

    if not metadata_filters:
        return chunks

    filtered_chunks = []

    for chunk in chunks:
        matches = True

        sources = metadata_filters.get("source")

        if sources and chunk.get("source") not in sources:
            matches = False

        topics = metadata_filters.get("topic")

        if matches and topics:
            section_path = chunk.get("section_path") or []

            chunk_topics = {
                section.strip().casefold()
                for section in section_path
                if isinstance(section, str)
            }

            requested_topics = {
                topic.strip().casefold() for topic in topics if isinstance(topic, str)
            }

            if not chunk_topics.intersection(requested_topics):
                matches = False

        if matches:
            filtered_chunks.append(chunk)

    return filtered_chunks
