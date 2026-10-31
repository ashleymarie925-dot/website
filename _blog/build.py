#!/usr/bin/env python3
"""Builds the blog for ashleymariegurevich.com.

Write each post as a Markdown file in _blog/posts/ with a YAML header, then run:
    python3 _blog/build.py
It writes blog/<slug>.html for every post, blog/index.html, and refreshes the
blog entries in sitemap.xml and llms.txt. Folders starting with "_" are not
published by GitHub Pages, so this script and the Markdown sources stay private.
"""
import datetime as dt
import html
import json
import pathlib
import re

import markdown
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "_blog" / "posts"
OUT = ROOT / "blog"
SITE = "https://ashleymariegurevich.com"
AUTHOR = {
    "@type": "Person",
    "name": "Ashley Gurevich",
    "jobTitle": "Senior Mortgage Loan Officer",
    "url": SITE + "/",
    "image": SITE + "/headshot.jpg",
    "identifier": "NMLS #847540",
    "worksFor": {"@type": "Organization", "name": "CrossCountry Mortgage, LLC"},
}
CALENDLY = "https://calendly.com/ashleymariemortgageadvisor/30min"
APPLY = "https://app.crosscountrymortgage.com/#/signup?referrerId=ashley.gurevich%40ccm.com"


def esc(s):
    return html.escape(str(s), quote=True)


def fmt_date(d):
    return d.strftime("%B %-d, %Y")


def load_posts():
    posts = []
    for p in sorted(POSTS.glob("*.md")):
        raw = p.read_text()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        meta, body = yaml.safe_load(m.group(1)), m.group(2)
        if meta.get("draft"):
            continue
        meta["published"] = meta["published"] if isinstance(meta["published"], dt.date) else dt.date.fromisoformat(str(meta["published"]))
        upd = meta.get("updated") or meta["published"]
        meta["updated"] = upd if isinstance(upd, dt.date) else dt.date.fromisoformat(str(upd))
        md = markdown.Markdown(extensions=["tables", "toc", "attr_list", "md_in_html"])
        meta["html"] = md.convert(body)
        meta["words"] = len(re.findall(r"\w+", body))
        meta["url"] = f"{SITE}/blog/{meta['slug']}"
        posts.append(meta)
    posts.sort(key=lambda x: x["published"], reverse=True)
    return posts


