#!/usr/bin/env python3
"""
JosephCap.com Automated Content Migration Script (Drop 1 of 3)
Parses JOSEPHCAP_COMPLETE_WEBSITE_BUNDLE.md into clean Astro Markdown & JSON datasets
optimized for GitHub Pages hosting.

Usage:
    python migrate_bundle.py
    python migrate_bundle.py --bundle JOSEPHCAP_COMPLETE_WEBSITE_BUNDLE.md --download-images
"""

import argparse
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(".")
DATA_DIR = ROOT / "src" / "data"
CONTENT_DIR = ROOT / "src" / "content"
IMAGES_DIR = ROOT / "public" / "images"

AUDIT_NOTES = []


# ============================================================================
# UTILITIES
# ============================================================================

def ensure_dirs():
    for d in [
        DATA_DIR,
        CONTENT_DIR / "magnifica-humanitas",
        CONTENT_DIR / "seraphic-way",
        CONTENT_DIR / "writings",
        IMAGES_DIR / "workshops",
        IMAGES_DIR / "albums",
        IMAGES_DIR / "stations",
        IMAGES_DIR / "misc",
    ]:
        d.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md(path: Path, frontmatter: dict, body: str):
    lines = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        elif v is None:
            continue
        else:
            escaped = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{escaped}"')
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def unwrap_google_redirect(url: str) -> str:
    if not url:
        return ""
    url = url.strip().strip("<>")
    if "google.com/url?" in url:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if "q" in qs and qs["q"]:
            return urllib.parse.unquote(qs["q"][0])
    return url


def extract_youtube_id(url: str):
    if not url:
        return None
    m = re.search(
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        url,
    )
    return m.group(1) if m else None


def fix_split_markdown_links(text: str) -> str:
    """Fixes Google Sites export glitches like [Phenomenolog](<url>)y -> [Phenomenology](<url>)."""
    text = re.sub(r"\[([^\]]+)\]\(<([^>]+)>\)([A-Za-z]+)", r"[\1\3](\2)", text)
    text = re.sub(r"\]\(<([^>]+)>\)", r"](\1)", text)
    return text


