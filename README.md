# csv-cleaner

A small command-line tool that cleans messy CSV files and prints a summary of what it changed.
Python 3.8+, standard library only, no installation needed.

## What it does

- Trims leading/trailing spaces and collapses repeated spaces in every cell
- Converts dates in mixed formats to ISO format (`YYYY-MM-DD`)
- Lower-cases or Title-Cases the columns you choose (e.g. emails, names, cities)
- Removes rows where required columns are empty
- Removes duplicate rows (compared after cleaning, so `" anna "` and `"Anna"` match)
- Prints a report: rows read/written, duplicates removed, dates fixed, invalid dates

## Usage

```bash
python main.py samples/messy.csv \
    --date-columns signup_date \
    --required name email \
    --lower email \
    --title name city \
    -o cleaned.csv
```

If `-o` is omitted, the result is saved next to the input as `<name>_clean.csv`.

### Example

Input (`samples/messy.csv`, 8 rows):

```
name,email,signup_date,city
  anna   KOVAL ,Anna.Koval@Example.com,2024-03-05,kyiv
Anna Koval,anna.koval@example.com,05.03.2024,KYIV
 Petro Shevchenko,petro@example.com,12/04/2024,  Lviv
...
```

Report:

```
=== Cleaning report ===
Rows read:                8
Rows written:             4
Duplicates removed:       2
Missing required removed: 2
Dates normalized:         4
Invalid dates blanked:    1
```

## Supported date formats

`2024-04-12`, `12.04.2024`, `12/04/2024`, `12-04-2024`, `12 Apr 2024`, `Apr 12, 2024`.
Slash dates are read day-first (`03/04/2024` is 3 April). Dates that cannot be parsed are
left empty and counted in the report.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```
cleaner.py   # cleaning logic (pure functions, easy to test)
main.py      # command-line interface
tests/       # unit tests
samples/     # example messy data
```

## Possible improvements

- Excel (.xlsx) input/output
- Configurable date formats
- Fuzzy duplicate detection
