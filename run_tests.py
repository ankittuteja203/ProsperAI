from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
os.environ["PYTHONPATH"] = str(SRC)
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