def clean_markdown_headings(text: str) -> str:
    """Fixes `#Heading` without space -> `## Heading`."""
    lines = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})([^\s#].*)$", line)
        if m:
            lines.append(f"{m.group(1)} {m.group(2).strip()}")
        else:
            lines.append(line)
    return "\n".join(lines)


def download_image(url: str, subfolder: str, prefix: str, enabled: bool) -> str:
    """Optionally downloads remote image into public/images/<subfolder>/ and returns local path."""
    if not url or not enabled:
        return url
    try:
        h = hashlib.md5(url.encode("utf-8")).hexdigest()[:10]
        filename = f"{prefix}_{h}.jpg"
        dest = IMAGES_DIR / subfolder / filename
        if not dest.exists():
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (JosephCap-Migrator/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                dest.write_bytes(resp.read())
        return f"/images/{subfolder}/{filename}"
    except Exception as exc:
        AUDIT_NOTES.append(f"Image download failed ({prefix}): {url} -> {exc}")
        return url


# ============================================================================
# STEP 1: SPLIT MASTER BUNDLE INTO PAGES
# ============================================================================

def parse_bundle(bundle_path: Path) -> dict:
    raw = bundle_path.read_text(encoding="utf-8")
    chunks = re.split(r'(?=<a id="page-[^"]+"></a>)', raw)
    pages = {}

    for chunk in chunks:
        if not chunk.strip().startswith('<a id="page-'):
            continue
        meta_m = re.search(
            r"#\s+\d+\.\s+(.+?)\n\*\*URL:\*\*\s+`([^`]+)`\s+\|\s+\*\*Path:\*\*\s+`([^`]+)`\s+\|\s+\*\*Category:\*\*\s+`([^`]+)`",
            chunk,
        )
        if not meta_m:
            continue
        title, url, path, category = [g.strip() for g in meta_m.groups()]
        content_split = chunk.split("### Content:", 1)
        content = content_split[1].strip() if len(content_split) > 1 else ""
        # Strip trailing horizontal divider between pages
        content = re.sub(r"\n---\s*$", "", content).strip()

        pages[path] = {
            "title": title,
            "url": url,
            "path": path,
            "category": category,
            "content": content,
        }

    return pages


# ============================================================================
# STEP 2: VETRISAIPADAL (ALL 500+ KARAOKE TRACKS)
# ============================================================================

VETRI_CATEGORY_MAP = {
    "வருகைப் பாடல்கள்": ("entrance", "Entrance"),
    "தியானப் பாடல்கள்": ("meditation", "Meditation"),
    "காணிக்கைப் பாடல்கள்": ("offertory", "Offertory"),
    "திருவிருந்துப் பாடல்கள்": ("communion", "Communion"),
    "மரியன்னை பாடல்கள்": ("marian", "Marian"),
    "பிற பாடல்கள்": ("others", "Praise & Others"),
    "இறைபுகழ் கீதம்": ("praise", "Praise & Worship"),
    "நன்றிப்பாடல்கள்": ("thanksgiving", "Thanksgiving"),
    "திரு இருதயம்": ("sacred_heart", "Sacred Heart"),
    "புனிதர்கள்": ("saints", "Saints"),
    "நடனம்": ("dance", "Dance & Cultural"),
    "திரைஇசைப் பாடல்கள்": ("film_devotional", "Devotional Cinema"),
    "பிறபாடல்கள்": ("others", "Praise & Others"),
    "அருங்கொடைப் பாடல்கள்": ("charismatic", "Charismatic"),
    "கிறிஸ்து பிறப்பு பாடல்கள்": ("christmas", "Christmas"),
    "தவக்காலப் பாடல்கள்": ("lent", "Lent & Passion"),
    "கிறிஸ்தவ பாடல்கள்": ("christian", "Christian Hymns"),
    "ஜெபத்தோட்ட ஜெயகீதங்கள்": ("jebathotta", "Jebathotta Jeyageethangal"),
    "பாரம்பரிய பாடல்கள்": ("traditional", "Traditional Hymns"),
}

VETRI_PLAYLISTS = {
    "all": "https://www.youtube.com/@Vetrisaipadal",
    "entrance": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPrtdldNQXvFcGUYZm1uS5xT",
    "meditation": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPpS9puKYH1ymnJ9m9nbHoLE",
    "offertory": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPq565YSCEkBWAAeKOJrBe3i",
    "communion": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPqNVXA6_Tg5qC6tcJC6H9h7",
    "marian": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPo17lhfCHAfZz5hmWzIA_LJ",
    "lent": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPobaAKZinNItHeAkKcJV5tJ",
    "christmas": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPqWp-JDRtnjzxb0uiSCuy-u",
    "others": "https://www.youtube.com/playlist?list=PL4TrpyyQSPPrNq-SSdBnxAL8O09kLW1z6",
}


def migrate_vetrisaipadal(pages: dict):
    page = pages.get("/art/music/vetrisaipadal")
    if not page:
        return

    text = page["content"]
    marker = "All the titles are clickable links"
    body = text.split(marker, 1)[1] if marker in text else text

    current_cat_id = "entrance"
    tracks = []
    seen_keys = set()
    used_categories = {}

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line == "---":
            continue

        # Check if line is a category header
        plain = re.sub(r"^#+\s*", "", line)
        link_header = re.match(r"^\[([^\]]+)\]\(<?[^>]+>?\)$", plain)
        header_candidate = link_header.group(1).strip() if link_header else plain.strip()

        if header_candidate in VETRI_CATEGORY_MAP:
            cat_id, eng = VETRI_CATEGORY_MAP[header_candidate]
            current_cat_id = cat_id
            used_categories[cat_id] = {
                "id": cat_id,
                "tamil": header_candidate,
                "english": eng,
                "playlistUrl": VETRI_PLAYLISTS.get(cat_id, VETRI_PLAYLISTS["all"]),
            }
            continue

        # Check if line is a track entry
        m = re.match(r"^\[([^\]]+)\]\(<?(https?://[^>)\s]+)>?\)$", line)
        if m:
            label, url = m.group(1).strip(), m.group(2).strip()
            yt_id = extract_youtube_id(url)
            if not yt_id:
                continue

            # Parse leading code like "006\. Title" or "043 Title"
            label_clean = label.replace(r"\.", ".")
            code_m = re.match(r"^(\d{2,4})[\.\s]+(.+)$", label_clean)
            if code_m:
                code = code_m.group(1).zfill(3)
                title = code_m.group(2).strip()
            else:
                code = "000"
                title = label_clean

            dedup_key = (code, yt_id)
            if dedup_key in seen_keys:
                AUDIT_NOTES.append(f"Vetrisaipadal: Removed duplicate track #{code} ({title})")
                continue
            seen_keys.add(dedup_key)

            tracks.append(
                {
                    "code": code,
                    "title": title,
                    "category": current_cat_id,
                    "youtubeId": yt_id,
                }
            )

    categories_list = [
        {
            "id": "all",
            "tamil": "அனைத்தும்",
            "english": "All Tracks",
            "playlistUrl": VETRI_PLAYLISTS["all"],
        }
    ] + list(used_categories.values())

    write_json(
        DATA_DIR / "vetrisaipadal.json",
        {
            "channelUrl": "https://www.youtube.com/@Vetrisaipadal",
            "totalTracks": len(tracks),
            "disclaimerTamil": "கத்தோலிக்கத் திருஅவையின் படிப்பினையின் படி, திருப்பலியில் இவ்வகை வெற்றிசைப்பாடல்கள் பயன்படுத்தக்கூடாது. ஆனால், இறைஇசை ஆர்வலர்களுக்கும், பாடகர் குழுவினருக்கும், பொது நிகழ்வுகளிலும் கலை நிகழ்ச்சிகளிலும் சினிமாப் பாடல்களைத் தவிர்த்து இறை இசைப் பாடல்களை ஊக்குவிக்க இது ஓர் அரிய ஊடகமாகும்.",
            "disclaimerEnglish": "Processed via AI vocal isolation and stem separation. While these karaoke tracks are not permitted during the Liturgy of the Holy Mass per Catholic Church teachings, they empower choirs, learners, and communities to choose sacred devotional music over cinema songs at public and cultural events.",
            "categories": categories_list,
            "tracks": tracks,
        },
    )
    print(f"[OK] vetrisaipadal.json -> {len(tracks)} tracks across {len(used_categories)} categories")


# ============================================================================
# STEP 3: GLOBAL AI WORKSHOPS
# ============================================================================

def migrate_workshops(pages: dict, download_imgs: bool):
    page = pages.get("/science/ai-workshops")
    if not page:
        return

    blocks = [b.strip() for b in page["content"].split("\n---\n") if b.strip()]
    workshops = []

    for idx, block in enumerate(blocks):
        if "📍 Place:" not in block:
            continue

        lines = [l.strip() for l in block.splitlines() if l.strip()]
        title = lines[0]

        def get_field(prefix):
            for l in lines:
                if l.startswith(prefix):
                    return l.replace(prefix, "", 1).strip()
            return ""

        place = get_field("📍 Place:")
        date_str = get_field("📅 Date:")
        target = get_field("👥 Target Group:")
        participants_raw = get_field("🔢 Participants:")
        focus = get_field("🎯 Focus:")
        takeaway = get_field("💡 Key Takeaway:")

        num_m = re.search(r"(\d+)", participants_raw)
        participants_count = int(num_m.group(1)) if num_m else 0

        # Extract country from place
        country = "India"
        for c in ["France", "Italy", "Cameroon", "India"]:
            if c.lower() in place.lower():
                country = c
                break

        fb_m = re.search(r"\[!\[Facebook\][^\]]+\]\(<?([^>)]+)>?\)", block)
        li_m = re.search(r"\[!\[LinkedIn\][^\]]+\]\(<?([^>)]+)>?\)", block)
        img_m = re.search(r"!\[\]\((https?://[^)]+)\)", block)

        image_url = (
            download_image(img_m.group(1), "workshops", f"ws_{idx:02d}", download_imgs)
            if img_m
            else ""
        )

        workshops.append(
            {
                "id": f"workshop-{idx:02d}",
                "title": title,
                "place": place,
                "country": country,
                "date": date_str,
                "targetGroup": target,
                "participantsLabel": participants_raw,
                "participantsCount": participants_count,
                "focus": focus,
                "takeaway": takeaway,
                "facebookUrl": unwrap_google_redirect(fb_m.group(1)) if fb_m else None,
                "linkedinUrl": unwrap_google_redirect(li_m.group(1)) if li_m else None,
                "image": image_url,
            }
        )

    write_json(
        DATA_DIR / "workshops.json",
        {
            "totalWorkshops": len(workshops),
            "totalParticipants": sum(w["participantsCount"] for w in workshops),
            "countries": sorted(list({w["country"] for w in workshops})),
            "workshops": workshops,
        },
    )
    print(f"[OK] workshops.json -> {len(workshops)} workshops")


# ============================================================================
# STEP 4: AI PROJECTS (AUTO-FIXES PRIVATE /edit LINKS & DUPLICATES)
# ============================================================================

INTERNAL_LINK_FIXES = {
    "1sTmA-oP3wgR7ql3heAlV82pwfsVw85LE": "/faith/writings/aadhavan-geetham",
    "1Jk_CMTpvz7Y5_fpCXXRDrngxFvda57Wr": "/faith/writings/kudilum-kurusum",
    "1UOia9xueNHwGzWmRc5rOQAoSmC-uJIS1": "/faith/writings/seraphic-way-of-the-cross",
}


def migrate_ai_projects(pages: dict):
    page = pages.get("/science/ai-projects")
    if not page:
        return

    sections = [s.strip() for s in page["content"].split("\n---\n") if s.strip()]
    projects = []
    seen_titles = set()

    for sec in sections:
        if sec == "# AI-Projects":
            continue
        lines = [l.strip() for l in sec.splitlines() if l.strip()]
        if not lines:
            continue

        category = re.sub(r"^#+\s*", "", lines[0]).strip()
        rest = "\n".join(lines[1:])

        # Split items inside category by `#Title` or known unprefixed headers
        item_blocks = re.split(
            r"(?=(?:^#[^\s#]|^Enterprise Data Synthesis:|^Profile Auto-Architecture:))",
            rest,
            flags=re.MULTILINE,
        )

        for item in item_blocks:
            item = item.strip()
            if not item:
                continue
            item_lines = [l.strip() for l in item.splitlines() if l.strip()]
            title = re.sub(r"^#+\s*", "", item_lines[0]).strip()

            if title in seen_titles:
                AUDIT_NOTES.append(f"AI-Projects: Removed duplicate project '{title}'")
                continue
            seen_titles.add(title)

            body_text = "\n".join(item_lines[1:])

            # Extract CTA link
            cta_url = None
            cta_label = "Explore Project"
            link_m = re.search(r"\[([^\]]+)\]\(<?([^>)]+)>?\)", body_text)
            if link_m:
                cta_label = link_m.group(1).strip().strip("[]")
                raw_url = link_m.group(2).strip()
                # Fix private Google Sites /edit links
                fixed = False
                for site_page_id, clean_route in INTERNAL_LINK_FIXES.items():
                    if site_page_id in raw_url:
                        cta_url = clean_route
                        fixed = True
                        AUDIT_NOTES.append(
                            f"AI-Projects: Fixed private Google Sites /edit link on '{title}' -> {clean_route}"
                        )
                        break
                if not fixed:
                    if "/science/ai-projects/sub_trans" in raw_url:
                        cta_url = "/science/ai-projects/sub-trans"
                    else:
                        cta_url = raw_url

            if "[Your Workflow Link Here]" in body_text:
                cta_url = None
                AUDIT_NOTES.append(
                    f"AI-Projects: Stripped unfinished '[Your Workflow Link Here]' placeholder on '{title}'"
                )

            # Remove link line from summary description
            summary = re.sub(r"🔗.*$", "", body_text, flags=re.MULTILINE).strip()
            summary = re.sub(
                r"(?:Read the full case study:|Read it here:|Acces the Playlist:).*",
                "",
                summary,
            ).strip()

            projects.append(
                {
                    "id": re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50],
                    "category": category,
                    "title": title,
                    "summary": summary,
                    "ctaLabel": cta_label,
                    "ctaUrl": cta_url,
                }
            )

    write_json(DATA_DIR / "ai-projects.json", {"projects": projects})
    print(f"[OK] ai-projects.json -> {len(projects)} unique AI case studies")

    # Also export Varayan Contextual Subtitle Translation case study as Markdown
    sub_page = pages.get("/science/ai-projects/sub_trans")
    if sub_page:
        body = clean_markdown_headings(fix_split_markdown_links(sub_page["content"]))
        write_md(
            CONTENT_DIR / "writings" / "sub-trans.md",
            {
                "title": "Contextual Subtitle Translation — Varayan (2022) AI Case Study",
                "slug": "sub-trans",
                "category": "AI Case Study",
                "language": "English",
            },
            body,
        )
        print("[OK] src/content/writings/sub-trans.md")


# ============================================================================
# STEP 5: PHILOSOPHY, THEOLOGY & MUSIC LEARNING ARCHIVES
# ============================================================================

def parse_drive_archive(text: str, section_name: str) -> list:
    text = fix_split_markdown_links(text)
    categories = []
    blocks = [b.strip() for b in text.split("\n---\n") if b.strip()]

    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        # Skip intro block
        if "PDFs of all my" in block or "Foundational Years" in block:
            continue

        cat_title = re.sub(r"^(?:#+|\d+\\?\.)\s*", "", lines[0]).strip()
        items = []
        for l in lines[1:]:
            l_clean = re.sub(r"^\d+\\?\.\s*", "", l).strip()
            m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", l_clean)
            if m:
                prefix = l_clean[: m.start()].strip()
                name = f"{prefix} {m.group(1)}".strip()
                items.append({"title": name, "url": m.group(2), "available": True})
            elif l_clean and not l_clean.startswith("#"):
                items.append({"title": l_clean, "url": None, "available": False})

        if items:
            categories.append({"category": cat_title, "items": items})

    return categories


def migrate_archives(pages: dict):
    phil = pages.get("/faith/archives/philosophy")
    theo = pages.get("/faith/archives/theology")

    phil_data = parse_drive_archive(phil["content"], "philosophy") if phil else []
    theo_data = parse_drive_archive(theo["content"], "theology") if theo else []

    AUDIT_NOTES.append(
        "Theology Archives: Verify SS19 (Pauline Literature) & SS20 (Hebrews) — both currently share Drive ID 1in4gF4LCZG1OHFqSu2-mI831kjCD_Nwg."
    )

    write_json(
        DATA_DIR / "archives.json",
        {
            "philosophy": {
                "institute": "St. Joseph's Philosophical Institute (2013–2016)",
                "groups": phil_data,
            },
            "theology": {
                "institute": "Francesco Theological Institute (2017–2020)",
                "groups": theo_data,
            },
        },
    )
    print(
        f"[OK] archives.json -> {sum(len(g['items']) for g in phil_data)} Philosophy & {sum(len(g['items']) for g in theo_data)} Theology PDFs"
    )


# ============================================================================
# STEP 6: MAGNIFICA HUMANITAS (DEDUPLICATED E-READER CHAPTERS)
# ============================================================================

MH_CHAPTER_MAP = [
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_introduction", "introduction", "முன்னுரை", 0),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_01", "chapter-01", "அதிகாரம் 1: நற்செய்திக்குப் பிரமாணிக்கமான ஆற்றல்மிக்க அணுகுமுறை", 1),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_02", "chapter-02", "அதிகாரம் 2: திருஅவையின் சமூகக் கோட்பாட்டின் அடிப்படைகளும் கொள்கைகளும்", 2),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_03", "chapter-03", "அதிகாரம் 3: தொழில்நுட்பமும் ஆதிக்கமும்", 3),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_04", "chapter-04", "அதிகாரம் 4: மாற்றங்களின் காலத்தில் மனிதகுலத்தைப் பாதுகாத்தல்", 4),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_05", "chapter-05", "அதிகாரம் 5: அதிகாரத்தின் கலாச்சாரமும் அன்பின் நாகரிகமும்", 5),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_conclusion", "conclusion", "முடிவுரை", 6),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_footnote", "footnotes", "அடிக்குறிப்புகள் (Footnotes)", 7),
    ("/faith/magnifica-humanitas/magnifica-humanitas_pages/mh_acknowledgement", "acknowledgement", "Documentation & AI Translation Methodology", 8),
]


