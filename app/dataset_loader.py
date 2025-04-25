import os

import pandas as pd
import argparse
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app import models


def clean_value(value):
    if value == "None" or pd.isna(value):
        return 0
    try:
        return int(str(value).replace("$", "").replace(",", ""))
    except ValueError:
        return 0


def row_to_dict(row):
    return {
        "show_number": row['Show Number'],
        "air_date": datetime.strptime(row['Air Date'], "%Y-%m-%d").date(),
        "round": row['Round'],
        "category": row['Category'],
        "value": clean_value(row['Value']),
        "question": row['Question'],
        "answer": row['Answer'],
    }


def load_questions(url: str, verbose: bool = False, max_value: int = 1200):
    chunk_size = 50000
    batch_size = 500
    session = SessionLocal()
    total_inserted = 0  # Add counter
    total_processed = 0  # Add counter for all processed records

    try:
        for chunk in pd.read_csv(url, chunksize=chunk_size, skipinitialspace=True):
            chunk['Value_numeric'] = chunk['Value'].apply(clean_value)
            filtered = chunk[chunk['Value_numeric'] <= max_value]

            buffer = []

            for _, row in filtered.iterrows():
                try:
                    q_dict = row_to_dict(row)
                    buffer.append(q_dict)

                    if len(buffer) >= batch_size:
                        stmt = insert(models.Question).values(buffer)
                        stmt = stmt.on_conflict_do_nothing(index_elements=['question'])
                        session.execute(stmt)
                        session.commit()
                        total_inserted += len(buffer)
                        if verbose:
                            print(f"{total_inserted} records loaded")
                        buffer.clear()
                except Exception as e:
                    if verbose:
                        print(f"Skipped row due to error: {e}")

            if buffer:
                stmt = insert(models.Question).values(buffer)
                stmt = stmt.on_conflict_do_nothing(index_elements=['question'])
                session.execute(stmt)
                session.commit()
                total_inserted += len(buffer)
                if verbose:
                    print(f"{total_inserted} records loaded")

        print(f"Data load complete. Total loaded: {total_inserted} records")
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load filtered Jeopardy questions into the database.")
    parser.add_argument("--url", type=str,
                        default="https://raw.githubusercontent.com/russmatney/go-jeopardy/master/JEOPARDY_CSV.csv",
                        help="URL to the Jeopardy CSV dataset")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--max-value", type=int, default=1200, help="Maximum value allowed for questions")
    args = parser.parse_args()
    load_questions(args.url, args.verbose, args.max_value)
