# Jonathan Dolan — portfolio scaffold

Private, local-only scaffold for the approved 4 Nov 2026 batch. Astro 5.16.7, adapted from [Case](https://github.com/erlandv/case), MIT (original license retained). No fallback theme was used. Case supports per-project images through MDX and its image component; this scaffold adds explicit, accessible media slots with build-time file detection.

## Run locally

Use the installed Node 24.21.0. The lockfile preserves the installed versions.

```sh
npm ci
npm run dev
npm run build
npm run preview
```

The dev server normally serves at http://localhost:4321. Preview serves the built static files. Build runs Astro's type check before static generation. No paid service or runtime API is needed to build or view this site.

## Where to edit

| File | Purpose |
| --- | --- |
| `site.config.ts` | Public identity, links, exact résumé AI-tools line, skills, image dimensions, canonical site URL |
| `astro.config.mjs` | Static Astro build, MDX and sitemap integration; uses the same source configuration |
| `src/content/projects/igor.mdx` | Featured personal project, problem/solution, stack evidence and placeholders |
| `src/content/projects/trellife.mdx` | Second project, three-person bootcamp capstone and placeholders |
| `src/pages/index.astro` | Home, About, skills and contact sections |
| `src/components/MediaSlot.astro` | Real-image-or-placeholder rendering; rebuild after adding assets |
| `src/styles/portfolio.css` | Portfolio adjustments to Case's retained styles |
| `public/images/README.md` | The two diagram and three screenshot paths |
| `docs/theme-configuration.md` | Documented former environment names and source equivalents |

There is no blog, writing, speaking, journey, decision log, testimonial collection, or third project.

## Environment-file exclusion

All `.env*` entries were skipped unread during the source import and are ignored by Git. The upstream environment type declaration was skipped too. Do not create or read environment files. The template's `loadEnv`, environment schema and `import.meta.env` reads were removed. All portfolio settings are ordinary, public source values in `site.config.ts`; `src/config.ts` re-exports them. Original upstream documents in `docs/upstream/` are references only: their environment-file setup instructions do not apply here.

## Content evidence

Claims use `~/Documents/01_Work/Resume_Fact_Bank.md` and the existing English Path A résumé in `~/dev/job-search/Jonathan_Dolan_Resume_Path_A_2026-10-30.docx`. The matching PDF was copied unchanged to `public/resume.pdf` (SHA-256 `5971111bb5d566bf2c9d27d60d1816f46581fb6af5414b8ea34c44387dda3656`). The filename has no explicit v3 suffix; confirm the version label at the copy review. AI tools text was copied exactly from that document.

Wolt's documented Support Associate title and self-reported Shift Manager responsibilities are distinguished. Igor is personal work built with AI coding agents under Jonathan's direction and review. No personal Python/Linux administration or company production experience is claimed. Trellife has no asserted individual backend ownership and no live-demo link.

## Remaining content work

- TODO-CLAUDE: final About copy; problem statements and learning points for both projects; Trellife solution text; final case-study copy and individual contribution review.
- TODO-CLAUDE: two architecture diagrams at the exact paths in `public/images/README.md`.
- TODO-JONATHAN: three reviewed screenshots, then accurate alt text describing the final assets. Copy only approved images into the repository.
- TODO-VERIFY: iCloud CalDAV is not implemented in the inspected Igor code; Whisper code/readiness exists but same-day transcription was not verified. Do not turn either into an unsupported active-integration claim.
- TODO-CLAUDE: prepare the sanitized Igor showcase separately. The planned GitHub address is displayed as a placeholder, not an active link to a nonexistent repository. No showcase repository or source excerpts were created in this batch.
- TODO-CLAUDE: complete Trellife privacy/security review before publication.
- TODO-CLAUDE: set the approved production URL in `site.config.ts` before the separately approved deployment; current canonical/sitemap URLs use localhost deliberately. Rebuild and recheck after copy/assets change.

## Explain it in an interview

Astro reads two project MDX files, validates their fields, and turns them into static HTML pages. Case supplies the theme's visual foundation. One source configuration controls public identity and navigation. Empty image slots show explicit placeholders; adding an approved image at the expected path and rebuilding replaces the placeholder. The browser only needs a small theme-toggle script. There is no portfolio backend, account, analytics or runtime AI call.

## Next step and limits

Next content session: Claude, Opus, medium effort, on the Mac in `~/dev/portfolio`, Thursday 5 Nov at 10:15, following the approved brief. Add verified copy, two SVG diagrams and reviewed screenshots; resolve the explicitly marked evidence/version questions. Deployment to Vercel's free tier is a separate action and was not performed here. Keep the GitHub repository private.
