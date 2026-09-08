"""Refresh a local SVG using public repository metadata; no external packages."""
import json
import os
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen


def fetch(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'crackyyytech-profile'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com' + path, headers=headers), timeout=30) as response:
        return json.load(response)


def render(repos, stamp):
    owned = [r for r in repos if not r.get('fork') and not r.get('private')]
    stars = sum(r.get('stargazers_count', 0) for r in owned)
    langs = len({r['language'] for r in owned if r.get('language')})
    values = [(len(owned), 'PUBLIC ORIGINAL REPOS', '#32e6da'),
              (stars, 'STARS ON THESE REPOS', '#af83ff'),
              (langs, 'PRIMARY REPO LANGUAGES', '#ff73bb')]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="220" viewBox="0 0 1000 220">',
           '<rect width="1000" height="220" rx="20" fill="#0d1224"/>']
    for i, (value, label, color) in enumerate(values):
        x = 30 + i * 330
        out.append(f'<text x="{x}" y="88" fill="{color}" font-family="sans-serif" font-size="48" font-weight="bold">{value}</text>')
        out.append(f'<text x="{x}" y="128" fill="#c8d3ec" font-family="sans-serif" font-size="13">{label}</text>')
    out.append(f'<text x="30" y="185" fill="#a6b5d0" font-family="sans-serif" font-size="13">Public metadata only · forks excluded · refreshed {escape(stamp)}</text></svg>')
    return ''.join(out)


def main():
    repos = []
    page = 1
    while True:
        batch = fetch(f'/users/crackyyytech/repos?type=owner&per_page=100&page={page}')
        if not isinstance(batch, list):
            raise ValueError('Unexpected GitHub API response; preserving existing SVG')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    target = Path(__file__).resolve().parents[1] / 'assets' / 'activity.svg'
    temporary = target.with_suffix('.tmp')
    temporary.write_text(render(repos, datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')), encoding='utf-8')
    temporary.replace(target)

if __name__ == '__main__':
    main()
