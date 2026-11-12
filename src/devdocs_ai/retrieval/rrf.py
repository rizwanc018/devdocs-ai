def reciprocal_rank_fusion(
    dense_results: list[dict],
    bm25_results: list[dict],
    top_k: int = 5,
    k: int = 60,
) -> list[dict]:
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    fused_results = {}

    rankings = [
        ("dense", dense_results),
        ("bm25", bm25_results),
    ]

    for retriever_name, results in rankings:
        for rank, chunk in enumerate(results, start=1):
            chunk_id = chunk.get("chunk_id")

            if not chunk_id:
                raise ValueError("Retrieved chunk has no chunk_id.")

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    **chunk,
                    "rrf_score": 0.0,
                    "retrieved_by": [],
                    "dense_rank": None,
                    "bm25_rank": None,
                }
            else:
                fused_results[chunk_id].update(
                    {
                        key: value
                        for key, value in chunk.items()
                        if key not in ("rrf_score", "retrieved_by")
                    }
                )

            fused_results[chunk_id]["rrf_score"] += 1 / (k + rank)
            fused_results[chunk_id]["retrieved_by"].append(retriever_name)
            fused_results[chunk_id][f"{retriever_name}_rank"] = rank

    ranked_results = sorted(
        fused_results.values(),
        key=lambda item: item["rrf_score"],
        reverse=True,
    )

    return ranked_results[:top_k]
