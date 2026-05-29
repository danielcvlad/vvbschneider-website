#!/usr/bin/env python3
import subprocess, os

# Read token
token = None
with open(os.path.expanduser('~/.hermes/.env')) as f:
    for line in f:
        stripped = line.strip()
        if stripped.startswith('GITHUB_TOKEN='):
            token = stripped.split('=', 1)[1].strip().strip('"').strip("'")
            break

print(f"Token: {token[:8]}..." if token else "NO TOKEN")

proj = '/home/pi/vvbschneider'
remote_url = f"https://danielcvlad:{token}@github.com/danielcvlad/vvbschneider-website.git"

# Init git
subprocess.run(['git', 'init'], cwd=proj, capture_output=True)
subprocess.run(['git', 'config', 'user.email', 'danielcvlad@gmail.com'], cwd=proj, capture_output=True)
subprocess.run(['git', 'config', 'user.name', 'Daniel Vlad'], cwd=proj, capture_output=True)
subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=proj, capture_output=True)
subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=proj, capture_output=True)

# .gitignore
gitignore = """node_modules/
dist/
.astro/
.env
.env.*
.DS_Store
*.log
.vscode/
"""
with open(f'{proj}/.gitignore', 'w') as f:
    f.write(gitignore)

# Stage all
subprocess.run(['git', 'add', '.'], cwd=proj, capture_output=True)

# Commit
r = subprocess.run(['git', 'commit', '-m', 'Initial commit: VVB Schneider insurance website\n\n- Astro.js static site\n- Home, Produkte, Über Uns+Kontakt, Impressum, Datenschutz pages\n- hCaptcha-protected contact form with Formspree\n- Google Maps embed\n- Responsive, polished CSS\n- German language\n- GitHub Pages deployment ready'], cwd=proj, capture_output=True, text=True)
print("Commit:", r.stdout[-200:])
if r.stderr: print("Stderr:", r.stderr[-200:])

# Push
r = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'], cwd=proj, capture_output=True, text=True)
print("Push stdout:", r.stdout[-300:] if r.stdout else "")
print("Push stderr:", r.stderr[-300:] if r.stderr else "")
print("Return code:", r.returncode)
