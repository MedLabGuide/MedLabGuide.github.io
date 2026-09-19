"""
site_gen.py
Generates a complete HTML website from articles.
Professional medical blog design — clean, fast, AdSense-ready.
No framework needed — pure HTML/CSS, works perfectly on GitHub Pages.
"""
from pathlib import Path
from datetime import datetime


AUTHOR = "Dr. Abhishek Bansal"
AUTHOR_CREDENTIALS = "PhD (Clinical Biochemistry) | Laboratory Medicine Expert | Published Researcher"
SITE_NAME = "Clinical Biochemistry Guide"
SITE_URL = "https://medlabguide.github.io"
TAGLINE = "Expert Medical Laboratory Information You Can Trust"
ADSENSE_CLIENT = "ca-pub-8996085625627875"  # Your real AdSense publisher ID


CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Georgia', serif; color: #2d3748; background: #f7fafc; line-height: 1.8; }
header { background: #1a365d; color: white; padding: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
header .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
header h1 { font-size: 1.8em; font-weight: bold; }
header p { font-size: 0.95em; opacity: 0.85; margin-top: 4px; }
nav { background: #2c5282; padding: 10px 0; }
nav .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
nav a { color: #bee3f8; text-decoration: none; margin-right: 20px; font-size: 0.95em; }
nav a:hover { color: white; }
.container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
.main-grid { display: grid; grid-template-columns: 1fr 300px; gap: 30px; margin: 30px auto; max-width: 1100px; padding: 0 20px; }
.article-card { background: white; border-radius: 8px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #2c5282; }
.article-card h2 { font-size: 1.3em; color: #1a365d; margin-bottom: 10px; }
.article-card h2 a { text-decoration: none; color: inherit; }
.article-card h2 a:hover { color: #2c5282; }
.article-card .meta { font-size: 0.85em; color: #718096; margin-bottom: 12px; }
.article-card .excerpt { color: #4a5568; font-size: 0.95em; }
.article-card .read-more { display: inline-block; margin-top: 12px; color: #2c5282; font-weight: bold; text-decoration: none; font-size: 0.9em; }
.sidebar { }
.sidebar-widget { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.sidebar-widget h3 { color: #1a365d; font-size: 1em; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #bee3f8; }
.sidebar-widget ul { list-style: none; }
.sidebar-widget ul li { padding: 6px 0; border-bottom: 1px solid #f0f4f8; }
.sidebar-widget ul li a { text-decoration: none; color: #2c5282; font-size: 0.9em; }
.author-box { background: #ebf8ff; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
.author-box h3 { color: #1a365d; margin-bottom: 8px; }
.author-box p { font-size: 0.9em; color: #4a5568; }
footer { background: #1a365d; color: #bee3f8; text-align: center; padding: 30px 20px; margin-top: 40px; font-size: 0.9em; }
footer a { color: #90cdf4; text-decoration: none; }
.disclaimer { background: #fffbeb; border: 1px solid #f6e05e; border-radius: 6px; padding: 15px; margin: 20px 0; font-size: 0.85em; color: #744210; }
/* Article page styles */
.article-content { background: white; border-radius: 8px; padding: 35px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.article-content h1 { font-size: 1.8em; color: #1a365d; margin-bottom: 10px; line-height: 1.4; }
.article-content .meta { color: #718096; font-size: 0.9em; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #f0f4f8; }
.article-content h2 { font-size: 1.3em; color: #2c5282; margin: 25px 0 12px; padding-left: 12px; border-left: 3px solid #2c5282; }
.article-content p { margin-bottom: 15px; color: #4a5568; }
.faq-section { background: #f0f4f8; border-radius: 8px; padding: 20px; margin-top: 25px; }
.faq-section h2 { color: #1a365d; margin-bottom: 15px; border: none; padding: 0; }
.faq-item { margin-bottom: 15px; }
.faq-item strong { color: #2c5282; display: block; margin-bottom: 5px; }
.breadcrumb { font-size: 0.85em; color: #718096; margin: 15px 0; }
.breadcrumb a { color: #2c5282; text-decoration: none; }
.ad-placeholder { background: #f0f4f8; border: 2px dashed #cbd5e0; border-radius: 6px; padding: 20px; text-align: center; color: #a0aec0; font-size: 0.85em; margin: 20px 0; min-height: 90px; display: flex; align-items: center; justify-content: center; }
@media(max-width:768px) { .main-grid { grid-template-columns: 1fr; } }
"""


def _header(title: str, description: str, canonical: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | {SITE_NAME}</title>
<meta name="description" content="{description}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<!-- Google Site Verification -->
<meta name="google-site-verification" content="CXS6yGB8E5wQurV5Dm6EbxVwCE3LKtIJzU6nF59D6cc" />
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8996085625627875" crossorigin="anonymous"></script>
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="container">
    <h1><a href="{SITE_URL}" style="color:white;text-decoration:none">{SITE_NAME}</a></h1>
    <p>{TAGLINE}</p>
  </div>
</header>
<nav>
  <div class="container">
    <a href="{SITE_URL}">Home</a>
    <a href="{SITE_URL}/lab-tests">Lab Tests</a>
    <a href="{SITE_URL}/clinical-biochemistry">Clinical Biochemistry</a>
    <a href="{SITE_URL}/about">About Dr. Bansal</a>
  </div>
</nav>"""


def _footer() -> str:
    year = datetime.utcnow().year
    return f"""<footer>
  <p>© {year} {SITE_NAME} | Written by <strong>{AUTHOR}</strong></p>
  <p style="margin-top:8px">{AUTHOR_CREDENTIALS}</p>
  <p style="margin-top:12px;font-size:0.8em;opacity:0.7">
    <a href="{SITE_URL}/disclaimer">Medical Disclaimer</a> |
    <a href="{SITE_URL}/privacy">Privacy Policy</a> |
    <a href="{SITE_URL}/contact">Contact</a>
  </p>
  <p style="margin-top:10px;font-size:0.8em;opacity:0.6">
    The information on this site is for educational purposes only and does not constitute medical advice.
    Always consult a qualified healthcare professional for diagnosis and treatment.
  </p>
</footer>
</body>
</html>"""


def _sidebar(all_articles: list) -> str:
    recent = all_articles[:5]
    links = "\n".join(
        f'<li><a href="{SITE_URL}/{a["slug"]}">{a["title"][:55]}...</a></li>'
        for a in recent
    )
    return f"""<aside class="sidebar">
  <div class="author-box">
    <h3>👨‍⚕️ {AUTHOR}</h3>
    <p>{AUTHOR_CREDENTIALS}</p>
    <p style="margin-top:8px;font-size:0.85em">Expert in renal biomarkers, metabolic disorders, and clinical laboratory medicine.</p>
  </div>
  <div class="sidebar-widget">
    <h3>📚 Recent Articles</h3>
    <ul>{links}</ul>
  </div>
  <div class="sidebar-widget">
    <h3>🔬 Categories</h3>
    <ul>
      <li><a href="{SITE_URL}/lab-tests">Lab Test Explanations</a></li>
      <li><a href="{SITE_URL}/clinical-biochemistry">Clinical Biochemistry</a></li>
      <li><a href="{SITE_URL}/patient-guides">Patient Guides</a></li>
      <li><a href="{SITE_URL}/research">Research Updates</a></li>
    </ul>
  </div>
  <!-- AdSense Sidebar Ad -->
  <div class="ad-placeholder">Advertisement<br>(AdSense ad will appear here after approval)</div>
</aside>"""


def generate_homepage(all_articles: list, output_dir: Path):
    """Generate the homepage with article listings."""
    cards = ""
    for a in all_articles:
        excerpt = a["sections"][0][1][:200].replace('\n', ' ') + "..."
        date = datetime.utcnow().strftime("%B %d, %Y")
        cards += f"""
<div class="article-card">
  <h2><a href="{SITE_URL}/{a['slug']}">{a['title']}</a></h2>
  <div class="meta">By {AUTHOR} | {date} | {a['category'].replace('-', ' ').title()}</div>
  <div class="excerpt">{excerpt}</div>
  <a href="{SITE_URL}/{a['slug']}" class="read-more">Read Full Article →</a>
</div>"""

    html = _header(
        f"Medical Laboratory Tests & Clinical Biochemistry Guide",
        f"Expert explanations of medical lab tests, clinical biochemistry, and patient guides by {AUTHOR}, PhD Clinical Biochemistry.",
        SITE_URL
    )
    html += f"""
<div class="main-grid">
  <main>
    <div class="disclaimer">
      ⚕️ <strong>Medical Disclaimer:</strong> This site provides educational information only.
      Always consult your doctor for medical advice, diagnosis, or treatment.
    </div>
    <!-- AdSense Banner Ad -->
    <div class="ad-placeholder" style="min-height:90px">Advertisement (AdSense banner will appear here)</div>
    {cards}
  </main>
  {_sidebar(all_articles)}
</div>"""
    html += _footer()

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  [site] Homepage generated ✓")


def generate_article_page(article: dict, output_dir: Path):
    """Generate individual article HTML page."""
    content_html = ""
    for heading, body in article["sections"]:
        paragraphs = ""
        for para in body.split('\n'):
            para = para.strip()
            if para:
                para = para.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                para = para.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                para = para.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                paragraphs += f"<p>{para}</p>\n"
        content_html += f"<h2>{heading}</h2>\n{paragraphs}\n"
        content_html += '<div class="ad-placeholder" style="min-height:60px">Advertisement</div>\n'

    faq_html = ""
    for q, a in article.get("faq", []):
        faq_html += f'<div class="faq-item"><strong>Q: {q}</strong><p>{a}</p></div>'

    date = datetime.utcnow().strftime("%B %d, %Y")
    keywords = ", ".join(article["keywords"])

    html = _header(article["title"], article["meta_description"],
                   f"{SITE_URL}/{article['slug']}")
    html += f"""
<div class="main-grid">
  <main>
    <div class="breadcrumb">
      <a href="{SITE_URL}">Home</a> → 
      <a href="{SITE_URL}/{article['category']}">{article['category'].replace('-',' ').title()}</a> → 
      {article['title'][:40]}...
    </div>
    <article class="article-content" itemscope itemtype="https://schema.org/MedicalWebPage">
      <h1 itemprop="name">{article['title']}</h1>
      <div class="meta">
        By <strong>{AUTHOR}</strong> | {AUTHOR_CREDENTIALS} | Published: {date}
      </div>
      <div class="disclaimer">
        ⚕️ <strong>Medical Disclaimer:</strong> This article is for educational purposes only.
        Consult your healthcare provider for medical advice specific to your situation.
      </div>
      <!-- AdSense Top Ad -->
      <div class="ad-placeholder">Advertisement (AdSense ad will appear here after approval)</div>
      <div itemprop="text">
        {content_html}
      </div>
      {f'<div class="faq-section"><h2>Frequently Asked Questions</h2>{faq_html}</div>' if faq_html else ''}
      <!-- AdSense Bottom Ad -->
      <div class="ad-placeholder" style="margin-top:20px">Advertisement</div>
    </article>
  </main>
  <aside class="sidebar">
    <div class="author-box">
      <h3>👨‍⚕️ About the Author</h3>
      <p><strong>{AUTHOR}</strong></p>
      <p>{AUTHOR_CREDENTIALS}</p>
      <p style="margin-top:8px;font-size:0.85em">Published researcher specializing in renal biomarkers and clinical laboratory medicine.</p>
    </div>
    <div class="ad-placeholder" style="min-height:250px">Advertisement</div>
  </aside>
</div>"""
    html += _footer()

    article_dir = output_dir / article["slug"]
    article_dir.mkdir(parents=True, exist_ok=True)
    (article_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  [site] Article generated: {article['slug']} ✓")
