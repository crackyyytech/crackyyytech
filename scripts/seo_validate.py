"""Validate the SEO files in this repo; no external packages.

Checks the XML sitemap, every JSON-LD block in the portfolio head pack,
required meta tags, robots.txt sitemap line, and that no placeholder
YOUR_DEPLOYED_URL strings were left behind. Exits non-zero on any problem
so it can gate CI.
"""
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SEO = ROOT / 'seo'
CANONICAL = 'https://portfolio-crackyyytechs-projects.vercel.app/'

errors = []


def fail(message):
    errors.append(message)


def check_no_placeholder(path):
    text = path.read_text(encoding='utf-8')
    if 'YOUR_DEPLOYED_URL' in text:
        fail(f'{path.name}: still contains the YOUR_DEPLOYED_URL placeholder')
    return text


def check_sitemap():
    path = SEO / 'sitemap.xml'
    check_no_placeholder(path)
    try:
        tree = ElementTree.parse(path)
    except ElementTree.ParseError as exc:
        fail(f'sitemap.xml: invalid XML ({exc})')
        return
    locs = [node.text for node in tree.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if not locs:
        fail('sitemap.xml: no <loc> entries found')
    for loc in locs:
        if not loc.startswith('https://'):
            fail(f'sitemap.xml: <loc> is not https ({loc})')


def check_robots():
    text = check_no_placeholder(SEO / 'robots.txt')
    if 'Sitemap:' not in text:
        fail('robots.txt: missing Sitemap directive')
    if CANONICAL not in text:
        fail('robots.txt: Sitemap does not point at the canonical domain')


def check_head():
    path = SEO / 'portfolio-head.html'
    text = check_no_placeholder(path)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
    if not blocks:
        fail('portfolio-head.html: no JSON-LD blocks found')
    seen = set()
    for i, block in enumerate(blocks, 1):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            fail(f'portfolio-head.html: JSON-LD block {i} is invalid ({exc})')
            continue
        seen.add(data.get('@type'))
    for required in ('Person', 'Organization', 'WebSite', 'FAQPage'):
        if required not in seen:
            fail(f'portfolio-head.html: missing {required} JSON-LD schema')
    for tag in ('rel="canonical"', 'og:title', 'twitter:card', 'hreflang'):
        if tag not in text:
            fail(f'portfolio-head.html: missing {tag}')


def check_files():
    for name in ('robots.txt', 'sitemap.xml', 'llms.txt', 'manifest.webmanifest',
                 'browserconfig.xml', 'humans.txt', 'portfolio-head.html',
                 'SEO-AUDIT.md', 'link-bio.md', 'indexnow-key.txt'):
        if not (SEO / name).exists():
            fail(f'missing seo/{name}')
    if not (SEO / '.well-known' / 'security.txt').exists():
        fail('missing seo/.well-known/security.txt')
    manifest = SEO / 'manifest.webmanifest'
    if manifest.exists():
        try:
            json.loads(manifest.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            fail(f'manifest.webmanifest: invalid JSON ({exc})')


def main():
    if not SEO.is_dir():
        print('seo/ directory not found', file=sys.stderr)
        return 1
    check_files()
    check_sitemap()
    check_robots()
    check_head()
    if errors:
        print('SEO validation failed:')
        for error in errors:
            print(f'  - {error}')
        return 1
    print('SEO validation passed: sitemap, robots, JSON-LD, meta tags and files OK.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
