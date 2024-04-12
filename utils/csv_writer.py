import csv
from typing import List


class CSVWriter:
    def __init__(self, path):
        self.path = path

    def write_header(self, header: List[str]):
        with open(self.path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

    def add_rows(self, rows: List[List[str]]):
        with open(self.path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
