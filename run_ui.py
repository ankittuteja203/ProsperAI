from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


def main() -> None:
    if importlib.util.find_spec("streamlit") is None:
        print("Streamlit is not installed in this Python environment.")
        print()
        print("Install the UI dependency with:")
        print('  py -m pip install -e ".[ui]"')
        print()
        print("Or, from an activated virtual environment:")
        print('  python -m pip install -e ".[ui]"')
        raise SystemExit(1)

    root = Path(__file__).resolve().parent
    app = root / "ui_app.py"
    raise SystemExit(
        subprocess.call(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(app),
                "--server.headless=true",
            ],
            cwd=root,
        )
    )


if __name__ == "__main__":
    main()
