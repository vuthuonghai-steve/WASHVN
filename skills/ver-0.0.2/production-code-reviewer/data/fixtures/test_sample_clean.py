"""test_sample_clean.py — unit test đi kèm sample_clean.py (REV-TST-01)."""

import unittest
from sample_clean import BillingService, load_config


class FakeRepository:
    def __init__(self, items):
        self._items = items

    def fetch(self, user_id, timeout=None):
        return type("Record", (), {"items": self._items})()


class BillingServiceTests(unittest.TestCase):
    def test_calculate_total_returns_zero_for_empty_user(self):
        svc = BillingService(FakeRepository([]))
        self.assertEqual(svc.calculate_total(""), 0.0)

    def test_calculate_total_sums_amounts(self):
        items = [type("I", (), {"amount": 10}), type("I", (), {"amount": 20})]
        svc = BillingService(FakeRepository(items))
        self.assertEqual(svc.calculate_total("u1"), 30.0)

    def test_calculate_total_returns_zero_on_io_error(self):
        class BrokenRepo:
            def fetch(self, *a, **kw):
                raise IOError("disk full")

        svc = BillingService(BrokenRepo())
        self.assertEqual(svc.calculate_total("u1"), 0.0)

    def test_load_config_returns_none_on_missing_file(self):
        self.assertIsNone(load_config("/nonexistent/path"))

    def test_load_config_parses_file(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
            tmp.write("hello")
            tmp_path = tmp.name
        try:
            result = load_config(tmp_path)
            self.assertIsNotNone(result)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
