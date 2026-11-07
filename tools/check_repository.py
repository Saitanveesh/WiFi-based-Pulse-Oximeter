"""Repository checks that do not require Arduino hardware or private credentials."""

import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKETCH = ROOT / "firmware" / "PulseOximeter" / "PulseOximeter.ino"
EXAMPLE = ROOT / "firmware" / "PulseOximeter" / "secrets.example.h"


def main() -> None:
    assert SKETCH.is_file(), "Arduino sketch missing"
    assert EXAMPLE.is_file(), "Local settings example missing"
    assert not (SKETCH.parent / "secrets.h").exists(), "Do not commit real secrets.h"
    assert not (ROOT / "Code for Oximeter.").exists(), "Legacy source must be retired"
    source = SKETCH.read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert '#include "secrets.h"' in source
    assert "WiFi.begin(WIFI_SSID, WIFI_PASSWORD)" in source
    assert "Blynk.config(BLYNK_AUTH_TOKEN)" in source
    assert "Blynk.virtualWrite(V7" in source
    assert "Blynk.virtualWrite(V8" in source
    assert "**/secrets.h" in ignore
    assert "not yet been verified on physical hardware" in readme
    assert "How To Electronics" in readme
    assert (ROOT / "docs" / "PROVENANCE.md").exists()
    assert (ROOT / "LICENSE").exists()
    assert (ROOT / "SECURITY.md").exists()
    banner = ROOT / "docs" / "brand" / "pulse-oximeter-banner.svg"
    assert banner.is_file(), "Project banner missing"
    root = ET.parse(banner).getroot()
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.attrib.get("viewBox") == "0 0 1600 640"
    assert "docs/brand/pulse-oximeter-banner.svg" in readme
    hero = ROOT / "docs" / "brand" / "adobe-pulse-oximeter-cover.jpg"
    assert hero.exists(), "Adobe cover artwork missing"
    assert hero.read_bytes()[:3] == bytes.fromhex("ffd8ff"), "Invalid cover JPEG"
    assert "docs/brand/adobe-pulse-oximeter-cover.jpg" in readme
    assert "hardware%20testing-pending" in readme
    assert (ROOT / "docs" / "BRANDING.md").exists()
    assert "98%" not in banner.read_text(encoding="utf-8"), "Do not display fabricated readings"
    for needle in ("char auth[]", "char ssid[]", "char pass[]"):
        assert needle not in source, "Legacy embedded credentials found"

    print("PASS: structure, redaction policy, and documentation checks")
    print("NOTE: hardware/Arduino compilation is not checked here")


if __name__ == "__main__":
    main()
