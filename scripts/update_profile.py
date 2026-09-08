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
    values = [(len(owned), 'PUBLIC ORIGINAL REPOS', '#00f0ff'),
              (stars, 'STARS ON THESE REPOS', '#ff2e97'),
              (langs, 'PRIMARY REPO LANGUAGES', '#00ff9f')]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="180" viewBox="0 0 1000 180"><defs>',
           '<linearGradient id="ag" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#00f0ff"/><stop offset="0.5" stop-color="#a855f7"/><stop offset="1" stop-color="#ff2e97"/></linearGradient>',
           '<linearGradient id="ah" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#00f0ff"/><stop offset="0.5" stop-color="#a855f7"/><stop offset="1" stop-color="#ff2e97"/></linearGradient>',
           '</defs><rect width="1000" height="180" rx="12" fill="#0a0e22"/>',
           '<rect x="1" y="1" width="998" height="178" rx="11" fill="none" stroke="url(#ag)" stroke-opacity="0.7" stroke-width="1.5"/>',
           '<path d="M0 0 V180 M120 0 V180 M240 0 V180" stroke="#00f0ff" stroke-opacity="0.05" fill="none"/>',
           '<text x="30" y="38" fill="#00f0ff" font-family="Consolas, \'Courier New\', monospace" font-size="15" font-weight="700" letter-spacing="3">&gt;&nbsp;GH_ACTIVITY/&nbsp;LIVE.SNAPSHOT</text>']
    for i, (value, label, color) in enumerate(values):
        x = 40 + i * 320
        ax = x + 168
        out.append(f'<text x="{x}" y="98" fill="{color}" font-family="Consolas, \'Courier New\', monospace" font-size="52" font-weight="800">{value}</text>')
        out.append(f'<text x="{x}" y="128" fill="#aab6dc" font-family="Consolas, \'Courier New\', monospace" font-size="12" letter-spacing="1">{label}</text>')
        out.append(f'<path d="M{x} 148 H{ax}" stroke="{color}" stroke-opacity="0.4" stroke-width="2" fill="none"/>')
    out.append(f'<text x="30" y="170" fill="#7f8cb8" font-family="Consolas, \'Courier New\', monospace" font-size="12">Public metadata only / forks excluded / refreshed {escape(stamp)}</text></svg>')
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