import argparse
import csv
import sys
from pathlib import Path

from cleaner import clean_rows, format_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Clean a messy CSV file: trim spaces, fix dates, remove duplicates.")
    parser.add_argument("input", type=Path, help="path to the input CSV file")
    parser.add_argument("-o", "--output", type=Path,
                        help="output file (default: <input>_clean.csv)")
    parser.add_argument("--date-columns", nargs="*", default=[],
                        help="columns to convert to YYYY-MM-DD")
    parser.add_argument("--required", nargs="*", default=[],
                        help="drop rows where any of these columns is empty")
    parser.add_argument("--lower", nargs="*", default=[],
                        help="columns to convert to lower case (e.g. email)")
    parser.add_argument("--title", nargs="*", default=[],
                        help="columns to convert to Title Case (e.g. name city)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if not args.input.exists():
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1

    output = args.output or args.input.with_name(args.input.stem + "_clean.csv")

    with open(args.input, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print("Error: the file is empty.", file=sys.stderr)
            return 1
        fieldnames = [name.strip() for name in reader.fieldnames]
        rows = [{k.strip(): v for k, v in row.items() if k is not None} for row in reader]

    requested = args.date_columns + args.required + args.lower + args.title
    unknown = [col for col in requested if col not in fieldnames]
    if unknown:
        print(f"Error: unknown column(s): {', '.join(unknown)}. "
              f"Available: {', '.join(fieldnames)}", file=sys.stderr)
        return 1

    cleaned, stats = clean_rows(
        rows,
        date_columns=args.date_columns,
        required_columns=args.required,
        lower_columns=args.lower,
        title_columns=args.title,
    )

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)

    print(format_report(stats))
    print(f"Saved to: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())