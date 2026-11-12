#!/usr/bin/env python3
"""Builds the static site from content.py.  Run from the repo root:  python3 _src/build.py"""
import html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from content import SITE, ABOUT, CV, PROJECTS, SECTIONS

ROOT = Path(__file__).resolve().parent.parent
E = html.escape


def img_size(name):
    try:
        from PIL import Image
        with Image.open(ROOT / 'img' / f'{name}.jpg') as im:
            return im.size
    except Exception:
        return (1600, 1000)


def year(p):
    for _, v in p.get('meta', []):
        m = re.search(r'(20\d\d)', v)
        if m:
            return m.group(1)
    return ''


def course(p):
    v = p['meta'][0][1] if p.get('meta') else ''
    m = re.match(r'([A-Za-z]+ [IVX]+)', v)
    return m.group(1).lower() if m else ''


def page(title, body, depth=0, desc=None, cls=''):
    up = '../' * depth
    d = E(desc or SITE['tagline'])
    nav = [('work', f'{up}index.html'), ('play', f'{up}index.html#play'), ('about', f'{up}about.html'), ('pdf', f'{up}book/')]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{d}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{d}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect x='2' y='2' width='12' height='12' fill='none' stroke='%23ff6026' stroke-width='2'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
</head>
<body class="{cls}">
<a class="logo" href="{up}index.html" aria-label="Home"><span data-scatter>kelsey wang</span></a>
<nav class="tags" aria-label="Main">{''.join(f'<a href="{u}" style="--r:{r}deg">{n}</a>' for (n, u), r in zip(nav, [-4, 3, -2, 5]))}</nav>
{body}
<footer><span>{E(SITE['name'].lower())} · new york</span><span>{' · '.join(f'<a href="{(up + u) if not u.startswith("http") else u}">{E(n.lower())}</a>' for n, u in SITE['links'])}</span></footer>
<div class="lb" id="lb" hidden><img alt=""><button aria-label="Close">×</button></div>
<script src="{up}fun.js"></script>
</body>
</html>
'''


def build_index():
    items = []
    for i, p in enumerate(PROJECTS):
        imgs = [p['cover']] if p.get('cover') else []
        for _, _, im in p.get('sections', []):
            imgs += [x for x in im if x not in imgs]
        items.append({
            'n': i + 1, 'title': p['title'], 'section': p['section'], 'summary': p['summary'],
            'href': p.get('external') or f"work/{p['slug']}.html", 'ext': bool(p.get('external')),
            'cover': p.get('cover'), 'imgs': imgs[:4], 'year': year(p), 'course': course(p),
            'size': list(img_size(p['cover'])) if p.get('cover') else [1200, 900],
        })
    rows = ''.join(
        f'<a class="row" href="{it["href"]}"{" target=_blank rel=noopener" if it["ext"] else ""} data-img="{("img/" + it["cover"] + ".jpg") if it["cover"] else ""}">'
        f'<span class="n">{it["n"]:02d}</span><span class="t">{E(it["title"].lower())}{" ↗" if it["ext"] else ""}</span>'
        f'<span class="c">{E(it["course"])}</span><span class="s">{E(dict(SECTIONS)[it["section"]].split(",")[0].lower())}</span><span class="y">{it["year"]}</span></a>'
        for it in items)
    body = f'''<main class="home">
<section class="hero">
  <h1 class="big" data-scatter data-explode>kelsey wang</h1>
  <p class="lede">{E(SITE['tagline'])}</p>
</section>
<div class="modes" role="tablist">
  <button data-mode="pile" class="on">pile</button><button data-mode="axon">axon</button><button data-mode="index">index</button>
  <span class="hint" id="hint">drag, throw, double-click to open</span>
</div>
<section class="stage" id="stage">
  <div class="view pile on" id="pile"></div>
  <div class="view axon" id="axon"><div class="iso" id="iso"></div></div>
  <div class="view index" id="index"><div class="rows">{rows}</div><img class="peek" id="peek" alt=""></div>
