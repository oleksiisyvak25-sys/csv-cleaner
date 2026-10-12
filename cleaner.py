from dataclasses import dataclass
from datetime import datetime

date_formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%b %d, %Y"]

@dataclass
class Stats:
    rows_in: int = 0
    rows_out: int = 0
    duplicates_removed: int = 0
    missing_required_removed: int = 0
    dates_normalized: int = 0
    invalid_dates: int = 0

def clean_text(value):
    return " ".join((value or "").split())

def normalize_date(value):
    value = clean_text(value)
    if not value:
        return None
    for fmt in date_formats:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def clean_rows(rows, date_columns=(), required_columns=(),
               lower_columns=(), title_columns=()):
    stats = Stats(rows_in=len(rows))
    cleaned = []
    seen = set()

    for row in rows:
        new_row = {col: clean_text(val) for col, val in row.items()}

        for col in lower_columns:
            if col in new_row:
                new_row[col] = new_row[col].lower()
        for col in title_columns:
            if col in new_row:
                new_row[col] = new_row[col].title()

        for col in date_columns:
            if col not in new_row or not new_row[col]:
                continue
            iso = normalize_date(new_row[col])
            if iso is None:
                stats.invalid_dates += 1
                new_row[col] = ""
            else:
                if iso != new_row[col]:
                    stats.dates_normalized += 1
                new_row[col] = iso

        if any(not new_row.get(col) for col in required_columns):
            stats.missing_required_removed += 1
            continue

        key = tuple(new_row.values())
        if key in seen:
            stats.duplicates_removed += 1
            continue
        seen.add(key)

        cleaned.append(new_row)

    stats.rows_out = len(cleaned)
    return cleaned, stats

def format_report(stats):
    return "\n".join([
        "=== Cleaning report ===",
        f"Rows read:                {stats.rows_in}",
        f"Rows written:             {stats.rows_out}",
        f"Duplicates removed:       {stats.duplicates_removed}",
        f"Missing required removed: {stats.missing_required_removed}",
        f"Dates normalized:         {stats.dates_normalized}",
        f"Invalid dates blanked:    {stats.invalid_dates}",
    ])