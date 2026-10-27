#!/usr/bin/env python3
"""Health and unit tests for EntropyMint. Built by Mourad.Soltani"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPT = ROOT / "entropymint.py"

class TestEntropyMint(unittest.TestCase):
    def run_cli(self, args):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)] + args,
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

    def test_health(self):
        out = self.run_cli(["health", "--json"])
        data = json.loads(out)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["built_by"], "Mourad.Soltani")
        self.assertTrue(data["stdlib_only"])

    def test_mint_password(self):
        out = self.run_cli(["mint", "--mode", "password", "--length", "16", "--json"])
        data = json.loads(out)
        self.assertEqual(data["mode"], "password")
        self.assertEqual(len(data["secret"]), 16)
        self.assertGreater(data["analysis"]["entropy_bits"], 50)
        self.assertEqual(data["built_by"], "Mourad.Soltani")

    def test_mint_passphrase(self):
        out = self.run_cli(["mint", "--mode", "passphrase", "--words", "4", "--json"])
        data = json.loads(out)
        self.assertEqual(data["mode"], "passphrase")
        self.assertIn("-", data["secret"])
        self.assertGreater(data["analysis"]["entropy_bits"], 30)

    def test_mint_apikey(self):
        out = self.run_cli(["mint", "--mode", "apikey", "--length", "40", "--style", "hex", "--json"])
        data = json.loads(out)
        self.assertEqual(data["mode"], "apikey")
        self.assertEqual(len(data["secret"]), 40)
        self.assertTrue(all(c in "0123456789abcdef" for c in data["secret"]))

    def test_analyze(self):
        out = self.run_cli(["analyze", "TestPass123!", "--json"])
        data = json.loads(out)
        self.assertGreater(data["entropy_bits"], 40)
        self.assertIn(data["strength"], ["fair", "strong", "very strong", "excellent"])

    def test_health_plain(self):
        out = self.run_cli(["health"])
        self.assertIn("OK", out)
        self.assertIn("Mourad.Soltani", out)

if __name__ == "__main__":
    unittest.main()
