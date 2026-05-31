#!/usr/bin/env python3
"""
Push helper — sends the built /dist output to GitHub Pages.

Usage:
    python3 push.py

Requirements:
  - Dist folder must exist (run `npm run build` first)
  - GH_TOKEN env var must be set (your GitHub PAT)
  - git remote must point to danielcvlad/vvbschneider-website
"""

import os
import subprocess

DIST = "dist"
REMOTE_URL = "https://github.com/danielcvlad/vvbschneider-website.git"

def run(cmd, **kwargs):
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(cmd)}")
    return result

token = os.environ.get("GH_TOKEN")
if not token:
    raise SystemExit("GH_TOKEN environment variable is not set.")

# Build
print("Building...")
run(["npm", "run", "build"])

# Copy .nojekyll to dist (GitHub Pages needs this for Astro output)
with open(f"{DIST}/.nojekyll", "w") as f:
    f.write("")

# Push to gh-pages branch
run([
    "gh", "api", "repos/danielcvlad/vvbschneider-website/pages",
    "-X", "POST",
    "-f", "build_type=workflow",
    "--input", "-",
], input=b"", text=False)

print(f"Pushed to: https://danielcvlad.github.io/vvbschneider-website/")