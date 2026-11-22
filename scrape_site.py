import os
import re
import json
import time
import zipfile
from urllib.parse import urljoin, urlparse, unquote
import requests
from bs4 import BeautifulSoup
import html2text

BASE_DOMAIN = "www.josephcap.com"
START_URL = "https://www.josephcap.com/home"
OUTPUT_DIR = os.path.abspath("scraped_site")
PAGES_DIR = os.path.join(OUTPUT_DIR, "pages")
EMBEDS_DIR = os.path.join(OUTPUT_DIR, "embeds")
BUNDLE_MD_PATH = os.path.abspath("JOSEPHCAP_COMPLETE_WEBSITE_BUNDLE.md")
BUNDLE_JSON_PATH = os.path.abspath("JOSEPHCAP_COMPLETE_WEBSITE_BUNDLE.json")
BUNDLE_ZIP_PATH = os.path.abspath("josephcap_scraped_bundle.zip")

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(EMBEDS_DIR, exist_ok=True)

h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = False
h2t.body_width = 0
h2t.protect_links = True
h2t.unicode_snob = True

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_slug(url_path):
    path = unquote(url_path).strip("/")
    if not path or path == "home":
        return "home"
    # sanitize filename
    safe = re.sub(r'[\\/*?:"<>|]', "_", path)
    return safe.replace("/", "_")

def crawl_site():
    print(f"[*] Crawling {START_URL}...")
    visited = set()
    to_visit = [START_URL]
    discovered = []

    while to_visit:
        curr = to_visit.pop(0)
        parsed = urlparse(curr)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if clean_url in visited:
            continue
        visited.add(clean_url)

        try:
            r = requests.get(clean_url, headers=headers, timeout=12)
            if r.status_code != 200:
                print(f"[-] Status {r.status_code}: {clean_url}")
                continue
            discovered.append((clean_url, r.text))
            print(f"[+] [{len(discovered)}] Fetched: {parsed.path or '/'}")

            soup = BeautifulSoup(r.text, "lxml")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
                    continue
                full = urljoin(clean_url, href)
                p = urlparse(full)
                c_url = f"{p.scheme}://{p.netloc}{p.path}"
                if p.netloc == BASE_DOMAIN and c_url not in visited and c_url not in to_visit:
                    to_visit.append(c_url)
        except Exception as e:
            print(f"[!] Error fetching {clean_url}: {e}")
        time.sleep(0.1)

    print(f"[*] Crawl finished. Total pages: {len(discovered)}")
    return discovered

