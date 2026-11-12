from devdocs_ai.retrieval.metadata_extraction import extract_metadata
from devdocs_ai.retrieval.metadata_filter import filter_chunks
from devdocs_ai.retrieval.validate_metadata import validate_metadata


def apply_metadata_filters(
    query: str,
    chunks: list[dict],
    catalog: dict,
) -> list[dict]:

    extracted_metadata = extract_metadata(query, catalog)
    extracted_metadata = extracted_metadata.model_dump()

    validated_metadata = validate_metadata(extracted_metadata, catalog)
    filtered_chunks = filter_chunks(chunks, validated_metadata)

    return filtered_chunks
