import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core.system_info import get_system_info
from main import format_system_info


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
            self.assertTrue(value.strip())

    def test_format_includes_all_system_fields(self):
        info = {
            "operating_system": "Example Linux",
            "kernel": "7.0-test",
            "architecture": "x86_64",
            "memory": "4096 MB",
        }
        formatted = format_system_info(info)
        self.assertIn("Operating system: Example Linux", formatted)
        self.assertIn("Kernel: 7.0-test", formatted)
        self.assertIn("Architecture: x86_64", formatted)
        self.assertIn("Installed memory: 4096 MB", formatted)


if __name__ == "__main__":
    unittest.main()
