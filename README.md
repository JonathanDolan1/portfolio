# Jonathan Dolan — portfolio

Source for https://jonathan-dolan.vercel.app. Astro 5.16.7, adapted from [Case](https://github.com/erlandv/case), MIT (original license retained). Case supports per-project images through MDX and its image component; this site adds explicit, accessible media slots with build-time file detection.

## Run locally

Use the installed Node 24.21.0. The lockfile preserves the installed versions.

```sh
npm ci
npm run dev
npm run build
npm run preview
```

The dev server normally serves at http://localhost:4321. Preview serves the built static files. Build runs Astro's type check before static generation. No paid service or runtime API is needed to build or view this site.

## Tests

Three Playwright smoke tests in `tests/smoke.spec.ts`. Each runs in Chromium at two window sizes, desktop (1280×800) and phone (390×844), so one run = 6 checks.

1. **Home page** returns 200, shows the name and headline from `site.config.ts`, and logs no console or page errors.
2. **Project cards**: on `/` and `/projects/`, the number of cards equals the number of `.mdx` files in `src/content/projects/` (zero cards fails). Each card's link returns 200 and the page's H1 matches the card title.
3. **Résumé and contact links**: `/resume.pdf` is linked and served as a PDF. The mailto, GitHub and LinkedIn links in the contact section and the footer exactly match `site.config.ts`. External links are checked by address only, never opened.

Tests run against a local production build (`astro build`, then `astro preview` on port 4321). Every non-localhost request is blocked during tests, so they never touch the live site or any outside service.

```sh
npx playwright install chromium   # once per machine
npm test                          # astro check + build, then all smoke tests
```

CI: `.github/workflows/smoke.yml` runs the same `npm test` on every push and pull request. The CI job itself needs the network to install npm packages and Chromium; the tests do not. The workflow does not deploy. Deploys stay manual (`vercel --prod`).

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

Site claims match Jonathan's résumé. `public/resume.pdf` is the English résumé, copied unchanged, and the AI-tools line in `site.config.ts` is copied exactly from it.

Wolt's documented Support Associate title and self-reported Shift Manager responsibilities are distinguished. Igor is personal work built with AI coding agents under Jonathan's direction and review. No personal Python/Linux administration or company production experience is claimed. Trellife was a three-person bootcamp capstone with no asserted individual backend ownership.

## How it works

Astro reads two project MDX files, validates their fields, and turns them into static HTML pages. Case supplies the theme's visual foundation. One source configuration controls public identity and navigation. Empty image slots show explicit placeholders; adding an approved image at the expected path and rebuilding replaces the placeholder. The browser only needs a small theme-toggle script. There is no portfolio backend, account, analytics or runtime AI call.

## Deploy

Hosted on Vercel's free tier. Deploys are manual (`vercel --prod`); pushing to GitHub does not deploy.
