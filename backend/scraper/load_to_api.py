"""
Reads one or more CSV files and sends them to the FastAPI bulk-insert API.

Run:  python load_to_api.py listings_scraped.csv listings_mock.csv
"""
import csv
import sys
import requests

API_URL = "http://127.0.0.1:8000/listings/bulk"
CHUNK = 200


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(files):
    rows = []
    for p in files:
        rows.extend(load(p))
    print(f"Total rows to upload: {len(rows)}")

    for i in range(0, len(rows), CHUNK):
        chunk = rows[i:i + CHUNK]
        r = requests.post(API_URL, json=chunk, timeout=60)
        r.raise_for_status()
        print(f"Inserted {r.json()['inserted']} rows")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_to_api.py file1.csv [file2.csv ...]")
        sys.exit(1)
    main(sys.argv[1:])
