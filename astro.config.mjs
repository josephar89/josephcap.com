import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  site: "https://www.josephcap.com",
  output: "static",
  integrations: [
    react(),
    tailwind({ applyBaseStyles: false }),
  ],
  redirects: {
    "/home": "/",
    "/creatives/about-me": "/about-me",
    "/faith/writings/seraphic-way-of-the-cross_1": "/faith/writings/seraphic-way-of-the-cross",
    "/science/ai-projects/sub_trans": "/science/ai-projects/sub-trans",
  },
});
