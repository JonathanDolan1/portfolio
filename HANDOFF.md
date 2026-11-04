# Portfolio scaffold handoff — 4 Nov 2026

- Done: Astro 5 + MIT Case, Igor featured and Trellife second, English support-first Home/About/skills/contact, unchanged résumé PDF and all five image slots.
- Theme: Case 1.1.0, upstream c7072e44ce345f59e47b9fa5fc0f338bf783943d; no fallback.
- Configuration: site.config.ts, re-exported by src/config.ts and imported by astro.config.mjs. Former environment names and equivalents: docs/theme-configuration.md. All environment files skipped unread; .env* ignored.
- Verified: build/type check clean; dev HTTP 200; all four pages checked at 1440px and 390px; links, PDF, theme switch/persistence passed; no browser errors.
- Lighthouse mobile: performance 100, accessibility 100, SEO 100. Reports and screenshots: ~/handoffs/portfolio-*. Current scores cover the placeholder scaffold; rerun after content/assets change.
- Igor checks: heartbeat active today; CalDAV implementation not found; Whisper code/readiness confirmed but today's transcription unverified. Details and three sanitized-module candidates: TODO-igor-showcase.md.
- Open: About/case-study copy and learning points, two SVG diagrams, three reviewed screenshots and accurate alt text, final integration wording, separate sanitized showcase, Trellife privacy/security review, production canonical URL and résumé version-label confirmation.
- Resume source: existing English Jonathan_Dolan_Resume_Path_A_2026-10-30.pdf, copied byte-for-byte; literal v3 suffix absent. Matching DOCX supplied the exact AI-tools line.
- Next: Thursday 5 Nov 10:15, Claude, Opus, medium effort, on the Mac in ~/dev/portfolio. Review the detailed ~/handoffs/2026-11-04-portfolio-scaffold.md, fill marked copy/assets, then rebuild and re-audit.
- Deployment is outside this batch. No public push, new showcase repository, paid activation, runtime modification or message was performed.