def process_page(url, html_content):
    soup = BeautifulSoup(html_content, "lxml")
    parsed = urlparse(url)
    slug = clean_slug(parsed.path)

    # 1. Page Title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        title = re.sub(r"\s*-\s*Google Sites$", "", title)
    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(strip=True) if h1 else slug

    # 2. Extract Custom Embeds (data-tile-id & data-code)
    embeds = []
    tile_divs = soup.find_all(attrs={"data-tile-id": True})
    for idx, t in enumerate(tile_divs):
        code = t.get("data-code", "")
        if code and len(code.strip()) > 50:
            embed_filename = f"{slug}_embed_{idx+1}.html"
            embed_path = os.path.join(EMBEDS_DIR, embed_filename)
            with open(embed_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # parse embed content to markdown
            embed_soup = BeautifulSoup(code, "lxml")
            embed_md = h2t.handle(str(embed_soup.body or embed_soup)).strip()
            embeds.append({
                "filename": embed_filename,
                "length": len(code),
                "markdown": embed_md
            })

    # 3. Clean Google Sites boilerplate
    for tag in soup.find_all(["nav", "header", "footer"]):
        tag.decompose()
    for tag in soup.find_all(attrs={"role": ["navigation", "banner", "contentinfo"]}):
        tag.decompose()
    for tag in soup.find_all(class_=re.compile(r"(banner|nav|header|footer|search|report-abuse)", re.I)):
        tag.decompose()

    # 4. Extract YouTube embeds & replace with clean markdown
    youtube_videos = []
    for ifr in soup.find_all("iframe"):
        src = ifr.get("src", "")
        m = re.search(r"youtube\.com/embed/([a-zA-Z0-9_-]+)", src)
        if m:
            vid = m.group(1)
            yt_url = f"https://www.youtube.com/watch?v={vid}"
            youtube_videos.append(yt_url)
            p = soup.new_tag("p")
            p.string = f"\n\n**[▶️ Watch on YouTube]({yt_url})**\n\n"
            ifr.replace_with(p)

    # 5. Extract Images
    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        alt = img.get("alt", "")
        if src and not src.startswith("data:"):
            images.append({"src": src, "alt": alt})

    # 6. Extract Section Content
    sections = soup.find_all("section")
    section_markdowns = []
    for s in sections:
        md = h2t.handle(str(s)).strip()
        # Clean repetitive whitespace
        md = re.sub(r"\n{3,}", "\n\n", md)
        if md:
            section_markdowns.append(md)

    main_content_md = "\n\n---\n\n".join(section_markdowns)

    # Combine embed markdown if section content is sparse
    if embeds and len(main_content_md.strip()) < 500:
        embed_sections = []
        for e in embeds:
            embed_sections.append(f"> **Interactive Application Embed (`{e['filename']}`):**\n\n" + e["markdown"])
        if main_content_md.strip():
            main_content_md = main_content_md + "\n\n---\n\n" + "\n\n---\n\n".join(embed_sections)
        else:
            main_content_md = "\n\n---\n\n".join(embed_sections)

    # Clean up empty headers or leftovers
    main_content_md = re.sub(r"##\s*\n+", "", main_content_md)
    main_content_md = re.sub(r"###\s*\n+", "", main_content_md)

    # Category grouping
    parts = parsed.path.strip("/").split("/")
    category = parts[0] if len(parts) > 1 else "root"
    if not category or category == "home":
        category = "root"

    page_data = {
        "url": url,
        "path": parsed.path or "/",
        "slug": slug,
        "category": category,
        "title": title,
        "youtube_videos": list(set(youtube_videos)),
        "image_count": len(images),
        "embed_count": len(embeds),
        "markdown": main_content_md.strip(),
        "embeds": embeds
    }

    # Save individual markdown file
    cat_dir = os.path.join(PAGES_DIR, category)
    os.makedirs(cat_dir, exist_ok=True)
    page_md_file = os.path.join(cat_dir, f"{slug}.md")
    
    with open(page_md_file, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"- **Original URL:** `{url}`\n")
        f.write(f"- **Path:** `{parsed.path}`\n")
        f.write(f"- **Category:** `{category}`\n\n")
        if youtube_videos:
            f.write(f"### Associated YouTube Videos\n")
            for yv in set(youtube_videos):
                f.write(f"- {yv}\n")
            f.write("\n")
        f.write(f"## Page Content\n\n")
        f.write(main_content_md if main_content_md else "_No text content extracted._\n")

    return page_data

def build_bundles(all_pages):
    print("[*] Generating consolidated Master Markdown Bundle...")
    
    # Sort pages: Root first, then Faith, Art, Science, etc.
    category_order = {"root": 0, "faith": 1, "art": 2, "science": 3}
    sorted_pages = sorted(all_pages, key=lambda p: (category_order.get(p["category"], 99), p["path"]))

    toc_lines = []
    bundle_content = []

    bundle_content.append("# Master Website Content Archive: josephcap.com")
    bundle_content.append("## Personal Website of Fr. Joseph Arputha Raj OFM Cap")
    bundle_content.append("> **Archive Generation Date:** 2026-11-22  ")
    bundle_content.append("> **Source:** [https://www.josephcap.com](https://www.josephcap.com)  ")
    bundle_content.append(f"> **Total Pages Archived:** {len(sorted_pages)}  ")
    bundle_content.append("> **Target Environment:** Google AI Studio (Gemini 2.5 Pro / Flash with 1M-2M context window)\n")
    bundle_content.append("---\n")

    bundle_content.append("## Table of Contents\n")
    for idx, p in enumerate(sorted_pages, 1):
        clean_anchor = re.sub(r'[^a-zA-Z0-9_-]', '', p['slug'].lower())
        toc_lines.append(f"{idx}. [{p['title']} (`{p['path']}`)](#page-{clean_anchor})")
    
    bundle_content.append("\n".join(toc_lines))
    bundle_content.append("\n\n---\n")

    for idx, p in enumerate(sorted_pages, 1):
        clean_anchor = re.sub(r'[^a-zA-Z0-9_-]', '', p['slug'].lower())
        bundle_content.append(f"<a id=\"page-{clean_anchor}\"></a>\n")
        bundle_content.append(f"# {idx}. {p['title']}")
        bundle_content.append(f"**URL:** `{p['url']}` | **Path:** `{p['path']}` | **Category:** `{p['category'].upper()}`\n")
        
        if p["youtube_videos"]:
            bundle_content.append("**Embedded YouTube Videos:**")
            for yv in p["youtube_videos"]:
                bundle_content.append(f"- {yv}")
            bundle_content.append("")

        if p["embeds"]:
            bundle_content.append(f"> ℹ️ *This page contains {len(p['embeds'])} custom interactive web application embed(s). The full standalone HTML source files are preserved in the `embeds/` directory.*")
            bundle_content.append("")

        bundle_content.append("### Content:")
        bundle_content.append(p["markdown"] if p["markdown"] else "_No body text content._")
        bundle_content.append("\n\n---\n")

    with open(BUNDLE_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(bundle_content))
    print(f"[+] Master Markdown Bundle written: {BUNDLE_MD_PATH} ({os.path.getsize(BUNDLE_MD_PATH)} bytes)")

    # Write Master JSON
    with open(BUNDLE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_pages, f, ensure_ascii=False, indent=2)
    print(f"[+] Master JSON Bundle written: {BUNDLE_JSON_PATH} ({os.path.getsize(BUNDLE_JSON_PATH)} bytes)")

    # Write ZIP Bundle
    print("[*] Creating portable ZIP archive...")
    with zipfile.ZipFile(BUNDLE_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(BUNDLE_MD_PATH, arcname=os.path.basename(BUNDLE_MD_PATH))
        zipf.write(BUNDLE_JSON_PATH, arcname=os.path.basename(BUNDLE_JSON_PATH))
        for root, _, files in os.walk(OUTPUT_DIR):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, os.path.dirname(OUTPUT_DIR))
                zipf.write(abs_path, arcname=rel_path)
    print(f"[+] Portable ZIP bundle written: {BUNDLE_ZIP_PATH} ({os.path.getsize(BUNDLE_ZIP_PATH)} bytes)")

def main():
    start_time = time.time()
    discovered_pages = crawl_site()
    all_pages_data = []

    for idx, (url, html_str) in enumerate(discovered_pages, 1):
        print(f"[{idx}/{len(discovered_pages)}] Processing: {url}")
        page_info = process_page(url, html_str)
        all_pages_data.append(page_info)

    build_bundles(all_pages_data)
    elapsed = time.time() - start_time
    print(f"\n[SUCCESS] Completed in {elapsed:.2f} seconds!")

if __name__ == "__main__":
    main()