def deduplicate_encyclical_blocks(text: str, slug: str) -> str:
    """Removes exact duplicate paragraphs/headings caused by copy-paste errors in MH_02 & MH_03."""
    paragraphs = re.split(r"\n\s*\n", text)
    cleaned = []
    seen_long_paras = set()
    removed = 0

    for p in paragraphs:
        p_stripped = p.strip()
        if not p_stripped:
            continue
        # Remove bottom prev/next navigation links (handled natively by Astro ReaderLayout)
        if re.match(r"^\[(<<<|.*>>>)\]", p_stripped) or re.match(r"^\[(முடிவுரை|அடிக்குறிப்புகள்)\]\(", p_stripped):
            continue
        # Strip leaked AI copy-paste note in acknowledgement
        if "(Note: You can copy/paste this block at the end of your published translation" in p_stripped:
            AUDIT_NOTES.append("MH_Acknowledgement: Stripped leaked AI copy/paste instruction note.")
            continue

        # Normalize paragraph body ignoring leading number ("59. " vs "73. ")
        norm = re.sub(r"^\d+\.\s*", "", p_stripped)
        norm = re.sub(r"\s+", " ", norm).strip()

        if len(norm) > 90:
            if norm in seen_long_paras:
                removed += 1
                continue
            seen_long_paras.add(norm)

        cleaned.append(p_stripped)

    if removed > 0:
        AUDIT_NOTES.append(f"Magnifica Humanitas ({slug}): Automatically removed {removed} duplicated paragraphs.")

    # Remove consecutive duplicate short headings left behind after dedup
    final_paras = []
    for i, p in enumerate(cleaned):
        if len(p) <= 90 and i > 0 and p in cleaned[:i] and len(p) > 15:
            # Skip repeated section headings that belonged to the duplicated block
            if slug in ("chapter-02", "chapter-03"):
                continue
        final_paras.append(p)

    return "\n\n".join(final_paras)


