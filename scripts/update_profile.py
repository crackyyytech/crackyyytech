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
    values = [(len(owned), 'PUBLIC REPOS', '#38b6ff'),
              (stars, 'STARS', '#ff2392'),
              (langs, 'LANGUAGES', '#3bd6a8')]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="200" viewBox="0 0 1000 200"><defs>',
           '<filter id="sh"><feDropShadow dx="0" dy="4" stdDeviation="0" flood-color="#1b1b2f" flood-opacity="0.2"/></filter>',
           '</defs><rect width="1000" height="200" rx="22" fill="#fff7e6"/>',
           '<rect x="3" y="3" width="994" height="194" rx="19" fill="#ffffff"/>',
           '<circle cx="930" cy="30" r="80" fill="#ffc800" opacity="0.15"/><circle cx="60" cy="180" r="70" fill="#38b6ff" opacity="0.15"/>',
           '<text x="34" y="44" fill="#ff2392" font-family="Trebuchet MS, Arial, sans-serif" font-size="18" font-weight="bold">GITHUB SNAPSHOT</text>']
    for i, (value, label, color) in enumerate(values):
        x = 34 + i * 330
        out.append(f'<text x="{x}" y="105" fill="{color}" font-family="Trebuchet MS, Arial, sans-serif" font-size="54" font-weight="bold">{value}</text>')
        out.append(f'<text x="{x+2}" y="140" fill="#1b1b2f" font-family="Trebuchet MS, Arial, sans-serif" font-size="16" font-weight="bold">{label}</text>')
        out.append(f'<rect x="{x}" y="160" width="210" height="10" rx="5" fill="{color}" opacity="0.35"/>')
    out.append(f'<text x="34" y="190" fill="#7a7a8a" font-family="Trebuchet MS, Arial, sans-serif" font-size="12">forks excluded / refreshed {escape(stamp)}</text></svg>')
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