CSS = """
:root{--bg:#0d0d0f;--bg2:#141417;--card:#1a1a1e;--line:#2a2a30;--gold:#c9a96a;--gold-soft:#d9bf8f;--text:#e8e6e1;--muted:#9b978f}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-weight:300}
h1,h2,h3{font-family:'Cormorant Garamond',serif;font-weight:600;letter-spacing:.4px}
a{color:var(--gold);text-decoration:none}
.wrap{max-width:1100px;margin:0 auto;padding:0 24px}
.eyebrow{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);font-weight:500}
nav{position:sticky;top:0;background:rgba(13,13,15,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);z-index:10}
.nav-inner{display:flex;justify-content:space-between;align-items:center;padding:18px 24px;max-width:1100px;margin:0 auto}
.logo{font-family:'Cormorant Garamond',serif;font-size:22px;color:var(--text)}
.logo span{color:var(--gold)}
.nav-links{display:flex;gap:28px;font-size:14px}
.nav-links a{color:var(--muted);transition:color .2s}
.nav-links a:hover,.nav-links a.on{color:var(--gold)}
.btn{display:inline-block;padding:13px 30px;border:1px solid var(--gold);color:var(--gold);font-size:13px;letter-spacing:2px;text-transform:uppercase;transition:all .25s;cursor:pointer;font-weight:400}
.btn:hover{background:var(--gold);color:#0d0d0f}
.btn.solid{background:var(--gold);color:#0d0d0f}
.btn.solid:hover{background:var(--gold-soft)}
.crumbs{font-size:12.5px;color:var(--muted);padding-top:26px}
.crumbs a{color:var(--muted)} .crumbs a:hover{color:var(--gold)}
/* post */
.post-head{padding:46px 0 34px;border-bottom:1px solid var(--line)}
.post-head h1{font-size:50px;line-height:1.08;margin:16px 0 18px;max-width:860px}
.post-head .dek{color:var(--muted);font-size:18px;max-width:720px}
.byline{display:flex;align-items:center;gap:14px;margin-top:26px;font-size:13.5px;color:var(--muted)}
.byline img{width:46px;height:46px;border-radius:50%;object-fit:cover;object-position:top;border:1px solid var(--gold)}
.byline b{color:var(--text);font-weight:500}
.post-grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:56px;padding:44px 0 70px}
.answer{background:var(--card);border-left:3px solid var(--gold);padding:22px 26px;margin-bottom:34px}
.answer .lbl{font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.answer p{color:var(--text);font-size:16.5px;margin:0}
.article{font-size:16.5px}
.article h2{font-size:34px;line-height:1.15;margin:44px 0 14px;color:var(--text)}
.article h3{font-size:24px;margin:30px 0 10px;color:var(--gold-soft)}
.article p{color:#c9c6bf;margin-bottom:18px}
.article strong{color:var(--text);font-weight:500}
.article ul,.article ol{margin:0 0 20px 22px;color:#c9c6bf}
.article li{margin-bottom:8px}
.article a{border-bottom:1px solid rgba(201,169,106,.4)}
.article blockquote{border-left:2px solid var(--gold);padding:6px 0 6px 22px;margin:26px 0;font-family:'Cormorant Garamond',serif;font-size:24px;font-style:italic;color:var(--text)}
.article blockquote p{color:var(--text);margin:0}
.post-photo{margin:30px 0 32px}
.post-photo img{width:100%;max-width:560px;display:block;border:1px solid var(--line)}
.post-photo figcaption{font-size:13px;color:var(--muted);margin-top:10px;font-style:italic;max-width:560px}
.article table{width:100%;border-collapse:collapse;margin:8px 0 26px;font-size:14.5px}
.article th{text-align:left;font-weight:500;color:var(--gold);border-bottom:1px solid var(--gold);padding:10px 12px;font-size:12px;letter-spacing:1.2px;text-transform:uppercase}
.article td{border-bottom:1px solid var(--line);padding:12px;color:#c9c6bf;vertical-align:top}
.article .tablewrap{overflow-x:auto}
aside .box{background:var(--card);border:1px solid var(--line);padding:24px;margin-bottom:18px;position:sticky;top:96px}
aside h3{font-size:22px;margin-bottom:8px}
aside p{font-size:14px;color:var(--muted);margin-bottom:16px}
aside .btn{display:block;text-align:center;margin-bottom:10px;padding:12px 10px}
aside .toc a{display:block;font-size:13.5px;color:var(--muted);padding:5px 0;border-bottom:1px solid var(--line)}
aside .toc a:hover{color:var(--gold)}
.faq{margin-top:46px}
.faq-item{border:1px solid var(--line);background:var(--card);margin-bottom:12px}
.faq-item summary{padding:18px 22px;cursor:pointer;font-weight:500;font-size:15px;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px}
.faq-item summary::after{content:'+';color:var(--gold);font-size:22px;font-weight:300}
.faq-item[open] summary::after{content:'\\2212'}
.faq-item .a{padding:0 22px 20px;color:var(--muted);font-size:14.5px}
.endcta{margin-top:50px;background:linear-gradient(135deg,#1c1a15,#141417);border:1px solid var(--gold);padding:38px 34px;text-align:center}
.endcta h2{font-size:32px;margin-bottom:10px}
.endcta p{color:var(--muted);max-width:560px;margin:0 auto 22px}
.endcta .row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.related{border-top:1px solid var(--line);padding:56px 0}
.related h2{font-size:30px;margin:10px 0 22px}
.updated{font-size:12.5px;color:var(--muted);margin-top:34px;font-style:italic}
.disclaim{font-size:12px;color:#6b6862;margin-top:18px;line-height:1.7}
/* index */
.blog-hero{padding:60px 0 40px;border-bottom:1px solid var(--line)}
.blog-hero h1{font-size:56px;line-height:1.05;margin:16px 0 16px}
.blog-hero p{color:var(--muted);font-size:17px;max-width:640px}
.cats{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.cat{border:1px solid var(--line);color:var(--muted);padding:9px 16px;border-radius:40px;font-size:13px;cursor:pointer;background:none;font-family:'Inter',sans-serif}
.cat.on,.cat:hover{border-color:var(--gold);color:var(--gold)}
.posts{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding:40px 0 80px}
.pcard{background:var(--card);border:1px solid var(--line);padding:28px 26px;display:flex;flex-direction:column;transition:border-color .25s,transform .25s}
.pcard:hover{border-color:var(--gold);transform:translateY(-2px)}
.pcard.feature{grid-column:span 3;padding:40px 40px}
.pcard.feature h2{font-size:40px}
.pcard h2{font-size:26px;line-height:1.15;color:var(--text);margin:10px 0 12px}
.pcard p{color:var(--muted);font-size:14.5px;flex:1}
.pcard .meta{font-size:12px;color:#7d7a73;margin-top:18px;letter-spacing:.5px}
.pcard .more{color:var(--gold);font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-top:14px}
footer{padding:44px 0;border-top:1px solid var(--line);font-size:11.5px;color:#6b6862;line-height:1.8}
footer a{color:#8a867e}
.mobile-bar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:50;background:rgba(13,13,15,.97);border-top:1px solid var(--gold);padding:10px 12px;gap:10px}
.mobile-bar a{flex:1;text-align:center;padding:12px 4px;font-size:12px;letter-spacing:1.5px;text-transform:uppercase}
@media(max-width:900px){
 .post-grid{grid-template-columns:1fr;gap:10px}
 aside .box{position:static}
 .posts{grid-template-columns:1fr}
 .pcard.feature{grid-column:span 1;padding:28px 24px}
 .pcard.feature h2{font-size:30px}
}
@media(max-width:820px){
 .mobile-bar{display:flex}body{padding-bottom:64px}
 .nav-links{display:none}
 .post-head h1{font-size:36px}
 .blog-hero h1{font-size:40px}
 .article h2{font-size:28px}
}
"""

