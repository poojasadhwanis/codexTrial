#!/usr/bin/env python3
"""Compare migration ID lists in two CSV files."""

import argparse
import csv
from typing import Set

def read_ids(csv_path: str) -> Set[str]:
    """Read the first column from a CSV file into a set of ids."""
    ids = set()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                ids.add(row[0].strip())
    return ids

def write_log(missing_in_first: Set[str], missing_in_second: Set[str], log_path: str) -> None:
    """Write missing id information to a log file."""
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write('IDs missing in file1 but present in file2:\n')
        for id_ in sorted(missing_in_first):
            log_file.write(f"{id_}\n")
        log_file.write('\nIDs missing in file2 but present in file1:\n')
        for id_ in sorted(missing_in_second):
            log_file.write(f"{id_}\n")

def main(first_csv: str, second_csv: str, log_path: str) -> None:
    first_ids = read_ids(first_csv)
    second_ids = read_ids(second_csv)

    missing_in_first = second_ids - first_ids
    missing_in_second = first_ids - second_ids

    write_log(missing_in_first, missing_in_second, log_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compare migration ID lists in two CSV files.'
    )
    parser.add_argument('file1', help='First CSV file of migration IDs')
    parser.add_argument('file2', help='Second CSV file of migration IDs')
    parser.add_argument(
        '-o',
        '--output',
        default='comparison.log',
        help='Path of the log file (default: comparison.log)'
    )

    args = parser.parse_args()
    main(args.file1, args.file2, args.output)
