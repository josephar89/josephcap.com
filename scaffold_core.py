#!/usr/bin/env python3
"""
JosephCap.com Core Project Scaffold (Drop 2 of 3)
Generates Astro + React + Tailwind configs, GitHub Pages CI/CD, Layouts,
Homepage, About Me, and the complete Faith & Multilingual Reader Hub.

Usage:
    python scaffold_core.py
    npm install
    npm run dev
"""

from pathlib import Path

ROOT = Path(".")

FILES = {
    # =========================================================================
    # 1. CONFIG & GITHUB PAGES DEPLOYMENT
    # =========================================================================
    "package.json": r"""{
  "name": "josephcap-website",
  "type": "module",
  "version": "1.0.0",
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "@astrojs/react": "^3.6.2",
    "@astrojs/tailwind": "^5.1.2",
    "@tailwindcss/typography": "^0.5.15",
    "astro": "^4.16.18",
    "lucide-react": "^0.460.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "tailwindcss": "^3.4.15"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1"
  }
}
""",
    "astro.config.mjs": r"""import { defineConfig } from "astro/config";
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
""",
    "tailwind.config.mjs": r"""import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', '"Noto Sans Tamil"', "system-ui", "sans-serif"],
        serif: ['"Merriweather"', '"Noto Serif Tamil"', "Georgia", "serif"],
      },
    },
  },
  plugins: [typography],
};
""",
    "tsconfig.json": r"""{
  "extends": "astro/tsconfigs/base",
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react"
  }
}
""",
    "public/CNAME": r"""www.josephcap.com
""",
    "public/robots.txt": r"""User-agent: *
Allow: /
Sitemap: https://www.josephcap.com/sitemap-index.xml
""",
    ".gitignore": r"""node_modules/
dist/
.astro/
.DS_Store
.env
*.pyc
__pycache__/
""",
    ".github/workflows/deploy.yml": r"""name: Deploy josephcap.com to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install, build, and upload Astro site
        uses: withastro/action@v3
        with:
          node-version: 20

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
""",
    # =========================================================================
    # 2. STYLES & CONTENT COLLECTION SCHEMAS
    # =========================================================================
    "src/styles/global.css": r"""@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: smooth;
    font-family: "Inter", "Noto Sans Tamil", system-ui, sans-serif;
  }
  body {
    @apply bg-stone-950 text-stone-100 antialiased selection:bg-amber-500/30 selection:text-amber-200;
  }
}

/* Reader theme modes for Magnifica Humanitas & Seraphic Way of the Cross */
.reader-surface[data-theme="dark"] {
  @apply bg-stone-900/70 text-stone-200 border-stone-800;
}
.reader-surface[data-theme="sepia"] {
  background-color: #f6efe2;
  color: #2b2118;
  border-color: #dfcfb3;
}
.reader-surface[data-theme="light"] {
  background-color: #ffffff;
  color: #1c1917;
  border-color: #e7e5e4;
}
.reader-surface[data-theme="sepia"] .prose,
.reader-surface[data-theme="light"] .prose {
  --tw-prose-body: #292524;
  --tw-prose-headings: #1c1917;
  --tw-prose-bold: #1c1917;
  --tw-prose-links: #b45309;
  --tw-prose-quotes: #44403c;
  --tw-prose-hr: #d6d3d1;
}
""",
    "src/content/config.ts": r"""import { defineCollection, z } from "astro:content";

const magnificaHumanitas = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    order: z.number(),
    prev: z.string().nullable().optional(),
    next: z.string().nullable().optional(),
  }),
});

const seraphicWay = defineCollection({
  type: "content",
  schema: z.object({
    langCode: z.string(),
    englishName: z.string(),
    nativeName: z.string(),
    title: z.string(),
    aiTranslated: z.boolean().optional().default(false),
    needsReview: z.boolean().optional().default(false),
  }),
});

const writings = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    language: z.string().optional().default("Tamil"),
    category: z.string().optional(),
  }),
});

export const collections = {
  "magnifica-humanitas": magnificaHumanitas,
  "seraphic-way": seraphicWay,
  writings,
};
""",
    # =========================================================================
    # 3. BASE LAYOUT & E-READER LAYOUT
    # =========================================================================
    "src/layouts/BaseLayout.astro": r"""---
import "../styles/global.css";

interface Props {
  title: string;
  description?: string;
  ogImage?: string;
}

const {
  title,
  description = "Personal portal of Fr. Joseph Arputha Raj OFM Cap — Capuchin Priest, DBIMA Paris Filmmaker, Tamil Sacred Musician, and Global AI Educator.",
  ogImage = "https://lh3.googleusercontent.com/d/1WKD-aqy7hxTtGc4Us16XzKQHZZgzhjSJ",
} = Astro.props;

const currentPath = Astro.url.pathname;

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/faith", label: "Faith" },
  { href: "/art/cinema", label: "Cinema" },
  { href: "/art/music/vetrisaipadal", label: "Music & Karaoke" },
  { href: "/science/ai-projects", label: "AI Lab" },
  { href: "/science/ai-workshops", label: "Workshops" },
  { href: "/about-me", label: "About Me" },
];
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} | Fr. Joseph Arputha Raj OFM Cap</title>
    <meta name="description" content={description} />
    <meta property="og:title" content={`${title} | Fr. Joseph Arputha Raj`} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={ogImage} />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
  </head>
  <body class="flex min-h-screen flex-col bg-stone-950 text-stone-100">
    <!-- Sticky Header -->
    <header class="sticky top-0 z-40 border-b border-stone-800/80 bg-stone-950/90 backdrop-blur-md">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6 lg:px-8">
        <a href="/" class="group flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center rounded-xl border border-amber-500/40 bg-amber-500/15 font-bold text-amber-400 transition group-hover:bg-amber-500 group-hover:text-stone-950">
            JR
          </div>
          <div>
            <p class="text-sm font-bold tracking-tight text-white">
              Fr. Joseph Arputha Raj
            </p>
            <p class="text-[11px] font-medium text-amber-400/90">
              OFM Cap • Faith • Cinema • AI
            </p>
          </div>
        </a>

        <!-- Desktop Navigation -->
        <nav class="hidden items-center gap-1 lg:flex" aria-label="Main navigation">
          {navLinks.map((link) => {
            const isActive =
              link.href === "/"
                ? currentPath === "/"
                : currentPath.startsWith(link.href);
            return (
              <a
                href={link.href}
                class={`rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                  isActive
                    ? "bg-amber-500/15 text-amber-300"
                    : "text-stone-300 hover:bg-stone-900 hover:text-white"
                }`}
              >
                {link.label}
              </a>
            );
          })}
        </nav>

        <!-- Mobile Menu Toggle -->
        <button
          id="mobile-menu-btn"
          type="button"
          aria-label="Toggle navigation menu"
          class="inline-flex items-center justify-center rounded-lg border border-stone-800 bg-stone-900 p-2 text-stone-300 hover:text-white lg:hidden"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <!-- Mobile Drawer -->
      <div id="mobile-menu" class="hidden border-t border-stone-800 bg-stone-950 px-4 py-3 lg:hidden">
        <div class="flex flex-col space-y-1">
          {navLinks.map((link) => (
            <a
              href={link.href}
              class="rounded-lg px-3 py-2 text-sm font-medium text-stone-300 hover:bg-stone-900 hover:text-amber-300"
            >
              {link.label}
            </a>
          ))}
        </div>
      </div>
    </header>

    <!-- Page Body -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="mt-20 border-t border-stone-800/80 bg-stone-950/95">
      <div class="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 md:grid-cols-3 lg:px-8">
        <div>
          <p class="text-base font-bold text-white">Fr. Joseph Arputha Raj OFM Cap</p>
          <p class="mt-2 text-xs leading-relaxed text-stone-400">
            "எல்லாருக்கும் எல்லாமாக" — 1 கொரி 9:22.<br />
            Bridging Franciscan spirituality, visual cinema at DBIMA Paris, Tamil devotional heritage, and ethical Generative AI.
          </p>
        </div>
        <div class="grid grid-cols-2 gap-4 text-xs">
          <div class="space-y-2">
            <p class="font-semibold uppercase tracking-wider text-amber-400">Explore</p>
            <ul class="space-y-1.5 text-stone-400">
              <li><a href="/faith/magnifica-humanitas" class="hover:text-white">Magnifica Humanitas</a></li>
              <li><a href="/faith/writings/seraphic-way-of-the-cross" class="hover:text-white">Seraphic Way (12 Langs)</a></li>
              <li><a href="/faith/archives" class="hover:text-white">Philosophy & Theology</a></li>
              <li><a href="/art/history" class="hover:text-white">Malayadipatty & Family Tree</a></li>
            </ul>
          </div>
          <div class="space-y-2">
            <p class="font-semibold uppercase tracking-wider text-amber-400">Media & AI</p>
            <ul class="space-y-1.5 text-stone-400">
              <li><a href="/art/music/vetrisaipadal" class="hover:text-white">Vetrisaipadal Karaoke</a></li>
              <li><a href="/art/music/albums" class="hover:text-white">Original Albums</a></li>
              <li><a href="/art/cinema" class="hover:text-white">DBIMA Paris Films</a></li>
              <li><a href="/science/ai-workshops" class="hover:text-white">Global AI Workshops</a></li>
            </ul>
          </div>
        </div>
        <div class="space-y-2 text-xs text-stone-400">
          <p class="font-semibold uppercase tracking-wider text-amber-400">Connect</p>
          <p>Fraternité des Capucins, 32 rue Boissonade, 75014 Paris / Tamil Nadu, India</p>
          <div class="flex flex-wrap gap-3 pt-2">
            <a href="mailto:josephar89@gmail.com" class="rounded-md border border-stone-800 px-2.5 py-1 hover:border-amber-500/60 hover:text-white">Email</a>
            <a href="https://www.linkedin.com/in/josephar89" target="_blank" rel="noopener" class="rounded-md border border-stone-800 px-2.5 py-1 hover:border-amber-500/60 hover:text-white">LinkedIn</a>
            <a href="https://www.youtube.com/@Fr.JosephArRa" target="_blank" rel="noopener" class="rounded-md border border-stone-800 px-2.5 py-1 hover:border-amber-500/60 hover:text-white">YouTube</a>
            <a href="https://www.youtube.com/@Vetrisaipadal" target="_blank" rel="noopener" class="rounded-md border border-stone-800 px-2.5 py-1 hover:border-amber-500/60 hover:text-white">Vetrisaipadal</a>
          </div>
        </div>
      </div>
      <div class="border-t border-stone-900 py-4 text-center text-xs text-stone-500">
        © {new Date().getFullYear()} Fr. Joseph Arputha Raj OFM Cap • Hosted on GitHub Pages
      </div>
    </footer>

    <script is:inline>
      const btn = document.getElementById("mobile-menu-btn");
      const menu = document.getElementById("mobile-menu");
      btn?.addEventListener("click", () => menu?.classList.toggle("hidden"));
    </script>
  </body>
</html>
""",
    "src/layouts/ReaderLayout.astro": r"""---
import BaseLayout from "./BaseLayout.astro";

interface NavItem {
  href: string;
  label: string;
  active?: boolean;
}

interface Props {
  title: string;
  subtitle?: string;
  badge?: string;
  backHref: string;
  backLabel: string;
  sidebarTitle?: string;
  sidebarItems?: NavItem[];
  prev?: { href: string; label: string } | null;
  next?: { href: string; label: string } | null;
}

const {
  title,
  subtitle,
  badge,
  backHref,
  backLabel,
  sidebarTitle = "Chapters",
  sidebarItems = [],
  prev = null,
  next = null,
} = Astro.props;
---

<BaseLayout title={title} description={subtitle || title}>
  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <!-- Top Breadcrumb & Reader Toolbar -->
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4 border-b border-stone-800 pb-4">
      <a
        href={backHref}
        class="inline-flex items-center gap-2 text-xs font-semibold text-amber-400 hover:text-amber-300"
      >
        ← {backLabel}
      </a>

      <!-- Font Size & Theme Controls -->
      <div class="flex flex-wrap items-center gap-2">
        <div class="inline-flex items-center rounded-lg border border-stone-800 bg-stone-900 p-1 text-xs">
          <button id="font-dec" type="button" class="rounded px-2.5 py-1 text-stone-300 hover:bg-stone-800 hover:text-white" title="Decrease font size">A-</button>
          <button id="font-reset" type="button" class="rounded px-2 py-1 text-stone-400 hover:bg-stone-800 hover:text-white" title="Default font size">A</button>
          <button id="font-inc" type="button" class="rounded px-2.5 py-1 text-stone-300 hover:bg-stone-800 hover:text-white" title="Increase font size">A+</button>
        </div>

        <div class="inline-flex items-center rounded-lg border border-stone-800 bg-stone-900 p-1 text-xs">
          <button data-set-theme="dark" type="button" class="rounded px-2.5 py-1 text-stone-300 hover:bg-stone-800">Dark</button>
          <button data-set-theme="sepia" type="button" class="rounded px-2.5 py-1 text-amber-200 hover:bg-stone-800">Sepia</button>
          <button data-set-theme="light" type="button" class="rounded px-2.5 py-1 text-stone-100 hover:bg-stone-800">Light</button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-8 lg:grid-cols-12">
      <!-- Optional Sidebar TOC -->
      {sidebarItems.length > 0 && (
        <aside class="lg:col-span-3">
          <div class="sticky top-24 rounded-2xl border border-stone-800 bg-stone-900/60 p-4">
            <p class="mb-3 text-xs font-bold uppercase tracking-wider text-amber-400">
              {sidebarTitle}
            </p>
            <nav class="flex max-h-[65vh] flex-col space-y-1 overflow-y-auto pr-1">
              {sidebarItems.map((item) => (
                <a
                  href={item.href}
                  class={`rounded-lg px-3 py-2 text-xs leading-snug transition ${
                    item.active
                      ? "bg-amber-500/20 font-semibold text-amber-300"
                      : "text-stone-400 hover:bg-stone-800/70 hover:text-stone-100"
                  }`}
                >
                  {item.label}
                </a>
              ))}
            </nav>
          </div>
        </aside>
      )}

      <!-- Main E-Reader Paper Surface -->
      <article class={sidebarItems.length > 0 ? "lg:col-span-9" : "mx-auto w-full max-w-4xl lg:col-span-12"}>
        <div
          id="reader-surface"
          data-theme="dark"
          class="reader-surface rounded-2xl border p-6 shadow-xl transition-colors duration-200 sm:p-10"
        >
          <header class="mb-8 border-b border-current/15 pb-6">
            {badge && (
              <span class="mb-3 inline-block rounded-full border border-amber-500/40 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-500">
                {badge}
              </span>
            )}
            <h1 class="text-2xl font-extrabold leading-tight sm:text-3xl">
              {title}
            </h1>
            {subtitle && (
              <p class="mt-2 text-sm opacity-75">{subtitle}</p>
            )}
          </header>

          <div
            id="reader-prose"
            class="prose prose-invert max-w-none leading-loose prose-headings:scroll-mt-24 prose-a:text-amber-400 prose-img:mx-auto prose-img:rounded-xl prose-img:shadow-lg"
            style="font-size: 17px;"
          >
            <slot />
          </div>

          <!-- Chapter Prev/Next Footer -->
          {(prev || next) && (
            <div class="mt-12 grid grid-cols-1 gap-4 border-t border-current/15 pt-6 sm:grid-cols-2">
              <div>
                {prev && (
                  <a
                    href={prev.href}
                    class="block rounded-xl border border-amber-500/30 p-4 text-left transition hover:bg-amber-500/10"
                  >
                    <span class="block text-[11px] uppercase tracking-wider opacity-60">← Previous</span>
                    <span class="mt-1 block text-sm font-semibold text-amber-500">{prev.label}</span>
                  </a>
                )}
              </div>
              <div>
                {next && (
                  <a
                    href={next.href}
                    class="block rounded-xl border border-amber-500/30 p-4 text-right transition hover:bg-amber-500/10"
                  >
                    <span class="block text-[11px] uppercase tracking-wider opacity-60">Next →</span>
                    <span class="mt-1 block text-sm font-semibold text-amber-500">{next.label}</span>
                  </a>
                )}
              </div>
            </div>
          )}
        </div>
      </article>
    </div>
  </div>

  <script is:inline>
    const surface = document.getElementById("reader-surface");
    const prose = document.getElementById("reader-prose");
    let size = Number(localStorage.getItem("jc_reader_size") || 17);
    const savedTheme = localStorage.getItem("jc_reader_theme") || "dark";

    function applyFont() {
      if (prose) prose.style.fontSize = size + "px";
      localStorage.setItem("jc_reader_size", String(size));
    }
    function applyTheme(theme) {
      if (!surface || !prose) return;
      surface.setAttribute("data-theme", theme);
      if (theme === "dark") {
        prose.classList.add("prose-invert");
      } else {
        prose.classList.remove("prose-invert");
      }
      localStorage.setItem("jc_reader_theme", theme);
    }

    applyFont();
    applyTheme(savedTheme);

    document.getElementById("font-dec")?.addEventListener("click", () => {
      size = Math.max(13, size - 2);
      applyFont();
    });
    document.getElementById("font-reset")?.addEventListener("click", () => {
      size = 17;
      applyFont();
    });
    document.getElementById("font-inc")?.addEventListener("click", () => {
      size = Math.min(26, size + 2);
      applyFont();
    });
    document.querySelectorAll("[data-set-theme]").forEach((btn) => {
      btn.addEventListener("click", () => {
        applyTheme(btn.getAttribute("data-set-theme") || "dark");
      });
    });
  </script>
</BaseLayout>
""",
    # =========================================================================
    # 4. HOMEPAGE (/) & ABOUT ME (/about-me)
    # =========================================================================
    "src/pages/index.astro": r"""---
import BaseLayout from "../layouts/BaseLayout.astro";

const pillars = [
  {
    title: "Faith & Vocation",
    subtitle: "Franciscan Spirituality & Publications",
    desc: "Rooted in the Franciscan path of simplicity from Malayadipatti to Paris. Explore the complete Tamil translation of Pope Leo XIV's Magnifica Humanitas, the 12-language Seraphic Way of the Cross, and my Philosophy & Theology archives.",
    links: [
      { label: "Magnifica Humanitas (Tamil)", href: "/faith/magnifica-humanitas" },
      { label: "Seraphic Way (12 Languages)", href: "/faith/writings/seraphic-way-of-the-cross" },
      { label: "AI Priest Open Letter", href: "/faith/writings/ai-priest" },
      { label: "Philosophy & Theology PDFs", href: "/faith/archives" },
    ],
    cta: { label: "Enter Faith Hub", href: "/faith" },
  },
  {
    title: "Art & History",
    subtitle: "DBIMA Cinema, Sacred Music & Heritage",
    desc: "Creating modern 'Digital Parables' through film, Carnatic-inspired liturgical hymns, 500+ AI-separated Tamil Catholic karaoke tracks, and the 350-year digital chronicle of Malayadipatty.",
    links: [
      { label: "DBIMA Paris Cinema Portfolio", href: "/art/cinema" },
      { label: "Vetrisaipadal (500+ Karaoke)", href: "/art/music/vetrisaipadal" },
      { label: "Original Music Albums", href: "/art/music/albums" },
      { label: "Malayadipatty & Family Tree", href: "/art/history" },
    ],
    cta: { label: "Explore Cinema & Music", href: "/art/cinema" },
  },
  {
    title: "Tech & AI",
    subtitle: "Algorethics & Global AI Education",
    desc: "Guided by the Church's call for ethical technology, democratizing AI literacy through hands-on workshops across India, France, Italy, and Cameroon alongside open-source media & localization workflows.",
    links: [
      { label: "14 Applied AI Case Studies", href: "/science/ai-projects" },
      { label: "Global AI Workshops (15+)", href: "/science/ai-workshops" },
      { label: "Varayan AI Subtitle Pipeline", href: "/science/ai-projects/sub-trans" },
      { label: "Executive CV & Credentials", href: "/about-me" },
    ],
    cta: { label: "Explore AI Lab", href: "/science/ai-projects" },
  },
];

const stats = [
  { value: "600+", label: "AI Karaoke Tracks Engineered" },
  { value: "15+", label: "Global AI Workshops (4 Countries)" },
  { value: "50,000+", label: "EdTech Learners & Archived Pages" },
  { value: "12", label: "Languages in Seraphic Way of the Cross" },
];
---

<BaseLayout title="Home">
  <!-- Hero Section -->
  <section class="relative overflow-hidden border-b border-stone-800/80">
    <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(245,158,11,0.16),_transparent_60%)]" />
    <div class="mx-auto grid max-w-7xl items-center gap-10 px-4 py-16 sm:px-6 lg:grid-cols-12 lg:px-8 lg:py-24">
      <div class="lg:col-span-7">
        <span class="inline-flex items-center gap-2 rounded-full border border-amber-500/40 bg-amber-500/10 px-3.5 py-1 text-xs font-semibold text-amber-300">
          Capuchin Friar • Filmmaker (DBIMA Paris) • AI Integration Specialist
        </span>
        <h1 class="mt-5 text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
          Fr. Joseph Arputha Raj
          <span class="block text-amber-400">OFM Cap</span>
        </h1>
        <p class="mt-4 text-lg font-medium text-stone-300">
          &ldquo;எல்லாருக்கும் எல்லாமாக&rdquo; — 1 கொரி 9:22
        </p>
        <p class="mt-4 max-w-2xl text-base leading-relaxed text-stone-400">
          My humble religious journey as a Capuchin friar—bridging ancient Franciscan spirituality,
          contemporary cinema in Paris, Tamil sacred music, and ethical Generative AI to serve communities worldwide.
        </p>
        <div class="mt-8 flex flex-wrap gap-3">
          <a
            href="/about-me"
            class="rounded-xl bg-amber-500 px-6 py-3 text-sm font-bold text-stone-950 transition hover:bg-amber-400"
          >
            About Me &amp; CV
          </a>
          <a
            href="/art/music/vetrisaipadal"
            class="rounded-xl border border-stone-700 bg-stone-900 px-6 py-3 text-sm font-semibold text-white transition hover:border-amber-500/60 hover:text-amber-300"
          >
            Open Vetrisaipadal Karaoke
          </a>
          <a
            href="/science/ai-workshops"
            class="rounded-xl border border-stone-700 bg-stone-900 px-6 py-3 text-sm font-semibold text-white transition hover:border-amber-500/60 hover:text-amber-300"
          >
            Global AI Workshops
          </a>
        </div>
      </div>

      <div class="lg:col-span-5">
        <div class="relative overflow-hidden rounded-3xl border border-stone-800 bg-stone-900/80 p-3 shadow-2xl">
          <img
            src="https://lh3.googleusercontent.com/d/1WKD-aqy7hxTtGc4Us16XzKQHZZgzhjSJ"
            alt="Fr. Joseph Arputha Raj Banner"
            class="aspect-[4/3] w-full rounded-2xl object-cover"
          />
          <div class="mt-3 flex items-center justify-between px-2 py-1 text-xs text-stone-400">
            <span>Paris, France &amp; Tamil Nadu, India</span>
            <span class="font-semibold text-amber-400">Pax et Bonum</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Impact Metrics Bar -->
  <section class="border-b border-stone-800/80 bg-stone-900/40">
    <div class="mx-auto grid max-w-7xl grid-cols-2 gap-6 px-4 py-8 sm:px-6 lg:grid-cols-4 lg:px-8">
      {stats.map((s) => (
        <div class="rounded-2xl border border-stone-800/80 bg-stone-950/70 p-5 text-center">
          <p class="text-2xl font-extrabold text-amber-400 sm:text-3xl">{s.value}</p>
          <p class="mt-1 text-xs font-medium text-stone-400">{s.label}</p>
        </div>
      ))}
    </div>
  </section>

  <!-- Three Core Pillars -->
  <section class="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
    <div class="mb-10 text-center">
      <p class="text-xs font-bold uppercase tracking-widest text-amber-400">Three Dimensions of Ministry</p>
      <h2 class="mt-2 text-3xl font-bold text-white">Faith • Art • Technology</h2>
    </div>

    <div class="grid gap-7 lg:grid-cols-3">
      {pillars.map((p) => (
        <div class="flex flex-col justify-between rounded-2xl border border-stone-800 bg-stone-900/60 p-6 transition hover:border-amber-500/50">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-amber-400">{p.subtitle}</p>
            <h3 class="mt-1 text-2xl font-bold text-white">{p.title}</h3>
            <p class="mt-3 text-sm leading-relaxed text-stone-400">{p.desc}</p>
            <ul class="mt-5 space-y-2 border-t border-stone-800 pt-4">
              {p.links.map((item) => (
                <li>
                  <a href={item.href} class="flex items-center justify-between text-sm text-stone-300 transition hover:text-amber-300">
                    <span>{item.label}</span>
                    <span class="text-amber-500/80">→</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <a
            href={p.cta.href}
            class="mt-6 block rounded-xl border border-amber-500/40 bg-amber-500/10 py-2.5 text-center text-sm font-semibold text-amber-300 transition hover:bg-amber-500 hover:text-stone-950"
          >
            {p.cta.label}
          </a>
        </div>
      ))}
    </div>
  </section>
</BaseLayout>
""",
    "src/pages/about-me.astro": r"""---
import BaseLayout from "../layouts/BaseLayout.astro";

const skills = [
  "Generative AI Systems Integration",
  "Film Direction & Cinematography",
  "EdTech Logistics (50k+ Scale)",
  "Audio Engineering & Stem Separation",
  "Liturgical & Carnatic Composition",
  "Digital Archiving & Databases",
  "Applied Philosophy & Algorethics",
];

const education = [
  { degree: "MA Cinema Arts & Audiovisual", school: "DBIMA, Paris", period: "2025 – 2027" },
  { degree: "MSc Counseling & Psychotherapy", school: "Periyar University", period: "2023 – 2024" },
  { degree: "Diploma in Sound Engineering", school: "Bridge Academy", period: "2022" },
  { degree: "BA & MA English & MA History", school: "Annamalai University", period: "2014 – 2025" },
  { degree: "Bachelor of Theology & Philosophy", school: "Ecclesial Studies", period: "2013 – 2020" },
];

const experience = [
  {
    role: "Global AI Educator & Workshop Facilitator",
    org: "Independent Initiative",
    period: "Apr 2025 – Present",
    bullets: [
      "Designed and facilitated a global AI literacy initiative, conducting 15+ specialized AI workshops across India, France, Italy, and Cameroon.",
      "Tailored Train-the-Trainer curriculums for PhD scholars, school educators, media students, and international religious leaders.",
    ],
  },
  {
    role: "Digital Communications & Web Admin",
    org: "Amala Annai Capuchin Province",
    period: "May 2020 – Present",
    bullets: [
      "Engineered AI-assisted audio pipelines (vocal isolation, stem separation) to mass-scale 600+ Tamil tracks for Vetrisaipadal, achieving 25,000+ views.",
      "Architected the Malayadipatty Digital Archive, digitizing 350 years of mission history into a structured online repository.",
    ],
  },
  {
    role: "Provincial Secretary (Digital Transformation)",
    org: "Order of Friars Minor Capuchin",
    period: "Apr 2023 – Dec 2024",
    bullets: [
      "Led end-to-end modernization of legacy administrative records, digitizing and logically indexing over 50,000 pages into a secure cloud system.",
      "Oversaw physical construction of a modern archive facility with high-density shelving.",
    ],
  },
  {
    role: "EdTech Operations & Logistics Lead",
    org: "Thalir Holistic Welfare Centre",
    period: "Oct 2020 – Dec 2021",
    bullets: [
      "Co-spearheaded crisis-era digital transformation, engineering backend infrastructure for 60+ online courses.",
      "Onboarded and managed databases for over 50,000 global participants with zero-downtime under heavy traffic.",
    ],
  },
];

const certifications = [
  "Google Prompting Essentials (Coursera)",
  "Google AI Essentials (Coursera)",
  "IICT AI Skills House Scholar",
  "Gen AI: Beyond the Chatbot",
];
---

<BaseLayout title="About Me & CV">
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <!-- Profile Header Card -->
    <div class="rounded-3xl border border-stone-800 bg-stone-900/70 p-6 sm:p-10">
      <div class="grid items-center gap-8 md:grid-cols-12">
        <div class="md:col-span-3">
          <img
            src="https://lh3.googleusercontent.com/d/18b7YL8GrrE3I6N0_jLuO57xWiHlrjN3j"
            alt="Fr. Joseph Arputha Raj V"
            class="mx-auto h-44 w-44 rounded-2xl border-2 border-amber-500/40 object-cover shadow-xl"
          />
        </div>
        <div class="md:col-span-9">
          <p class="text-xs font-bold uppercase tracking-widest text-amber-400">
            AI Integration Specialist • Filmmaker • Capuchin Priest
          </p>
          <h1 class="mt-1 text-3xl font-extrabold text-white sm:text-4xl">
            Joseph Arputha Raj V
          </h1>
          <p class="mt-4 text-sm leading-relaxed text-stone-300">
            A modern Capuchin missionary, filmmaker, and Master AI Trainer candidate dedicated to
            bridging traditional storytelling and Generative AI. With 14 years of theological formation,
            experience managing EdTech logistics for 50,000+ users, and leading digital migrations, I
            empower individuals and institutions to harness AI ethically for impactful communication.
          </p>
          <div class="mt-5 flex flex-wrap gap-3 text-xs text-stone-300">
            <span class="rounded-lg border border-stone-800 bg-stone-950 px-3 py-1.5">Paris, FR / Tamil Nadu, IN</span>
            <a href="mailto:josephar89@gmail.com" class="rounded-lg border border-stone-800 bg-stone-950 px-3 py-1.5 hover:border-amber-500/60">josephar89@gmail.com</a>
            <a href="tel:+918637668430" class="rounded-lg border border-stone-800 bg-stone-950 px-3 py-1.5 hover:border-amber-500/60">+91 86376 68430</a>
            <a href="https://www.linkedin.com/in/josephar89" target="_blank" rel="noopener" class="rounded-lg border border-amber-500/40 bg-amber-500/10 px-3 py-1.5 font-semibold text-amber-300 hover:bg-amber-500 hover:text-stone-950">LinkedIn ↗</a>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-10 grid gap-8 lg:grid-cols-12">
      <!-- Left Column: Skills, Education, Certs -->
      <div class="space-y-8 lg:col-span-4">
        <section class="rounded-2xl border border-stone-800 bg-stone-900/50 p-6">
          <h2 class="text-sm font-bold uppercase tracking-wider text-amber-400">Core Skills</h2>
          <div class="mt-4 flex flex-wrap gap-2">
            {skills.map((s) => (
              <span class="rounded-lg border border-stone-700/80 bg-stone-950 px-3 py-1.5 text-xs font-medium text-stone-200">
                {s}
              </span>
            ))}
          </div>
        </section>

        <section class="rounded-2xl border border-stone-800 bg-stone-900/50 p-6">
          <h2 class="text-sm font-bold uppercase tracking-wider text-amber-400">Education Stack</h2>
          <div class="mt-4 space-y-4">
            {education.map((edu) => (
              <div class="border-l-2 border-amber-500/40 pl-3.5">
                <p class="text-sm font-semibold text-white">{edu.degree}</p>
                <p class="text-xs text-stone-400">{edu.school}</p>
                <p class="text-[11px] font-medium text-amber-400/80">{edu.period}</p>
              </div>
            ))}
          </div>
        </section>

        <section class="rounded-2xl border border-stone-800 bg-stone-900/50 p-6">
          <h2 class="text-sm font-bold uppercase tracking-wider text-amber-400">IICT &amp; Google Certifications</h2>
          <ul class="mt-4 space-y-2.5 text-xs text-stone-300">
            {certifications.map((c) => (
              <li class="flex items-start gap-2">
                <span class="text-amber-400">✓</span>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <!-- Right Column: High-Impact Experience -->
      <div class="space-y-6 lg:col-span-8">
        <h2 class="text-xl font-bold text-white">High-Impact Experience</h2>
        {experience.map((job) => (
          <article class="rounded-2xl border border-stone-800 bg-stone-900/50 p-6">
            <div class="flex flex-wrap items-baseline justify-between gap-2">
              <div>
                <h3 class="text-lg font-bold text-white">{job.role}</h3>
                <p class="text-sm font-medium text-amber-400">{job.org}</p>
              </div>
              <span class="rounded-full border border-stone-700 bg-stone-950 px-3 py-1 text-xs text-stone-300">
                {job.period}
              </span>
            </div>
            <ul class="mt-4 list-disc space-y-2 pl-5 text-sm leading-relaxed text-stone-300">
              {job.bullets.map((b) => (
                <li>{b}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </div>
  </div>
</BaseLayout>
""",
    # =========================================================================
    # 5. FAITH HUB, CHRONICLES, MAGNIFICA HUMANITAS, SWC (12 LANGS), WRITINGS
    # =========================================================================
    "src/pages/faith/index.astro": r"""---
import BaseLayout from "../../layouts/BaseLayout.astro";

const cards = [
  {
    tag: "Papal Encyclical • Tamil Translation",
    title: "மாண்புமிகு மனிதகுலம் (Magnifica Humanitas)",
    desc: "Complete 42,000-word Tamil translation of Pope Leo XIV's landmark encyclical on AI, technology, and human dignity—with distraction-free E-Reader controls and AI-translation methodology.",
    href: "/faith/magnifica-humanitas",
  },
  {
    tag: "800th Anniversary of Transitus • 12 Languages",
    title: "Seraphic Way of the Cross",
    desc: "Walk the 14 Stations of Christ's Passion paired with the life of St. Francis of Assisi—available in English, Tamil, Italian, French, Spanish, Mexican, Hindi, Kannada, Konkani, Malayalam, Telugu, and Odia.",
    href: "/faith/writings/seraphic-way-of-the-cross",
  },
  {
    tag: "Pastoral Writings & Meditations",
    title: "Writings & Open Letters",
    desc: "Read 'AI Priest: An Open Letter', 'ஆதவன் கீதமும் ஆண்டவர் சிலுவையும்', and 'குடிலும் குருசும்', plus my Vatican II interfaith dissertation.",
    href: "/faith/writings",
  },
  {
    tag: "Academic Study Vault • 100+ PDFs",
    title: "Philosophy & Theology Archives",
    desc: "Searchable repository of handwritten and compiled notes from St. Joseph's Philosophical Institute (2013–2016) and Francesco Theological Institute (2017–2020).",
    href: "/faith/archives",
  },
  {
    tag: "Milestones & Video Memories",
    title: "Life Chronicles",
    desc: "Video archives from Simple Profession (2013), Diaconate & Malayadipatty E-Book Release (2020), Priestly Ordination, and First Holy Mass (2021).",
    href: "/faith/chronicles",
  },
];
---

<BaseLayout title="Faith & Vocation">
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <div class="mb-10 border-b border-stone-800 pb-6">
      <p class="text-xs font-bold uppercase tracking-widest text-amber-400">Faith &amp; Vocation</p>
      <h1 class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">Spiritual Writings &amp; Theological Archives</h1>
      <p class="mt-2 max-w-2xl text-sm text-stone-400">
        Franciscan reflections, magisterial Tamil translations, multilingual devotionals, and academic notes from 14 years of formation.
      </p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      {cards.map((c) => (
        <a
          href={c.href}
          class="group flex flex-col justify-between rounded-2xl border border-stone-800 bg-stone-900/60 p-6 transition hover:-translate-y-0.5 hover:border-amber-500/60"
        >
          <div>
            <span class="text-xs font-semibold text-amber-400">{c.tag}</span>
            <h2 class="mt-2 text-xl font-bold text-white group-hover:text-amber-300">{c.title}</h2>
            <p class="mt-3 text-sm leading-relaxed text-stone-400">{c.desc}</p>
          </div>
          <span class="mt-5 inline-block text-xs font-bold text-amber-400">Open Resource →</span>
        </a>
      ))}
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/faith/chronicles.astro": r"""---
import BaseLayout from "../../layouts/BaseLayout.astro";
import chroniclesData from "../../data/chronicles.json";
---

<BaseLayout title="Life Chronicles">
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <div class="mb-10 border-b border-stone-800 pb-6">
      <a href="/faith" class="text-xs font-semibold text-amber-400 hover:underline">← Back to Faith Hub</a>
      <h1 class="mt-2 text-3xl font-extrabold text-white">Life Events &amp; Chronicles</h1>
      <p class="mt-2 text-sm text-stone-400">Key milestones along my Capuchin religious journey.</p>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      {chroniclesData.events.map((ev) => (
        <article class="overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/60">
          <div class="aspect-video w-full bg-black">
            <iframe
              class="h-full w-full"
              src={`https://www.youtube.com/embed/${ev.youtubeId}`}
              title={ev.title}
              loading="lazy"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          <div class="p-5">
            <span class="text-xs font-semibold text-amber-400">{ev.year} • {ev.date}</span>
            <h2 class="mt-1 text-lg font-bold text-white">{ev.title}</h2>
            <p class="text-xs text-stone-400">{ev.place}</p>
          </div>
        </article>
      ))}
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/faith/magnifica-humanitas/index.astro": r"""---
import { getCollection } from "astro:content";
import BaseLayout from "../../../layouts/BaseLayout.astro";

const chapters = (await getCollection("magnifica-humanitas")).sort(
  (a, b) => a.data.order - b.data.order
);
---

<BaseLayout
  title="மாண்புமிகு மனிதகுலம் (Magnifica Humanitas)"
  description="Complete Tamil translation of Pope Leo XIV's encyclical Magnifica Humanitas on Artificial Intelligence and human dignity."
>
  <div class="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
    <a href="/faith" class="text-xs font-semibold text-amber-400 hover:underline">← Back to Faith Hub</a>

    <div class="mt-4 rounded-3xl border border-amber-500/30 bg-gradient-to-br from-amber-950/30 via-stone-900 to-stone-950 p-8 sm:p-10">
      <span class="inline-block rounded-full border border-amber-500/40 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-300">
        Pope Leo XIV • Encyclical Tamil Translation (2026)
      </span>
      <h1 class="mt-3 text-3xl font-extrabold text-white sm:text-4xl">
        மாண்புமிகு மனிதகுலம்
        <span class="block text-xl font-medium text-amber-400 sm:text-2xl">Magnifica Humanitas</span>
      </h1>
      <p class="mt-4 text-sm leading-relaxed text-stone-300">
        மாண்புமிகு திருத்தந்தை 14-ஆம் லியோ அவர்களால் வெளியிடப்பட்ட இந்தச் சுற்றுமடல், செயற்கை நுண்ணறிவு (AI),
        நவீன தொழில்நுட்பம் மற்றும் மனித மாண்பு ஆகியவற்றிற்கு இடையிலான ஆழமான தொடர்பை விளக்குகிறது.
      </p>
      <p class="mt-3 text-sm leading-relaxed text-stone-400">
        Promulgated by His Holiness Pope Leo XIV, this landmark 42,000-word encyclical offers vital pastoral and
        theological guidance on AI, technology, justice, and human dignity. Translated via a specialized human-reviewed
        AI theological pipeline by Fr. Joseph Arputha Raj OFM Cap.
      </p>
      <div class="mt-6 flex flex-wrap gap-3">
        <a
          href="/faith/magnifica-humanitas/introduction"
          class="rounded-xl bg-amber-500 px-5 py-2.5 text-sm font-bold text-stone-950 hover:bg-amber-400"
        >
          Start Reading (முன்னுரை) →
        </a>
        <a
          href="https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html"
          target="_blank"
          rel="noopener"
          class="rounded-xl border border-stone-700 bg-stone-900 px-5 py-2.5 text-sm font-semibold text-stone-200 hover:border-amber-500/60"
        >
          Official Vatican Source ↗
        </a>
      </div>
    </div>

    <!-- Chapters List -->
    <div class="mt-10 space-y-3">
      <h2 class="text-lg font-bold text-white">மடல் உள்ளடக்கம் (Table of Contents)</h2>
      {chapters.map((ch) => (
        <a
          href={`/faith/magnifica-humanitas/${ch.slug}`}
          class="flex items-center justify-between rounded-xl border border-stone-800 bg-stone-900/60 px-5 py-4 transition hover:border-amber-500/50 hover:bg-stone-900"
        >
          <span class="text-sm font-semibold text-stone-100 sm:text-base">{ch.data.title}</span>
          <span class="text-xs font-bold text-amber-400">Read →</span>
        </a>
      ))}
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/faith/magnifica-humanitas/[...slug].astro": r"""---
import { getCollection } from "astro:content";
import ReaderLayout from "../../../layouts/ReaderLayout.astro";

export async function getStaticPaths() {
  const chapters = (await getCollection("magnifica-humanitas")).sort(
    (a, b) => a.data.order - b.data.order
  );
  return chapters.map((entry, idx) => ({
    params: { slug: entry.slug },
    props: {
      entry,
      chapters,
      prevEntry: idx > 0 ? chapters[idx - 1] : null,
      nextEntry: idx < chapters.length - 1 ? chapters[idx + 1] : null,
    },
  }));
}

const { entry, chapters, prevEntry, nextEntry } = Astro.props;
const { Content } = await entry.render();

const sidebarItems = chapters.map((c) => ({
  href: `/faith/magnifica-humanitas/${c.slug}`,
  label: c.data.title,
  active: c.slug === entry.slug,
}));
---

<ReaderLayout
  title={entry.data.title}
  subtitle="மாண்புமிகு மனிதகுலம் — Magnifica Humanitas (Pope Leo XIV)"
  badge="Magnifica Humanitas • Tamil Edition"
  backHref="/faith/magnifica-humanitas"
  backLabel="Encyclical Index"
  sidebarTitle="மடல் உள்ளடக்கம்"
  sidebarItems={sidebarItems}
  prev={prevEntry ? { href: `/faith/magnifica-humanitas/${prevEntry.slug}`, label: prevEntry.data.title } : null}
  next={nextEntry ? { href: `/faith/magnifica-humanitas/${nextEntry.slug}`, label: nextEntry.data.title } : null}
>
  <Content />
</ReaderLayout>
""",
    "src/pages/faith/writings/seraphic-way-of-the-cross/index.astro": r"""---
import { getCollection } from "astro:content";
import BaseLayout from "../../../../layouts/BaseLayout.astro";

const editions = (await getCollection("seraphic-way")).sort((a, b) =>
  a.data.englishName.localeCompare(b.data.englishName)
);
---

<BaseLayout
  title="Seraphic Way of the Cross (12 Languages)"
  description="800th Anniversary of the Transitus of St. Francis of Assisi — Seraphic Way of the Cross in 12 languages."
>
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <a href="/faith" class="text-xs font-semibold text-amber-400 hover:underline">← Back to Faith Hub</a>
    <div class="mt-4 mb-10 border-b border-stone-800 pb-6">
      <span class="inline-block rounded-full border border-amber-500/40 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-300">
        800th Anniversary of the Transitus (1226–2026)
      </span>
      <h1 class="mt-3 text-3xl font-extrabold text-white sm:text-4xl">
        Seraphic Way of the Cross
      </h1>
      <p class="mt-3 max-w-3xl text-sm leading-relaxed text-stone-400">
        Correlating the 14 Stations of Christ&apos;s Passion with pivotal moments in the life of St. Francis of Assisi.
        Select your language below to pray with our built-in distraction-free reader.
      </p>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {editions.map((ed) => (
        <a
          href={`/faith/writings/seraphic-way-of-the-cross/${ed.data.langCode}`}
          class="group flex flex-col justify-between rounded-2xl border border-stone-800 bg-stone-900/60 p-6 transition hover:-translate-y-0.5 hover:border-amber-500/60"
        >
          <div>
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs uppercase text-amber-400">{ed.data.langCode}</span>
              {ed.data.aiTranslated && (
                <span class="rounded bg-stone-800 px-2 py-0.5 text-[10px] text-stone-400">AI-Assisted</span>
              )}
            </div>
            <h2 class="mt-2 text-xl font-bold text-white group-hover:text-amber-300">
              {ed.data.nativeName}
            </h2>
            <p class="text-xs text-stone-400">{ed.data.englishName}</p>
          </div>
          <span class="mt-5 text-xs font-semibold text-amber-400">Pray Stations →</span>
        </a>
      ))}
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/faith/writings/seraphic-way-of-the-cross/[lang].astro": r"""---
import { getCollection } from "astro:content";
import ReaderLayout from "../../../../layouts/ReaderLayout.astro";

export async function getStaticPaths() {
  const editions = await getCollection("seraphic-way");
  return editions.map((entry) => ({
    params: { lang: entry.data.langCode },
    props: { entry, editions },
  }));
}

const { entry, editions } = Astro.props;
const { Content } = await entry.render();

const sidebarItems = editions
  .sort((a, b) => a.data.englishName.localeCompare(b.data.englishName))
  .map((e) => ({
    href: `/faith/writings/seraphic-way-of-the-cross/${e.data.langCode}`,
    label: `${e.data.nativeName} (${e.data.englishName})`,
    active: e.data.langCode === entry.data.langCode,
  }));
---

<ReaderLayout
  title={entry.data.title}
  subtitle="800th Anniversary of the Transitus of St. Francis of Assisi (1226–2026)"
  badge={`${entry.data.nativeName} Edition`}
  backHref="/faith/writings/seraphic-way-of-the-cross"
  backLabel="All 12 Languages"
  sidebarTitle="Switch Language"
  sidebarItems={sidebarItems}
>
  <Content />
</ReaderLayout>
""",
    "src/pages/faith/writings/index.astro": r"""---
import { getCollection } from "astro:content";
import BaseLayout from "../../../layouts/BaseLayout.astro";

const docs = (await getCollection("writings")).filter((d) => d.slug !== "sub-trans");
---

<BaseLayout title="Pastoral Writings & Meditations">
  <div class="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
    <a href="/faith" class="text-xs font-semibold text-amber-400 hover:underline">← Back to Faith Hub</a>
    <h1 class="mt-3 text-3xl font-extrabold text-white">Writings &amp; Reflections</h1>
    <p class="mt-2 text-sm text-stone-400">
      Franciscan meditations, open letters on AI ministry, and theological reflections.
    </p>

    <div class="mt-8 grid gap-5 md:grid-cols-2">
      <a href="/faith/magnifica-humanitas" class="rounded-2xl border border-amber-500/30 bg-stone-900/70 p-6 hover:border-amber-400">
        <span class="text-xs font-semibold text-amber-400">Encyclical Translation</span>
        <h2 class="mt-1 text-lg font-bold text-white">மாண்புமிகு மனிதகுலம் (Magnifica Humanitas)</h2>
        <p class="mt-2 text-xs text-stone-400">Full Tamil E-Reader edition of Pope Leo XIV&apos;s encyclical.</p>
      </a>

      <a href="/faith/writings/seraphic-way-of-the-cross" class="rounded-2xl border border-amber-500/30 bg-stone-900/70 p-6 hover:border-amber-400">
        <span class="text-xs font-semibold text-amber-400">12 Languages</span>
        <h2 class="mt-1 text-lg font-bold text-white">Seraphic Way of the Cross</h2>
        <p class="mt-2 text-xs text-stone-400">800th Transitus anniversary stations in 12 languages.</p>
      </a>

      {docs.map((doc) => (
        <a href={`/faith/writings/${doc.slug}`} class="rounded-2xl border border-stone-800 bg-stone-900/60 p-6 hover:border-amber-500/60">
          <span class="text-xs font-semibold text-amber-400">{doc.data.language}</span>
          <h2 class="mt-1 text-lg font-bold text-white">{doc.data.title}</h2>
          <span class="mt-4 inline-block text-xs font-semibold text-amber-400">Read →</span>
        </a>
      ))}

      <a
        href="https://drive.google.com/file/d/1cglxNtQBdnsufaNHBmgG1ixpTe65L_Lb/view"
        target="_blank"
        rel="noopener"
        class="rounded-2xl border border-stone-800 bg-stone-900/60 p-6 hover:border-amber-500/60"
      >
        <span class="text-xs font-semibold text-amber-400">Theological Dissertation (PDF)</span>
        <h2 class="mt-1 text-lg font-bold text-white">Internet Inter-Faith Integrity</h2>
        <p class="mt-2 text-xs text-stone-400">Social media as a modern platform for interreligious dialogue grounded in Vatican II.</p>
      </a>
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/faith/writings/[slug].astro": r"""---
import { getCollection } from "astro:content";
import ReaderLayout from "../../../layouts/ReaderLayout.astro";

export async function getStaticPaths() {
  const docs = (await getCollection("writings")).filter((d) => d.slug !== "sub-trans");
  return docs.map((entry) => ({
    params: { slug: entry.slug },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();
---

<ReaderLayout
  title={entry.data.title}
  badge={entry.data.language}
  backHref="/faith/writings"
  backLabel="All Writings"
>
  <Content />
</ReaderLayout>
""",
}


def main():
    for rel_path, content in FILES.items():
        path = ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"[CREATED] {rel_path}")
    print("\n[DONE] Core Astro + GitHub Pages scaffold created! Run `npm install` next.")


if __name__ == "__main__":
    main()