NAV = """<nav><div class="nav-inner">
  <a class="logo" href="/">Ashley <span>Gurevich</span></a>
  <div class="nav-links">
    <a href="/#about">About</a><a href="/loan-programs">Loan Programs</a><a href="/buy-before-you-sell">Buy Before You Sell</a><a href="/blog/" class="on">Blog</a><a href="/#reviews">Reviews</a><a href="/#contact">Contact</a>
  </div>
  <a class="btn solid" href="sms:+19255509733">Text Me</a>
</div></nav>"""

FOOTER = """<footer>
  <div class="wrap">
    <div class="footer-brand" style="margin-bottom:14px">Ashley Gurevich &middot; Senior Loan Officer &middot; NMLS #847540</div>
    <p style="color:#8a867e;margin-bottom:10px">Ashley Gurevich at CrossCountry Mortgage &middot; 857 2nd Street Suite C, Brentwood, CA 94513 &middot; Phone: <a href="tel:+19255509733">(925) 550-9733</a> &middot; Email: <a href="mailto:ashley.gurevich@ccm.com">ashley.gurevich@ccm.com</a></p>
    <p style="margin-bottom:14px">
      <a href="https://www.instagram.com/AshleyMarieGurevich" target="_blank" rel="noopener">Instagram</a> &middot;
      <a href="https://www.facebook.com/AshleyMarieMortgageAdvisor/" target="_blank" rel="noopener">Facebook</a> &middot;
      <a href="https://www.experience.com/reviews/ashley-gurevich-454089" target="_blank" rel="noopener">Reviews</a> &middot;
      <a href="/blog/">Blog</a>
    </p>
    <p>Ashley Gurevich is a Senior Loan Officer with CrossCountry Mortgage, LLC. NMLS3029 | Branch NMLS #2831895. Licensed in CA, WA, VA. Equal Housing Opportunity. This is not a commitment to lend; all loans subject to underwriting approval, and program terms may change without notice. CrossCountry Mortgage, LLC, 2160 Superior Avenue, Cleveland, OH 44114.
    <a href="https://crosscountrymortgage.com/licensing-and-disclosures/" target="_blank" rel="noopener">Disclosures &amp; Licenses</a> &middot;
    <a href="https://crosscountrymortgage.com/privacy-policy/" target="_blank" rel="noopener">Privacy</a> &middot;
    <a href="https://nmlsconsumeraccess.org/EntityDetails.aspx/COMPANY/3029" target="_blank" rel="noopener">NMLS Consumer Access</a></p>
  </div>
</footer>
<div class="mobile-bar">
  <a class="btn solid" href="sms:+19255509733">Text Me</a>
  <a class="btn" href="tel:+19255509733">Call</a>
</div>"""


