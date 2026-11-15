"""Check that every compiled module that renders ``sp_trigger`` imports it (issue #44).

Reflex compiles a component that reads state into a module of its own under
``.web/app_components/``. ``sp_trigger`` used to be custom code, which Reflex writes into the page
module only, so an overlay controlled from state rendered an undefined ``SilverpointTrigger``.
It is a module now; this reads a compiled app and fails if any module renders the trigger without
importing it. The demo keeps a modal controlled from state with a text trigger, so the stateful
case is always in what CI compiles.

    cd silverpoint_react_demo && uv run reflex compile
    uv run python scripts/check_compiled_trigger.py silverpoint_react_demo/.web
"""

import re
import sys
from pathlib import Path

_RENDERS = re.compile(r"\bjsx\(\s*SilverpointTrigger\b")
_IMPORTS = re.compile(r"import\s*\{[^}]*\bSilverpointTrigger\b[^}]*\}\s*from\s*[\"'][^\"']*trigger\.jsx[\"']")


def check(web: Path) -> list[str]:
    """Find the compiled modules that render the trigger without importing it.

    Args:
        web: The compiled app's ``.web`` directory.

    Returns:
        One line per problem; empty when the compiled app is sound.
    """
    rendering = [
        path
        for path in sorted(web.rglob("*.jsx"))
        if "node_modules" not in path.parts and _RENDERS.search(path.read_text(encoding="utf-8"))
    ]
    problems = [
        f"{path.relative_to(web).as_posix()} renders SilverpointTrigger but does not import SilverpointTrigger"
        for path in rendering
        if not _IMPORTS.search(path.read_text(encoding="utf-8"))
    ]
    if not any("app_components" in path.relative_to(web).parts for path in rendering):
        problems.append("no module under app_components/ renders the trigger: the stateful case of #44 is not compiled")
    return problems


def main() -> int:
    """Run the check on the directory given on the command line.

    Returns:
        The exit code.
    """
    web = Path(sys.argv[1] if len(sys.argv) > 1 else "silverpoint_react_demo/.web")
    if not web.is_dir():
        print(f"error  {web} is not a directory; compile the app first")
        return 1
    problems = check(web)
    for problem in problems:
        print(f"error  {problem}")
    print(f"check_compiled_trigger · {web} · {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