</section>
<section class="play" id="play">
  <h2 class="label">games + tools <span>({sum(1 for it in items if it["section"] == "play")})</span></h2>
  <div class="blocks">{''.join(f'<a class="block" href="{it["href"]}" target="_blank" rel="noopener" style="--r:{[-3, 2, -1.5, 3.5][k % 4]}deg"><div class="ph"><img src="img/{it["cover"]}.jpg" alt="" loading="lazy"></div><b>{E(it["title"].lower())} ↗</b><small>{E(it["summary"])}</small></a>' for k, it in enumerate([x for x in items if x["section"] == "play"]))}</div>
</section>
</main>
<script>window.WORKS = {json.dumps(items)};</script>
<script src="assets/matter.min.js"></script>'''
    (ROOT / 'index.html').write_text(page('Kelsey Wang', body, 0, cls='home'))


def figure(name, up='../', k=0):
    w, h = img_size(name)
    wide = ' wide' if w / h > 1.25 else ''
    return f'<figure class="f{wide}" style="--d:{k * 70}ms"><img src="{up}img/{name}.jpg" width="{w}" height="{h}" alt="" loading="lazy"></figure>'


def build_project(p, i, seq):
    meta = ''.join(f'<dt>{E(k.lower())}</dt><dd>{E(v)}</dd>' for k, v in p['meta'])
    links = ''.join(f'<a class="cta" href="{u}" target="_blank" rel="noopener">{E(n.lower())} ↗</a>' for n, u in p.get('links', []))
    body = ''.join(f'<p>{E(t)}</p>' for t in p['body'])
    secs = []
    for title, paras, imgs in p.get('sections', []):
        txt = ''.join(f'<p>{E(t)}</p>' for t in paras)
        figs = ''.join(figure(n, k=k) for k, n in enumerate(imgs))
        head = f'<h2 class="label">{E(title.lower())}</h2>' if title else ''
        secs.append(f'<section class="chapter">{"<div class=txt>" + head + txt + "</div>" if (head or txt) else ""}<div class="figs">{figs}</div></section>')
    prev, nxt = seq[i - 1], seq[(i + 1) % len(seq)]
    hero = f'<div class="hero-img"><img src="../img/{p["cover"]}.jpg" alt="{E(p["title"])}"></div>' if p.get('cover') else ''
    html_ = f'''<main class="project">
<div class="phead">
  <h1 class="ptitle" data-scatter data-explode>{E(p["title"].lower())}</h1>
  <div class="cols"><dl>{meta}</dl><div class="body"><p class="sum">{E(p["summary"])}</p>{body}{('<div class="ctas">' + links + '</div>') if links else ''}</div></div>
</div>
{hero}
{''.join(secs)}
<nav class="pn"><a href="{prev["slug"]}.html">← {E(prev["title"].lower())}</a><a href="../index.html">index</a><a href="{nxt["slug"]}.html">{E(nxt["title"].lower())} →</a></nav>
</main>'''
    (ROOT / 'work' / f"{p['slug']}.html").write_text(page(f"{p['title']} · Kelsey Wang", html_, 1, p['summary'], 'proj'))


def build_about():
    cv = ''.join(f'<h2 class="label">{E(h.lower())}</h2><ul>' + ''.join(f'<li><span>{E(y)}</span>{E(t)}</li>' for y, t in rows) + '</ul>' for h, rows in CV)
    first, rest = ABOUT[0], ABOUT[1:]
    body = f'''<main class="about">
<p class="intro" data-scatter>{E(first)}</p>
<div class="cols"><div></div><div class="body">{''.join(f"<p>{E(t)}</p>" for t in rest)}{cv}
<h2 class="label">elsewhere</h2><ul>{''.join(f'<li><span></span><a href="{u}">{E(n.lower())}</a></li>' for n, u in SITE["links"])}</ul></div></div></main>'''
    (ROOT / 'about.html').write_text(page('About · Kelsey Wang', body, 0, cls='aboutp'))


if __name__ == '__main__':
    (ROOT / 'work').mkdir(exist_ok=True)
    build_index()
    seq = [p for p in PROJECTS if not p.get('external')]
    for i, p in enumerate(seq):
        build_project(p, i, seq)
    build_about()
    print('built', len(seq), 'project pages')
