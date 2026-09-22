"""Run from the repository root: python run_pipeline.py"""
from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH
from src.pipeline import run_pipeline

if __name__ == "__main__":
    cleaned = run_pipeline(RAW_DATA_PATH, PROCESSED_DATA_PATH)
    print(f"Wrote {len(cleaned):,} clean records to {PROCESSED_DATA_PATH}")
