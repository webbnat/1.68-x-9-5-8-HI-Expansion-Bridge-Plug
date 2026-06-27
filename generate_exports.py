#!/usr/bin/env python3
"""Generate full export package: ANSYS + machine drawings."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

scripts = [
    ROOT / "export" / "ansys" / "generate_ansys_package.py",
    ROOT / "export" / "drawings" / "generate_drawings.py",
]

# Ensure STLs exist
subprocess.run([sys.executable, str(ROOT / "generate_stage3_iris.py")], check=False)
subprocess.run([sys.executable, str(ROOT / "generate_shex_54.py")], check=False)

for s in scripts:
    print(f"\n=== {s.name} ===")
    subprocess.run([sys.executable, str(s)], check=True)

print("\nAll export packages generated.")
