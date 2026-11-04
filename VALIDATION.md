# Scaffold validation — 4 Nov 2026

- Astro 5.16.7 production build passed; type check: 0 errors, 0 warnings, 0 hints (18 files).
- Development server returned HTTP 200 on loopback. Production preview returned HTTP 200 for Home, Projects, Igor and Trellife, the PDF and robots.txt.
- Lighthouse 13.6.0 mobile audit of built Home at 16:14 Israel time: **Performance 100 / Accessibility 100 / SEO 100**. Local report: `~/handoffs/portfolio-lighthouse-home.report.html` and matching JSON. These scores are for the current placeholder scaffold; rerun after final copy and assets.
- Browser checks at 1440px and 390px: all four content pages have one main landmark, one h1, no viewport overflow, no broken images and no clipped navigation. Theme toggle and persistence passed. No browser errors. External browser requests were blocked during QA.
- Home, mobile and Igor screenshots saved under `~/handoffs/portfolio-scaffold-*.png`; visual review completed. Screenshots contain only the scaffold, not Igor runtime material.
- Résumé is one page; extracted PDF text matches the selected DOCX. Copied bytes equal the English source PDF (SHA-256 recorded in README). Literal v3 suffix absent in source filename; final version-label check remains an explicit content-review item.
- Required sensitive-pattern scan found zero matching source files; no environment files exist in project source. `.env*` is ignored. Configurations have no environment reads. The imported environment example and declaration were skipped unread.
- Igor integration findings and their limits are in `TODO-igor-showcase.md`; no runtime source, logs, configured endpoint URLs or personal identifiers were copied into this repository.
- Case provenance: upstream `erlandv/case`, MIT, revision `c7072e44ce345f59e47b9fa5fc0f338bf783943d`, theme version 1.1.0. No fallback.
- No deployment, public push, paid service activation or new showcase repository.
