import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core.system_info import get_system_info


class SystemInfoTests(unittest.TestCase):
    def test_returns_expected_fields(self):
        info = get_system_info()
        self.assertEqual(
            set(info),
            {"operating_system", "kernel", "architecture", "memory"},
        )

    def test_values_are_non_empty_strings(self):
        for value in get_system_info().values():
            self.assertIsInstance(value, str)
            self.assertTrue(value)


if __name__ == "__main__":
    unittest.main()
