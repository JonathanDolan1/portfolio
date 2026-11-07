import type { APIRoute } from 'astro';
import { siteConfig } from '../config';

export const GET: APIRoute = () => {
  const sitemapURL = new URL('/sitemap-index.xml', siteConfig.url);
  const body = `User-agent: *\nAllow: /\n\nSitemap: ${sitemapURL.href}\n`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
