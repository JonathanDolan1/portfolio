import { readdirSync } from 'node:fs';
import { expect, test } from '@playwright/test';
import { siteConfig } from '../site.config.ts';

const projectFiles = readdirSync(new URL('../src/content/projects/', import.meta.url));
const projectCount = projectFiles.filter((filename) => filename.endsWith('.mdx')).length;

test.beforeEach(async ({ page }) => {
  await page.route('**/*', async (route) => {
    const hostname = new URL(route.request().url()).hostname;

    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      await route.abort();
      return;
    }

    await route.continue();
  });
});

test('home page loads with name and headline', async ({ page }) => {
  const consoleErrors: string[] = [];
  const pageErrors: string[] = [];

  page.on('console', (message) => {
    if (message.type() === 'error') {
      consoleErrors.push(message.text());
    }
  });
  page.on('pageerror', (error) => {
    pageErrors.push(error.message);
  });

  const response = await page.goto('/');
  expect(response).not.toBeNull();
  expect(response!.ok()).toBe(true);
  await expect(page.getByText(siteConfig.author.name).first()).toBeVisible();

  const headline = page.locator('h1#hero-title');
  await expect(headline).toBeVisible();
  const headlineText = (await headline.innerText()).replace(/\s+/g, ' ').trim();
  const titleParts = siteConfig.author.title.split(' & ');

  for (const part of titleParts) {
    const normalizedPart = part.replace(/\s+/g, ' ').trim();
    expect(headlineText).toContain(normalizedPart);
  }

  expect(consoleErrors).toEqual([]);
  expect(pageErrors).toEqual([]);
});

test('every project card opens its page', async ({ page }) => {
  for (const listing of ['/', '/projects/']) {
    await page.goto(listing);
    const caseLinks = page.locator('.project-card a.case-link');
    const count = await caseLinks.count();
    expect(count).toBeGreaterThan(0);
    expect(count).toBe(projectCount);

    const cards = page.locator('.project-card');
    const projects: { href: string; title: string }[] = [];

    for (let index = 0; index < count; index += 1) {
      const card = cards.nth(index);
      const href = await card.locator('a.case-link').getAttribute('href');
      expect(href).not.toBeNull();
      const title = await card.locator('h3 a').innerText();
      projects.push({ href: href!, title });
    }

    for (const project of projects) {
      const response = await page.goto(project.href);
      expect(response).not.toBeNull();
      expect(response!.status()).toBe(200);
      await expect(page.locator('h1')).toHaveText(project.title);
    }
  }
});

test('resume and contact links point where they should', async ({ page, baseURL }) => {
  await page.goto('/');
  const resumeLinks = page.locator(`a[href="${siteConfig.resume}"]`);
  expect(await resumeLinks.count()).toBeGreaterThanOrEqual(1);

  const resumeURL = new URL(siteConfig.resume, baseURL);
  expect(['localhost', '127.0.0.1']).toContain(resumeURL.hostname);
  const response = await page.request.get(siteConfig.resume, { maxRedirects: 0 });
  expect(response.status()).toBe(200);
  expect(response.headers()['content-type']).toContain('application/pdf');

  const contactHrefs = [
    `mailto:${siteConfig.author.email}`,
    siteConfig.social.github,
    siteConfig.social.linkedin,
  ];

  for (const selector of ['#contact', 'footer']) {
    const section = page.locator(selector);

    for (const href of contactHrefs) {
      await expect(section.locator(`a[href="${href}"]`)).toBeVisible();
    }
  }
});
