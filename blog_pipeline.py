#!/usr/bin/env python3
"""
blog_pipeline.py — Automated Medical Blog Publisher
=====================================================
Runs weekly via GitHub Actions:
1. Generates new medical articles
2. Builds complete HTML website
3. Deploys to GitHub Pages automatically
100% free — no API cost, no hosting cost, no domain cost.
"""
import sys, shutil
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))
from article_gen import get_articles_for_week, get_all_articles
from site_gen    import generate_homepage, generate_article_page

OUTPUT_DIR = Path(__file__).parent / "docs"


def run():
    print(f"\n{'='*60}")
    print(f"  Pipeline : Automated Medical Blog Publisher")
    print(f"  Output   : GitHub Pages (docs/ folder)")
    print(f"{'='*60}\n")

    week = datetime.utcnow().isocalendar()[1]

    # Step 1: Get all articles (existing + new this week)
    print("📝  Step 1/3 — Loading article catalog ...")
    all_articles = get_all_articles()
    new_articles  = get_articles_for_week(week, count=3)
    print(f"  → Total articles in catalog: {len(all_articles)}")
    print(f"  → New articles this week: {len(new_articles)}")
    for a in new_articles:
        print(f"     • {a['title'][:60]}...")

    # Step 2: Build complete website
    print(f"\n🏗️   Step 2/3 — Building website ...")
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Generate all article pages
    for article in all_articles:
        generate_article_page(article, OUTPUT_DIR)

    # Generate homepage
    generate_homepage(all_articles, OUTPUT_DIR)

    # Create .nojekyll (tells GitHub Pages not to use Jekyll)
    (OUTPUT_DIR / ".nojekyll").touch()

    # Create sitemap.xml for Google indexing
    _generate_sitemap(all_articles, OUTPUT_DIR)

    # Create robots.txt
    _generate_robots(OUTPUT_DIR)

    # Create about page
    _generate_about(OUTPUT_DIR)

    print(f"\n📊  Step 3/3 — Build complete!")
    html_files = list(OUTPUT_DIR.rglob("*.html"))
    print(f"  → Total pages built: {len(html_files)}")
    print(f"  → Output directory: {OUTPUT_DIR}")
    print(f"\n✅  GitHub Pages will auto-deploy from docs/ folder")
    print(f"🌐  Live at: https://medlabguide.github.io")


def _generate_sitemap(articles: list, output_dir: Path):
    from src.site_gen import SITE_URL
    urls = [f"<url><loc>{SITE_URL}</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>"]
    for a in articles:
        urls.append(
            f"<url><loc>{SITE_URL}/{a['slug']}</loc>"
            f"<changefreq>monthly</changefreq><priority>0.8</priority></url>"
        )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>"""
    (output_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  [site] sitemap.xml generated ✓")


def _generate_robots(output_dir: Path):
    from src.site_gen import SITE_URL
    robots = f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml"""
    (output_dir / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"  [site] robots.txt generated ✓")


def _generate_about(output_dir: Path):
    from src.site_gen import (AUTHOR, AUTHOR_CREDENTIALS, SITE_NAME,
                               SITE_URL, CSS, _footer)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About {AUTHOR} | {SITE_NAME}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="container">
    <h1><a href="{SITE_URL}" style="color:white;text-decoration:none">{SITE_NAME}</a></h1>
    <p>Expert Medical Laboratory Information You Can Trust</p>
  </div>
</header>
<div class="container" style="max-width:800px;margin:30px auto;padding:0 20px">
  <div class="article-content">
    <h1>About {AUTHOR}</h1>
    <div class="meta">{AUTHOR_CREDENTIALS}</div>
    <p>{AUTHOR} is a clinical biochemistry expert with a PhD in Laboratory Medicine,
    specializing in renal biomarkers, metabolic disorders, and diagnostic testing.
    With extensive experience in both research and clinical laboratory settings,
    Dr. Bansal brings evidence-based expertise to complex medical topics,
    making them accessible to patients, students, and healthcare professionals alike.</p>
    <h2>Areas of Expertise</h2>
    <p>• Renal biomarkers and chronic kidney disease (CKD) staging</p>
    <p>• Metabolic disorders and hormonal markers</p>
    <p>• Clinical laboratory quality control and diagnostics</p>
    <p>• Beta-trace protein (BTP) research</p>
    <p>• Medical education and research methodology</p>
    <h2>Publications</h2>
    <p>Dr. Bansal has published peer-reviewed research on renal biomarkers including
    beta-trace protein as a novel marker for CKD staging, and is co-author of
    "Quality Control in Clinical Biochemistry: Principles and Practice"
    (CBS Publishers).</p>
    <h2>About This Website</h2>
    <p>This website provides free, expert-written educational content about medical
    laboratory tests, clinical biochemistry, and health topics. All content is
    written based on current medical evidence and clinical experience.</p>
    <p style="margin-top:15px;font-size:0.85em;color:#718096">
    <strong>Medical Disclaimer:</strong> Content on this site is for educational
    purposes only and does not constitute medical advice. Always consult a
    qualified healthcare professional for medical decisions.</p>
  </div>
</div>
{_footer()}"""
    about_dir = output_dir / "about"
    about_dir.mkdir(exist_ok=True)
    (about_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  [site] About page generated ✓")


if __name__ == "__main__":
    run()
