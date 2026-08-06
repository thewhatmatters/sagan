import { defineConfig } from 'astro/config';

// Static output (Astro's default). Deploy is a separate ticket — no
// adapter, no integrations. `site` set for canonical URL generation only.
export default defineConfig({
  site: 'https://sagan.run',
});
