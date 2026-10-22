"""Feature-005 (silverpoint): the Claude plugin of this repository (T-248, REQ-555).

One plugin, `reflex-silverpoint`: the skill and the hosted silverpoint MCP server, declared inline in
`plugin.json` (a root `.mcp.json` would connect every session opened in this repository).
"""

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / ".claude-plugin"
VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]


def _read(name: str) -> dict:
    return json.loads((PLUGIN_DIR / name).read_text())


def test_req555_marketplace_lists_one_plugin_from_the_repository_root():
    marketplace = _read("marketplace.json")
    assert marketplace["name"] == "reflex-silverpoint"
    [plugin] = marketplace["plugins"]
    assert plugin["name"] == "reflex-silverpoint"
    assert plugin["source"] == "./"


def test_req555_plugin_holds_the_skill_and_the_hosted_server():
    plugin = _read("plugin.json")
    assert plugin["name"] == "reflex-silverpoint"
    assert plugin["skills"] == ["./skills/reflex-silverpoint"]
    assert (ROOT / "skills" / "reflex-silverpoint" / "SKILL.md").is_file()
    assert plugin["mcpServers"] == {"silverpoint": {"type": "http", "url": "https://silverpointweb.vercel.app/mcp"}}


def test_req555_no_root_mcp_json():
    assert not (ROOT / ".mcp.json").exists()


def test_req555_plugin_versions_are_the_package_version():
    assert _read("plugin.json")["version"] == VERSION
    assert [p["version"] for p in _read("marketplace.json")["plugins"]] == [VERSION]