def head(title, desc, url, og_type, image, schemas):
    blocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="author" content="Ashley Gurevich">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="Ashley Gurevich Blog" href="{SITE}/blog/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
{blocks}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{NAV}
"""


def render_post(p, posts):
    url = p["url"]
    image = SITE + p.get("image", "/headshot.jpg")
    faq = p.get("faq") or []
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": p["title"],
            "description": p["description"],
            "url": url,
            "mainEntityOfPage": url,
            "image": image,
            "datePublished": p["published"].isoformat(),
            "dateModified": p["updated"].isoformat(),
            "author": AUTHOR,
            "publisher": {"@type": "Organization", "name": "Ashley Gurevich at CrossCountry Mortgage", "logo": {"@type": "ImageObject", "url": SITE + "/headshot.jpg"}},
            "about": p.get("keywords", []),
            "wordCount": p["words"],
            "articleSection": p.get("category", "Guides"),
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
            ],
        },
    ]
    if faq:
        schemas.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq],
        })

    body = p["html"].replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
    toc = "".join(
        f'<a href="#{m.group(1)}">{m.group(2)}</a>'
        for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    )
    faq_html = ""
    if faq:
        items = "".join(f'<details class="faq-item"><summary>{esc(f["q"])}</summary><div class="a">{esc(f["a"])}</div></details>' for f in faq)
        faq_html = f'<section class="faq" id="faq"><div class="eyebrow">Questions</div><h2 style="font-size:34px;margin:10px 0 20px">Straight answers</h2>{items}</section>'
    answer = ""
    if p.get("short_answer"):
        answer = f'<div class="answer"><div class="lbl">The short answer</div><p>{esc(p["short_answer"])}</p></div>'

    others = [o for o in posts if o["slug"] != p["slug"]][:3]
    rel_cards = "".join(
        f'<a class="pcard" href="/blog/{o["slug"]}"><div class="eyebrow">{esc(o.get("category","Guides"))}</div><h2>{esc(o["title"])}</h2><p>{esc(o["description"])}</p><div class="more">Read</div></a>'
        for o in others
    )
    for link in p.get("related_pages", []):
        rel_cards += f'<a class="pcard" href="{link["href"]}"><div class="eyebrow">Program</div><h2>{esc(link["title"])}</h2><p>{esc(link["text"])}</p><div class="more">Learn more</div></a>'
    related = f'<section class="related"><div class="wrap"><div class="eyebrow">Keep reading</div><h2>Related</h2><div class="posts" style="padding:0">{rel_cards}</div></div></section>' if rel_cards else ""

    upd = ""
    if p["updated"] != p["published"]:
        upd = f' &middot; Updated {fmt_date(p["updated"])}'
    mins = max(3, round(p["words"] / 230))

    return head(p.get("seo_title", p["title"]) + " | Ashley Gurevich", p["description"], url, "article", image, schemas) + f"""
<div class="wrap crumbs"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; {esc(p.get("category","Guides"))}</div>
<header class="post-head"><div class="wrap">
  <div class="eyebrow">{esc(p.get("category","Guides"))}</div>
  <h1>{esc(p["title"])}</h1>
  <p class="dek">{esc(p["description"])}</p>
  <div class="byline"><img src="/headshot.jpg" alt="Ashley Gurevich"><div><b>Ashley Gurevich</b>, Senior Loan Officer, NMLS #847540<br>{fmt_date(p["published"])}{upd} &middot; {mins} min read</div></div>