def migrate_magnifica_humanitas(pages: dict):
    count = 0
    for idx, (path, slug, title, order) in enumerate(MH_CHAPTER_MAP):
        page = pages.get(path)
        if not page:
            continue
        body = fix_split_markdown_links(page["content"])
        body = deduplicate_encyclical_blocks(body, slug)
        body = clean_markdown_headings(body)

        prev_slug = MH_CHAPTER_MAP[idx - 1][1] if idx > 0 else None
        next_slug = MH_CHAPTER_MAP[idx + 1][1] if idx < len(MH_CHAPTER_MAP) - 1 else None

        write_md(
            CONTENT_DIR / "magnifica-humanitas" / f"{slug}.md",
            {
                "title": title,
                "slug": slug,
                "order": order,
                "prev": prev_slug,
                "next": next_slug,
            },
            body,
        )
        count += 1
    print(f"[OK] src/content/magnifica-humanitas/ -> {count} cleaned chapters")


# ============================================================================
# STEP 7: SERAPHIC WAY OF THE CROSS (12 LANGUAGES)
# ============================================================================

SWC_LANGS = [
    ("swc_eng", "en", "English", "English", False),
    ("swc_tam", "ta", "Tamil", "தமிழ்", False),
    ("swc_ita", "it", "Italian", "Italiano", False),
    ("swc_fra", "fr", "French", "Français", False),
    ("swc_mex", "mx", "Spanish (Mexico)", "Español (México)", False),
    ("swc_spa", "es", "Spanish", "Español", False),
    ("swc_hin", "hi", "Hindi", "हिंदी", True),
    ("swc_kan", "kn", "Kannada", "ಕನ್ನಡ", True),
    ("swc_kon", "kok", "Konkani", "ಕೊಂಕಣಿ", True),
    ("swc_mal", "ml", "Malayalam", "മലയാളം", True),
    ("swc_tel", "te", "Telugu", "తెలుగు", True),
    ("swc_odi", "or", "Odia", "ଓଡ଼ିଆ", True),
]


