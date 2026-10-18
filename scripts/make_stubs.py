"""Regenerate the package's .pyi stubs (Reflex 0.10 removed `reflex component build`).

Runs Reflex's own stub generator over the package, then fixes what it leaves for this package:
the `Palette` name the `palette=` keyword refers to, and the dynamically built Radix part
classes of `overlays.py` (whose stub is dropped: type checkers read the module itself).

    uv run python scripts/make_stubs.py
"""

import re
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "custom_components" / "reflex_silverpoint_react"
DROP = ("overlays.pyi",)
EXTRA_IMPORTS = {
    "Palette": "from .palette import Palette",
    "Component": "from reflex_base.components.component import Component",
}


def main() -> int:
    subprocess.run([sys.executable, "-m", "reflex_base.utils.pyi_generator", str(PACKAGE)], check=True)
    for name in DROP:
        (PACKAGE / name).unlink(missing_ok=True)
    for stub in sorted(PACKAGE.glob("*.pyi")):
        text = stub.read_text(encoding="utf-8")
        needed = [line for name, line in EXTRA_IMPORTS.items() if re.search(rf"\b{name}\b", text) and line not in text]
        if stub.name == "palette.pyi":
            needed = [line for line in needed if "Palette" not in line]
        if needed:
            marker = "# ------------------------------------------------------\n"
            head, sep, body = text.partition(marker)
            text = head + sep + "\n".join(needed) + "\n" + body if sep else "\n".join(needed) + "\n" + text
            stub.write_text(text, encoding="utf-8")
    ruff = [sys.executable, "-m", "ruff"]
    stubs = [str(p) for p in sorted(PACKAGE.glob("*.pyi"))]
    subprocess.run(
        [
            *ruff,
            "check",
            "--no-cache",
            "--config",
            "extend-exclude=[]",
            "--select",
            "I,UP,PYI",
            "--fix",
            "--unsafe-fixes",
            "-q",
            *stubs,
        ],
        check=False,
    )
    subprocess.run([*ruff, "format", "--no-cache", "--config", "extend-exclude=[]", "-q", *stubs], check=True)
    result = subprocess.run(
        [*ruff, "check", "--no-cache", "--config", "extend-exclude=[]", "--select", "F821", "-q", *stubs], check=False
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
