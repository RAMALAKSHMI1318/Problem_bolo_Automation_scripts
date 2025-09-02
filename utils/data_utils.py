import csv
import os

def read_csv(filename: str):
    filepath = os.path.join("data", filename)
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
