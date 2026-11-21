import { defineConfig } from '@playwright/test';
import type { ReporterDescription } from '@playwright/test';

const isCI = Boolean(process.env.CI);
const reporters: ReporterDescription[] = [['list']];

if (isCI) {
  reporters.push(['html', { open: 'never' }]);
}

export default defineConfig({
  testDir: './tests',
  forbidOnly: isCI,
  retries: 0,
  reporter: reporters,
  use: {
    baseURL: 'http://localhost:4321',
    browserName: 'chromium',
  },
  projects: [
    {
      name: 'desktop',
      use: {
        viewport: { width: 1280, height: 800 },
      },
    },
    {
      name: 'mobile',
      use: {
        viewport: { width: 390, height: 844 },
        isMobile: true,
        hasTouch: true,
      },
    },
  ],
  webServer: {
    command: 'npx astro preview --port 4321 --host 127.0.0.1',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
