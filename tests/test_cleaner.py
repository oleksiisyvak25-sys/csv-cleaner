import unittest

from cleaner import clean_rows, clean_text, normalize_date


class TestCleanText(unittest.TestCase):
    def test_trims_and_collapses_spaces(self):
        self.assertEqual(clean_text("  Ivan   Melnyk "), "Ivan Melnyk")

    def test_none_becomes_empty_string(self):
        self.assertEqual(clean_text(None), "")


class TestNormalizeDate(unittest.TestCase):
    def test_supported_formats(self):
        for raw in ["2024-04-12", "12.04.2024", "12/04/2024", "12 Apr 2024", "Apr 12, 2024"]:
            with self.subTest(raw=raw):
                self.assertEqual(normalize_date(raw), "2024-04-12")

    def test_invalid_returns_none(self):
        self.assertIsNone(normalize_date("not a date"))
        self.assertIsNone(normalize_date(""))


class TestCleanRows(unittest.TestCase):
    def test_removes_duplicates_after_cleaning(self):
        rows = [
            {"name": " anna ", "email": "A@x.com"},
            {"name": "Anna", "email": "a@x.com"},
        ]
        cleaned, stats = clean_rows(rows, lower_columns=["email"], title_columns=["name"])
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(stats.duplicates_removed, 1)

    def test_drops_rows_missing_required(self):
        rows = [{"name": "", "email": "a@x.com"}, {"name": "Bob", "email": "b@x.com"}]
        cleaned, stats = clean_rows(rows, required_columns=["name"])
        self.assertEqual([r["name"] for r in cleaned], ["Bob"])
        self.assertEqual(stats.missing_required_removed, 1)

    def test_invalid_dates_are_blanked_and_counted(self):
        rows = [{"name": "Bob", "date": "garbage"}]
        cleaned, stats = clean_rows(rows, date_columns=["date"])
        self.assertEqual(cleaned[0]["date"], "")
        self.assertEqual(stats.invalid_dates, 1)

    def test_dates_normalized_count(self):
        rows = [{"date": "12.04.2024"}, {"date": "2024-04-13"}]
        cleaned, stats = clean_rows(rows, date_columns=["date"])
        self.assertEqual([r["date"] for r in cleaned], ["2024-04-12", "2024-04-13"])
        self.assertEqual(stats.dates_normalized, 1)  # the second one was already ISO


if __name__ == "__main__":
    unittest.main()