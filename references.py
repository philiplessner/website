import csv
from typing import List
from pprint import pprint


def csv2list(csvfile: str) -> List:
    rows = list()
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(reader):
            if (i != 0):
                rows.append(row)
    return rows


if __name__ == "__main__":
    references = csv2list("about_me.csv")
    pprint(references)