def migrate_seraphic_way(pages: dict, download_imgs: bool):
    station_image_cache = {}
    count = 0

    for suffix, code, eng_name, native_name, ai_flag in SWC_LANGS:
        page = pages.get(f"/faith/writings/seraphic-way-of-the-cross_1/{suffix}")
        if not page:
            continue

        body = page["content"]
        # Remove back-to-index button
        body = re.sub(r"\[🔙Index - All Languages\]\([^)]+\)", "", body)

        # Clean Konkani stray `#` on body paragraphs (Stations 9-14)
        if code == "kok":
            fixed_lines = []
            for l in body.splitlines():
                if l.startswith("#") and not any(
                    k in l for k in ["ಸ್ಥಳ್:", "ನಿಮಾಣೆಂ ಮಾಗ್ಣೆಂ", "ಮುಕ್ಲೆಂಪಣ್", "ಸೆರಾಫಿಕ್"]
                ):
                    fixed_lines.append(l.lstrip("#").strip())
                else:
                    fixed_lines.append(l)
            body = "\n".join(fixed_lines)
            AUDIT_NOTES.append("SWC (Konkani): Cleaned stray '#' heading markers on Stations 9-14.")

        # Fix Tamil word inside Hindi footer
        if code == "hi" and "அற்புதராஜ்" in body:
            body = body.replace("அற்புதராஜ் (Arputharaj)", "अर्पुतराज (Arputharaj)")
            AUDIT_NOTES.append("SWC (Hindi): Fixed mixed Tamil script in author credit.")

        # Flag known cross-language pastes for 1-click Antigravity translation fix
        needs_review = False
        if code == "kn" and "सातवाँ पड़ाव" in body:
            needs_review = True
            body = body.replace(
                "#सातवाँ पड़ाव",
                "<!-- TODO_ANTIGRAVITY: Translate Station 7 from Hindi into Kannada -->\n## सातवाँ पड़ाव",
            )
            AUDIT_NOTES.append("SWC (Kannada): Station 7 is in Hindi — marked with TODO_ANTIGRAVITY for translation.")

        if code == "or" and "పదమూడవ స్థలం" in body:
            needs_review = True
            body = body.replace(
                "#పదమూడవ స్థలం",
                "<!-- TODO_ANTIGRAVITY: Translate Station 13 from Telugu into Odia -->\n## పదమూడవ స్థలం",
            )
            AUDIT_NOTES.append("SWC (Odia): Station 13 is in Telugu — marked with TODO_ANTIGRAVITY for translation.")

        if code == "ml" and "ಸಂಜೆವ್ಣ್ ಆನಿ ನಿರ್ಮಣ್" in body:
            needs_review = True
            body = body.replace(
                "ಸಂಜೆವ್ಣ್ ಆನಿ ನಿರ್ಮಣ್",
                "<!-- TODO_ANTIGRAVITY: Replace Konkani credits with Malayalam -->\nಸಂಜೆವ್ಣ್ ಆನಿ ನಿರ್ಮಣ್",
            )
            AUDIT_NOTES.append("SWC (Malayalam): Bottom credits are in Konkani — marked with TODO_ANTIGRAVITY.")

        # Deduplicate & optionally localize the 14 shared station images
        def replace_img(match):
            url = match.group(1)
            if url not in station_image_cache:
                idx = len(station_image_cache)
                station_image_cache[url] = download_image(
                    url, "stations", f"station_{idx:02d}", download_imgs
                )
            return f"![]({station_image_cache[url]})"

        body = re.sub(r"!\[\]\((https?://[^)]+)\)", replace_img, body)
        body = clean_markdown_headings(fix_split_markdown_links(body))

        write_md(
            CONTENT_DIR / "seraphic-way" / f"{code}.md",
            {
                "langCode": code,
                "englishName": eng_name,
                "nativeName": native_name,
                "title": f"Seraphic Way of the Cross ({eng_name})",
                "aiTranslated": ai_flag,
                "needsReview": needs_review,
            },
            body,
        )
        count += 1

    print(f"[OK] src/content/seraphic-way/ -> {count} language editions")


