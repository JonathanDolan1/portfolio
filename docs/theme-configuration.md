# Case configuration migration

Source for these expected variable names: upstream `docs/02-configuration/configuration.md`, retained unread-environment-free at `docs/upstream/configuration.md`; see https://github.com/erlandv/case/blob/main/docs/02-configuration/configuration.md . Names were not obtained from an environment file.

| Documented upstream name | Ordinary source equivalent in `site.config.ts` |
| --- | --- |
| SITE_URL | siteConfig.url; imported by astro.config.mjs for canonical URLs and sitemap |
| SITE_LANGUAGE | siteConfig.language |
| SITE_TITLE | siteConfig.title |
| SITE_DESCRIPTION | siteConfig.description |
| SITE_AUTHOR_NAME | siteConfig.author.name |
| SITE_AUTHOR_TITLE | siteConfig.author.title |
| SITE_AUTHOR_BIO | siteConfig.author.bio |
| SITE_AUTHOR_EMAIL | siteConfig.author.email |
| SITE_AUTHOR_LOCATION | siteConfig.author.location |
| SOCIAL_GITHUB | siteConfig.social.github |
| SOCIAL_LINKEDIN | siteConfig.social.linkedin |
| SOCIAL_TWITTER | siteConfig.social.twitter, empty/unused in v1 |
| SOCIAL_MASTODON | siteConfig.social.mastodon, empty/unused in v1 |
| SOCIAL_BLUESKY | siteConfig.social.bluesky, empty/unused in v1 |

`src/config.ts` re-exports this configuration for components. No loadEnv call, environment schema, process environment access or import.meta.env access remains in application source. `.env.example` and all `.env*` paths were skipped before extraction and never opened. `src/env.d.ts` was also skipped. `.gitignore` ignores `.env*`. This site has no credentials.