</div></header>
<div class="wrap post-grid">
  <article class="article">
    {answer}
    {body}
    {faq_html}
    <div class="endcta">
      <h2>{esc(p.get("cta_title","Let's map out your move."))}</h2>
      <p>{esc(p.get("cta_text","Every plan starts with one conversation. Text me and we'll look at your numbers together."))}</p>
      <div class="row"><a class="btn solid" href="{CALENDLY}" target="_blank" rel="noopener">{esc(p.get("cta_button","Book a Free Call"))}</a><a class="btn" href="sms:+19255509733">Text (925) 550-9733</a></div>
    </div>
    <p class="updated">Written by Ashley Gurevich, Senior Loan Officer at CrossCountry Mortgage (NMLS #847540), licensed in California, Washington and Virginia. Published {fmt_date(p["published"])}{upd}.</p>
    <p class="disclaim">This article is for general education and is not a commitment to lend or a loan approval. Program availability, terms and guidelines change and depend on your full application, credit, income, assets and property. Talk with a licensed loan officer about your specific situation. Equal Housing Opportunity.</p>
  </article>
  <aside>
    <div class="box">
      <h3>Talk it through</h3>
      <p>Tell me what you own, what you want to buy, and your timeline. I'll show you the options that fit.</p>
      <a class="btn solid" href="sms:+19255509733">Text Me</a>
      <a class="btn" href="{CALENDLY}" target="_blank" rel="noopener">Book a Call</a>
      {'<div class="toc" style="margin-top:18px"><div class="eyebrow" style="margin-bottom:6px">In this post</div>' + toc + '</div>' if toc else ''}
    </div>
  </aside>
</div>
{related}
{FOOTER}
</body>
</html>
"""


def render_index(posts):
    url = SITE + "/blog/"
    cats = sorted({p.get("category", "Guides") for p in posts})
    schemas = [{
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Ashley Gurevich Mortgage Blog",
        "url": url,
        "author": AUTHOR,
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": p["url"], "datePublished": p["published"].isoformat()} for p in posts],
    }]
    cards = ""
    for i, p in enumerate(posts):
        cls = "pcard feature" if i == 0 else "pcard"
        cards += f'<a class="{cls}" href="/blog/{p["slug"]}" data-c="{esc(p.get("category","Guides"))}"><div class="eyebrow">{esc(p.get("category","Guides"))}</div><h2>{esc(p["title"])}</h2><p>{esc(p["description"])}</p><div class="meta">{fmt_date(p["published"])}</div><div class="more">Read the post</div></a>'
    btns = '<button class="cat on" data-c="all">All</button>' + "".join(f'<button class="cat" data-c="{esc(c)}">{esc(c)}</button>' for c in cats)
    return head("Mortgage Blog: Buy Before You Sell, Self-Employed Loans & Bay Area Home Buying | Ashley Gurevich",
                "Straight answers from Bay Area loan officer Ashley Gurevich on buying before you sell, bank statement loans, RSU and tech income, rent vs buy, and real client wins.",
                url, "website", SITE + "/headshot.jpg", schemas) + f"""
<header class="blog-hero"><div class="wrap">
  <div class="eyebrow">The Blog</div>
  <h1>Straight answers for your next move.</h1>
  <p>Strategies, real client wins and plain-English guides from a Bay Area loan officer, so you can buy with a plan.</p>
  <div class="cats">{btns}</div>
</div></header>
<div class="wrap"><div class="posts" id="posts">{cards}</div></div>
{FOOTER}
<script>
document.querySelectorAll('.cat').forEach(function(b){{b.onclick=function(){{
 document.querySelectorAll('.cat').forEach(function(x){{x.classList.remove('on')}});b.classList.add('on');
 document.querySelectorAll('#posts .pcard').forEach(function(c){{c.style.display=(b.dataset.c==='all'||c.dataset.c===b.dataset.c)?'':'none'}});
}}}});
</script>
</body>
</html>
"""


def render_feed(posts):
    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{p['url']}</link><guid>{p['url']}</guid><pubDate>{dt.datetime.combine(p['published'], dt.time(8)).strftime('%a, %d %b %Y %H:%M:%S -0700')}</pubDate><description>{esc(p['description'])}</description></item>"
        for p in posts
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Ashley Gurevich Mortgage Blog</title><link>{SITE}/blog/</link><description>Bay Area home buying strategies from loan officer Ashley Gurevich.</description>{items}</channel></rss>\n'


def update_sitemap(posts):
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    s = re.sub(r"\s*<url><loc>https://ashleymariegurevich\.com/blog/[^<]*</loc>.*?</url>", "", s)
    newest = max((p["updated"] for p in posts), default=dt.date.today())
    entries = f'\n  <url><loc>{SITE}/blog/</loc><lastmod>{newest.isoformat()}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
    for p in posts:
        entries += f'\n  <url><loc>{p["url"]}</loc><lastmod>{p["updated"].isoformat()}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
    s = s.replace("\n</urlset>", entries + "\n</urlset>")
    sm.write_text(s)


def update_llms(posts):
    f = ROOT / "llms.txt"
    s = f.read_text()
    s = re.sub(r"\n## Blog\n.*?(?=\n## |\Z)", "", s, flags=re.S).rstrip() + "\n"
    lines = "\n".join(f"- [{p['title']}]({p['url']}): {p.get('short_answer', p['description'])}" for p in posts)
    s += f"\n## Blog\n- [All posts]({SITE}/blog/)\n{lines}\n"
    f.write_text(s)


def main():
    posts = load_posts()
    OUT.mkdir(exist_ok=True)
    for p in posts:
        (OUT / f"{p['slug']}.html").write_text(render_post(p, posts))
    (OUT / "index.html").write_text(render_index(posts))
    (OUT / "feed.xml").write_text(render_feed(posts))
    update_sitemap(posts)
    update_llms(posts)
    print(f"Built {len(posts)} post(s)")


if __name__ == "__main__":
    main()