# ============================================================================
# STEP 8: STANDALONE WRITINGS (AI PRIEST, AADHAVAN GEETHAM, KUDILUM KURUSUM)
# ============================================================================

def migrate_writings(pages: dict):
    mapping = [
        ("/faith/writings/ai-priest", "ai-priest", "AI Priest: An Open Letter (ஒரு AI-சுவாமியாரின் கடுதாசி)", "Bilingual (Tamil & English)"),
        ("/faith/writings/ஆதவன-கதமம-ஆணடவர-சலவயம", "aadhavan-geetham", "ஆதவன் கீதமும் ஆண்டவர் சிலுவையும்", "Tamil"),
        ("/faith/writings/கடலம-கரசம", "kudilum-kurusum", "குடிலும் குருசும்", "Tamil"),
    ]
    for path, slug, title, lang in mapping:
        page = pages.get(path)
        if not page:
            continue
        body = fix_split_markdown_links(page["content"])
        body = body.replace("https://www.josephcap.com/creatives/about-me", "/about-me")
        body = clean_markdown_headings(body)
        write_md(
            CONTENT_DIR / "writings" / f"{slug}.md",
            {"title": title, "slug": slug, "language": lang},
            body,
        )
    print("[OK] src/content/writings/ -> ai-priest.md, aadhavan-geetham.md, kudilum-kurusum.md")


