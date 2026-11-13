import argparse

from devdocs_ai.config.path import PROCESSED_DATA_DIR, RAW_DATA_DIR
from devdocs_ai.ingestion.pipeline import process_pdf
from devdocs_ai.ingestion.storage import save_chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--owner-id",
        required=True,
        help="ID of the user who owns these documents",
    )

    args = parser.parse_args()

    all_chunks = []

    pdf_files = sorted(RAW_DATA_DIR.glob("*.pdf"))

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        chunks = process_pdf(
            file_path=pdf_path,
            owner_id=args.owner_id,
        )

        print(f"  Chunks: {len(chunks)}")
        all_chunks.extend(chunks)

    output_path = PROCESSED_DATA_DIR / "chunks.jsonl"

    save_chunks(all_chunks, output_path)

    print("\nIngestion completed!")
    print(f"Documents: {len(pdf_files)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Owner ID: {args.owner_id}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
