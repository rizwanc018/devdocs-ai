from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
LANCE_DB_DIR = PROJECT_ROOT / "indexes" / "lancedb"
BM25_INDEXES_DIR = PROJECT_ROOT / "indexes" / "bm25"
EVAL_DATASET_DIR = PROJECT_ROOT / "data" / "evaluation"