# ============================================================================
# STEP 9: ORIGINAL MUSIC ALBUMS (ALL 7 ALBUMS + LYRICS + YOUTUBE)
# ============================================================================

ALBUM_PAGES = [
    ("vizhigalile", "விழிகளிலே (Vizhigalile)", "2010", "Era I: The Genesis", "/art/music/albums/வழகளல"),
    ("anbanay", "அன்பனே (Anbanay)", "2013", "Era II: The Novitiate Anthology", "/art/music/albums/அனபன"),
    ("franciscan-hymns", "அசிசியின் ராகம் (Franciscan Hymns)", "2012–2013", "Era II: The Novitiate Anthology", "/art/music/albums/franciscan-hymns"),
    ("other-languages", "Multilingual Hymns", "2013", "Era II: The Novitiate Anthology", "/art/music/albums/other-languages"),
    ("english", "English Hymns", "2013", "Era II: The Novitiate Anthology", "/art/music/albums/english"),
    ("friary", "Friary Echoes", "2013–2016", "Era III: The Pursuit of Wisdom", "/art/music/albums/friary"),
    ("francesco", "Francesco Fragrance", "2017–2020", "Era IV: The Word Documented", "/art/music/albums/francesco"),
]


def migrate_albums(pages: dict, download_imgs: bool):
    albums = []
    for slug, title, year, era, path in ALBUM_PAGES:
        page = pages.get(path)
        if not page:
            continue

        blocks = [b.strip() for b in page["content"].split("\n---\n") if b.strip()]
        tracks = []

        # Skip TOC block (first 1-2 blocks) and parse track blocks
        for i, block in enumerate(blocks):
            yt_id = extract_youtube_id(block)
            img_m = re.search(r"!\[\]\((https?://[^)]+)\)", block)

            # Determine track title and lyrics
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            if not lines:
                continue

            if yt_id or img_m:
                # Try to find heading inside block or use previous single-line heading block
                track_title = ""
                lyrics_lines = []
                for l in lines:
                    if "Watch on YouTube" in l or l.startswith("![]("):
                        continue
                    if not track_title and l.startswith("#"):
                        track_title = l.lstrip("#").strip()
                    else:
                        lyrics_lines.append(l)

                if not track_title and i > 0:
                    prev_lines = [pl.strip() for pl in blocks[i - 1].splitlines() if pl.strip()]
                    if len(prev_lines) == 1 and len(prev_lines[0]) < 80:
                        track_title = prev_lines[0].lstrip("#").strip()

                if not track_title:
                    track_title = f"Track {len(tracks) + 1}"

                lyric_img = (
                    download_image(img_m.group(1), "albums", f"{slug}_{len(tracks):02d}", download_imgs)
                    if img_m
                    else None
                )

                tracks.append(
                    {
                        "title": track_title,
                        "youtubeId": yt_id,
                        "lyrics": "\n".join(lyrics_lines).strip() or None,
                        "lyricSheetImage": lyric_img,
                    }
                )

        albums.append(
            {
                "slug": slug,
                "title": title,
                "year": year,
                "era": era,
                "trackCount": len(tracks),
                "tracks": tracks,
            }
        )

    write_json(DATA_DIR / "albums.json", {"albums": albums})
    print(f"[OK] albums.json -> {len(albums)} albums ({sum(a['trackCount'] for a in albums)} tracks)")


# ============================================================================
# STEP 10: DBIMA FILMS, CHRONICLES & PROFILE JSON
# ============================================================================

