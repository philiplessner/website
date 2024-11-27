import csv
from collections import namedtuple
from typing import List, Dict
from pprint import pprint


def csv2list(csvfile: str) -> Dict:
    rows = list()
    references = dict()
    Papers = namedtuple('Papers', ['authors', 'title', 'reference', 'date', 'link'])
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(reader):
            if (i != 0):
                rows.append(Papers(*row))
    references.update({"references":rows})
    return references

def print_references(references) -> None:
    for reference in references:
        print(reference.authors)


if __name__ == "__main__":
    references = csv2list("about_me.csv")
#    pprint(references)
    print_references(**references)