#!/usr/bin/env python3
"""Regenerate /tags/ pages in the Silicon Dark design system."""
import os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POST = {
    "url": "https://LoveGPTAI.github.io/blog/2026-06-21-ai-eda-foundry-flow-silicon-feedback/",
    "title": "從 RFIC 工程師到 AI-native EDA Workflow Architect：我貫穿半導體設計、量產與工具鏈的全端主線",
    "date": "2026-06-21",
    "read": "5 min read",
    "summary": "16 年來換過 5 個職稱、4 家公司，但拆開每一段轉換的接點，其實一直在貫穿半導體從電路設計、量產測試、良率診斷到 EDA 工具鏈的全端業務。",
    "tags": [("AI", "ai"), ("EDA", "eda"), ("Career", "career"), ("Foundry Flow", "foundry-flow")],
}

# slug -> (display name, has_post)
TAGS = {
    "ai": ("AI", True),
    "eda": ("EDA", True),
    "career": ("Career", True),
    "foundry-flow": ("Foundry Flow", True),
    "vibe-coding": ("Vibe Coding", False),
    "personal": ("Personal", False),
    "半導體": ("半導體", False),
    "雲端": ("雲端", False),
    "前端工程": ("前端工程", False),
    "components": ("Components", False),
    "css": ("CSS", False),
    "design": ("Design", False),
    "gpu": ("GPU", False),
    "hugo": ("Hugo", False),
    "rwd": ("RWD", False),
    "ux": ("UX", False),
}

HEAD = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} | Jarvis Wang's vibe 筆記</title>
  <link rel="icon" href="https://LoveGPTAI.github.io/images/logo.png" type="image/png">
  <meta name="theme-color" content="#060a11">
  <meta name="description" content="{desc}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <meta property="og:site_name" content="Jarvis Wang's vibe 筆記">
  <meta property="og:title" content="{title} | Jarvis Wang's vibe 筆記">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="/images/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/site.css">
</head>
<body>
  <div class="container">
    <div class="frame">

      <div class="chrome">
        <div class="layers" aria-hidden="true">
          <span class="layer-chip m1"></span>
          <span class="layer-chip via"></span>
          <span class="layer-chip poly"></span>
        </div>
        <span class="chrome-title"><b>jarvis_wang.gds</b> — layout viewer — cell: {cell}</span>
        <nav class="chrome-nav">
          <a href="https://LoveGPTAI.github.io/">首頁</a>
          <a href="https://LoveGPTAI.github.io/about">關於</a>
          <a href="https://LoveGPTAI.github.io/blog" class="active">部落格</a>
        </nav>
      </div>
      <div class="ruler" aria-hidden="true"></div>

      <main>
        <div class="article-wrap">
"""

FOOT = """
        </div>
      </main>

      <footer class="statusbar">
        <div class="status-group">
          <span class="status-item">DRC: <b>0 errors</b></span>
          <span class="status-item">LVS: <b>clean</b></span>
          <span class="status-item"><span class="amber">grid 0.001µ</span></span>
        </div>
        <div class="status-group">
          <span class="status-item">&copy; <span id="y"></span> Jarvis Wang</span>
          <span class="status-item">25.03°N 121.56°E · TAIPEI</span>
        </div>
      </footer>

    </div>
  </div>
  <script>document.getElementById('y').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

def post_item():
    tags = "\n                    ".join(
        f'<a class="tag" href="https://LoveGPTAI.github.io/tags/{urllib.parse.quote(slug)}/">#{name}</a>'
        for name, slug in POST["tags"]
    )
    return f"""              <div class="post-item">
                <h2 class="post-title-h">
                  <a href="{POST['url']}">{POST['title']}</a>
                </h2>
                <div class="post-meta">{POST['date']} · {POST['read']}</div>
                <p class="post-summary">{POST['summary']}</p>
                <div class="post-foot">
                  <div class="tag-list">
                    {tags}
                  </div>
                  <a class="read-more" href="{POST['url']}">Read more</a>
                </div>
              </div>"""

def tag_page(slug, name, has_post):
    canonical = f"https://LoveGPTAI.github.io/tags/{urllib.parse.quote(slug)}/"
    count = 1 if has_post else 0
    body_post = post_item() if has_post else \
        '              <p style="color:var(--faint);font-family:var(--mono);font-size:12px;">// 尚無文章 — net is floating.</p>'
    body = f"""
          <a class="back-link" href="https://LoveGPTAI.github.io/tags/">所有標籤</a>

          <h1 class="tag-heading">{name}</h1>
          <div class="tag-count">{count} post{"s" if count != 1 else ""} routed to this net</div>

          <div class="card">
            <p class="card-label"><span class="idx">[01]</span> Posts</p>
{body_post}
          </div>
"""
    return (HEAD.format(title=name, desc=f"標籤：{name} 的文章列表",
                        canonical=canonical, cell=f"TAGS / {name.upper()}")
            + body + FOOT)

def tags_index():
    canonical = "https://LoveGPTAI.github.io/tags/"
    # real tags first, then dormant ones
    cloud = []
    for slug, (name, has_post) in sorted(TAGS.items(), key=lambda kv: (not kv[1][1], kv[1][0].lower())):
        cnt = 1 if has_post else 0
        cloud.append(
            f'                <a class="tag" href="https://LoveGPTAI.github.io/tags/{urllib.parse.quote(slug)}/">#{name}<span class="cnt">{cnt}</span></a>'
        )
    cloud_html = "\n".join(cloud)
    body = f"""
          <a class="back-link" href="https://LoveGPTAI.github.io/blog">所有文章</a>

          <h1 class="tag-heading">Tags</h1>
          <div class="tag-count">{len(TAGS)} nets in this design</div>

          <div class="card">
            <p class="card-label"><span class="idx">[01]</span> Net List</p>
            <div class="tag-cloud">
{cloud_html}
            </div>
          </div>
"""
    return HEAD.format(title="Tags", desc="所有文章標籤", canonical=canonical, cell="TAGS") + body + FOOT

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(path, ROOT))

def redirect(url):
    return (f'<!doctype html><html lang="zh-Hant"><head><title>{url}</title>'
            f'<link rel="canonical" href="{url}"><meta name="robots" content="noindex">'
            f'<meta charset="utf-8"><meta http-equiv="refresh" content="0; url={url}"></head></html>\n')

for slug, (name, has_post) in TAGS.items():
    html = tag_page(slug, name, has_post)
    write(os.path.join(ROOT, "tags", slug, "index.html"), html)
    # page/1 → redirect to the tag page
    write(os.path.join(ROOT, "tags", slug, "page", "1", "index.html"),
          redirect(f"https://LoveGPTAI.github.io/tags/{urllib.parse.quote(slug)}/"))

write(os.path.join(ROOT, "tags", "index.html"), tags_index())
for n in ("1", "2"):
    p = os.path.join(ROOT, "tags", "page", n, "index.html")
    if os.path.exists(p):
        write(p, redirect("https://LoveGPTAI.github.io/tags/"))