def migrate_core_metadata():
    films = [
        {
            "id": "the-barren-field",
            "title": "The Barren Field",
            "alternateTitle": "தரிசு நிலம் • Le Champ Stérile",
            "year": "2025",
            "status": "Released",
            "language": "Tamil (French & English Subtitles)",
            "institution": "DBIMA — Don Bosco International Media Academy, Paris",
            "youtubeId": "9KjL8u_1ip4",
            "tagline": "A barren field is not the end of life—it is quiet waiting for a new seed.",
            "synopsis": "In a quiet village church in Tamil Nadu, Priya—five years into marriage without a child—is haunted by guilt over a past mistake and pushed to the brink of despair. Her encounter with Capuchin priest Fr. Prabhu (Br. Johnson of the Créteil fraternity) transforms confession into renewed hope.",
            "directorNotes": "Selected out of 15 student screenplays at DBIMA Paris for full-class production, marking the first-ever Tamil-language film directed at the academy. Generative AI served as the production office—bridging the language divide with AI storyboards, automated schedules, real-time on-set translation, French subtitles, and a Suno AI score.",
            "techStack": [
                "Gemini Pro (Script & Set Translation)",
                "AI Storyboarding",
                "Google AI Studio (French Subtitles)",
                "Suno AI (Original Score)",
            ],
        },
        {
            "id": "dbima-halloween",
            "title": "DBIMA Halloween",
            "alternateTitle": "Zero-Budget Fully AI Short Film",
            "year": "2025",
            "status": "Festival Entry",
            "language": "English / Visual Cinema",
            "institution": "DBIMA Film Festival, Paris",
            "youtubeId": "Tb4jca_gwuc",
            "tagline": "From blank page to finalized cinematic render in 3 hours—at zero dollar budget.",
            "synopsis": "An experimental, end-to-end generative AI film created for the DBIMA Film Festival in Paris, integrating digital-twin likeness into artificially generated scenes with consistent cinematic lighting.",
            "directorNotes": "Completed in 3 hours total work, earning critical acclaim and prompting DBIMA to invite Fr. Joseph to teach AI creative-disruption techniques to Master's peers.",
            "techStack": [
                "Gemini (Instant Script Conceptualization)",
                "Google Flow (Digital-Twin Integration)",
                "End-to-End Generative Cinema",
            ],
        },
        {
            "id": "jesus-antivirus",
            "title": "Jesus: an Anti-Virus",
            "alternateTitle": "Hybrid AI Studio • Eden OS",
            "year": "2026",
            "status": "Work in Progress",
            "language": "Sci-Fi / Digital Parable",
            "institution": "DBIMA Paris • Solo Hybrid AI Studio",
            "youtubeId": None,
            "resourceUrl": "https://drive.google.com/drive/folders/15Pd7YE8soTG06OIS8ssCAB2z_p6gQrpd?usp=drive_link",
            "tagline": "When the human network is corrupted, only a divine patch can restore the system.",
            "synopsis": "A technically ambitious narrative combining live-action 4K cinematography with fully functional interactive on-screen software ('Eden OS') built from scratch via Gemini Code.",
            "directorNotes": "Architected as a playable HTML operating system through 25 prompt-engineering iterations so actors could interact live on set, paired with Google Veo 3, Flow 3, RTX 3090 video-to-video VFX, and DaVinci Resolve Studio 20.",
            "techStack": [
                "Gemini Code (Eden OS HTML Emulator)",
                "Google Veo 3 & Flow 3",
                "RTX 3090 Video-to-Video VFX",
                "DaVinci Resolve Studio 20",
            ],
        },
    ]

    chronicles = [
        {"title": "Simple Profession", "year": "2013", "place": "Assisi Ashram", "date": "09-05-2013", "youtubeId": "MAjyMddQ9d0"},
        {"title": "Diaconate Ordination", "year": "2020", "place": "Francesco", "date": "19-07-2020", "youtubeId": "lGdBNyQKFf4"},
        {"title": "Malayadipatty E-Book Release", "year": "2020", "place": "Francesco", "date": "19-07-2020", "youtubeId": "4Y8cx9jeOs4"},
        {"title": "Priestly Ordination", "year": "2021", "place": "Francesco", "date": "10-04-2021", "youtubeId": "qxpPFg8Ai2c"},
        {"title": "First Holy Mass", "year": "2021", "place": "Malayadipatty", "date": "11-04-2021", "youtubeId": "FlnLwo0tf6g"},
        {"title": "Birthday Thanksgiving Mass", "year": "2021", "place": "Amalashram", "date": "20-04-2021", "youtubeId": "LMS25YkEyIA"},
    ]

    write_json(DATA_DIR / "films.json", {"dbimaFilms": films})
    write_json(DATA_DIR / "chronicles.json", {"events": chronicles})
    print("[OK] films.json & chronicles.json")


# ============================================================================
# MAIN RUNNER
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Migrate josephcap.com bundle to Astro data/content.")
    parser.add_argument(
        "--bundle",
        default="JOSEPHCAP_COMPLETE_WEBSITE_BUNDLE.md",
        help="Path to the master markdown bundle",
    )
    parser.add_argument(
        "--download-images",
        action="store_true",
        help="Download remote images locally to public/images/",
    )
    args = parser.parse_args()

    bundle_path = Path(args.bundle)
    if not bundle_path.exists():
        raise SystemExit(f"[ERROR] Bundle not found at: {bundle_path.resolve()}")

    ensure_dirs()
    pages = parse_bundle(bundle_path)
    print(f"Loaded {len(pages)} pages from {bundle_path.name}\n")

    migrate_vetrisaipadal(pages)
    migrate_workshops(pages, args.download_images)
    migrate_ai_projects(pages)
    migrate_archives(pages)
    migrate_magnifica_humanitas(pages)
    migrate_seraphic_way(pages, args.download_images)
    migrate_writings(pages)
    migrate_albums(pages, args.download_images)
    migrate_core_metadata()

    # Write Audit Report for Antigravity review
    report_lines = [
        "# Migration Audit & Cleanup Report",
        "",
        "## Automated Fixes & Remaining Manual Checks",
        "",
    ] + [f"- {note}" for note in AUDIT_NOTES]
    (ROOT / "MIGRATION_AUDIT_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\n[DONE] Migration complete! Check MIGRATION_AUDIT_REPORT.md for details.")


if __name__ == "__main__":
    main()
