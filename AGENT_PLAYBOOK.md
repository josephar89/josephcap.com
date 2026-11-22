# AGENT_PLAYBOOK.md — Remote Management Guide for josephcap.com

This repository powers **https://www.josephcap.com** via **Astro + React Islands + Tailwind CSS**, deployed statically to **GitHub Pages** on every push to `main`.

## 1. Golden Rules for AI Agents (Google Antigravity)
- **Static Only:** Never add SSR adapters, server API routes, or database servers. Everything must compile cleanly with `npm run build` into `dist/`.
- **Always Verify Build Before Pushing:** Run `npm run build` after any JSON/Markdown/component change to confirm zero Astro/TypeScript/schema errors.
- **Preserve `public/CNAME`:** Keep `www.josephcap.com` untouched so custom domain HTTPS never breaks.
- **Liturgical Fidelity:** Preserve the Catholic liturgical disclaimer on Vetrisaipadal (karaoke is for practice/cultural events, not Mass liturgy) and standard Tamil Roman Catholic theological terms (`நற்செய்தி`, `அருளடையாளம்`, `மனித மாண்பு`, `பொதுநலம்`).

## 2. Common Remote Update Recipes

### A. Add a New Vetrisaipadal Karaoke Track
Edit `src/data/vetrisaipadal.json` -> append to `"tracks"`:
```json
{
  "code": "555",
  "title": "தமிழ் பாடல் தலைப்பு",
  "category": "marian",
  "youtubeId": "11_CHAR_YOUTUBE_ID"
}
```

### B. Add or Update an Original Music Album
Edit `src/data/albums.json` -> add album or song object with title, lyrics, YouTube/streaming links.

### C. Add a Film / Cinema Project
Edit `src/data/films.json` -> add film object with title, role, synopsis, and poster/stills.

### D. Add an AI Project / Experiment
Edit `src/data/ai-projects.json` -> add project object with category, description, and link.

### E. Add an AI Literacy Workshop
Edit `src/data/workshops.json` -> add workshop object with organization, location, audience, and topics.

### F. Add a Philosophy or Theology Archive Document
Edit `src/data/archives.json` -> add document object with title, subject, driveId / URL, and year.

### G. Publish a New Theological Article / Writing
Create a new Markdown file in `src/content/writings/<slug>.md` with frontmatter (`title`, `description`, `date`, `language`, `tags`).

## 3. Architecture & Directory Overview
- `src/pages/`: Astro file-based static routing.
- `src/components/react/`: Interactive React client islands (e.g. `client:load` for search/audio/video filters).
- `src/layouts/`: `BaseLayout.astro` and `ReaderLayout.astro`.
- `src/data/`: Structured JSON data files.
- `src/content/`: Content collections defined in `src/content/config.ts`.
- `public/`: Static assets (`CNAME`, images, icons).

## 4. Verification & Deployment
- Run `npm run build` to generate static files in `dist/`.
- Automatic CI/CD workflow in `.github/workflows/deploy.yml` deploys `dist/` to GitHub Pages upon push to `main`.
