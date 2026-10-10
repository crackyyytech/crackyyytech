# SEO audit & launch checklist — Sudalai Manikandan S / CRACKYYY.TECH

Canonical site: **https://portfolio-crackyyytechs-projects.vercel.app/**
GitHub hub: **https://github.com/crackyyytech**
Entity: **Sudalai Manikandan S — Founder & Owner of CRACKYYY.TECH**

This repo is the GitHub profile hub. It carries the keyword/entity text and
backlinks; the portfolio site carries the technical SEO tags. GitHub sanitises
`<script>` and `<meta>` in READMEs, so **all structured data lives in
`seo/portfolio-head.html`**.

## What is included

| Item | File | Status |
|---|---|---|
| Person + Organization + Service + WebSite + ProfilePage + FAQ + Breadcrumb JSON-LD | `seo/portfolio-head.html` | done |
| Canonical, hreflang (en-IN / ta-IN / x-default), geo, OG, Twitter, robots meta | `seo/portfolio-head.html` | done |
| robots.txt (search + AI crawlers, sitemap) | `seo/robots.txt` | done |
| XML sitemap with image extension | `seo/sitemap.xml` | done |
| AI answer-engine summary | `seo/llms.txt` | done |
| PWA / mobile manifest | `seo/manifest.webmanifest` | done |
| Windows tile config | `seo/browserconfig.xml` | done |
| Team + site metadata | `seo/humans.txt` | done |
| Security contact | `seo/.well-known/security.txt` | done |
| IndexNow key | `seo/indexnow-key.txt` | done |
| Backlink / authority plan | `seo/link-bio.md` | done |
| Automated validation | `scripts/seo_validate.py` + `.github/workflows/seo.yml` | done |

## Deploy steps (portfolio site)

1. Copy the contents of `seo/portfolio-head.html` (**everything inside `<head>`**)
   into the deployed portfolio's `<head>` (Next.js: `app/layout.tsx` metadata +
   a JSON-LD component; static: `index.html`).
2. Copy to the site root: `robots.txt`, `sitemap.xml`, `manifest.webmanifest`,
   `browserconfig.xml`, `humans.txt`, `llms.txt`, `social-preview.png`.
3. Copy `seo/.well-known/security.txt` to `/.well-known/security.txt`.
4. Create a favicon (`/favicon.ico`) and apple-touch-icon.
5. Deploy, then confirm each URL returns 200:
   - `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/.well-known/security.txt`.

## IndexNow (instant indexing for Bing / Yandex / Seznam)

1. Rename `seo/indexnow-key.txt` to `<key>.txt` (the key is the file name and
   its only content) and host it at the site root, e.g.
   `https://portfolio-crackyyytechs-projects.vercel.app/<key>.txt`.
2. Submit once:
   `curl "https://api.indexnow.org/indexnow?url=https://portfolio-crackyyytechs-projects.vercel.app/&key=<key>"`

## Search Console / Webmaster submission

1. Google Search Console — add the portfolio domain (DNS or HTML-file verify),
   submit `/sitemap.xml`, request indexing for `/`.
2. Bing Webmaster Tools — import from Google Search Console, submit the sitemap.
3. (Optional) Yandex Webmaster + IndexNow.

## Measurement

- Search monthly for: `Sudalai Manikandan S Tenkasi`, `crackyyytech`,
  `CRACKYYY.TECH founder`, `Python developer Tenkasi`.
- Track in GSC: impressions, clicks, average position for the entity queries.
- Validate structured data: https://search.google.com/test/rich-results and
  https://validator.schema.org.

## Local validation

```
python scripts/seo_validate.py
```

Runs automatically on every push/PR via `.github/workflows/seo.yml`.
