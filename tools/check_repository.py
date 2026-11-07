"""Repository checks that do not require Arduino hardware or private credentials."""

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
    for needle in ("char auth[]", "char ssid[]", "char pass[]"):
        assert needle not in source, "Legacy embedded credentials found"

    print("PASS: structure, redaction policy, and documentation checks")
    print("NOTE: hardware/Arduino compilation is not checked here")


if __name__ == "__main__":
    main()
