#!/usr/bin/env python3
"""Builds the static site from content.py.  Run from the repo root:  python3 _src/build.py"""
import html, os, sys
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

def page(title, body, depth=0, desc=None, cls=''):
    up = '../' * depth
    d = E(desc or SITE['tagline'])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{d}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{d}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
</head>
<body class="{cls}">
<header class="top">
  <a class="name" href="{up}index.html">{E(SITE['name'])}</a>
  <nav><a href="{up}index.html#studio">Work</a><a href="{up}index.html#play">Play</a><a href="{up}about.html">About</a><a href="{up}book/">PDF</a></nav>
</header>
{body}
<footer><span>{E(SITE['name'])} · New York</span><span>{' · '.join(f'<a href="{(up + u) if not u.startswith("http") else u}">{E(n)}</a>' for n, u in SITE['links'])}</span></footer>
<div class="lb" id="lb" hidden><img alt=""><button aria-label="Close">×</button></div>
<script>
const lb=document.getElementById('lb'),li=lb.querySelector('img');
document.querySelectorAll('figure img').forEach(i=>i.addEventListener('click',()=>{{li.src=i.src;lb.hidden=false;}}));
lb.addEventListener('click',()=>lb.hidden=true);
addEventListener('keydown',e=>{{if(e.key==='Escape')lb.hidden=true;}});
</script>
</body>
</html>
'''

def tile(p, up=''):
    href = p.get('external') or f"{up}work/{p['slug']}.html"
    ext = ' target="_blank" rel="noopener"' if p.get('external') else ''
    cover = (f'<div class="ph"><img src="{up}img/{p["cover"]}.jpg" alt="{E(p["title"])}" loading="lazy"></div>' if p.get('cover')
             else f'<div class="ph type"><span>{E(p["title"])}</span></div>')
    meta = p['meta'][0][1] if p.get('meta') else ''
    arrow = ' ↗' if p.get('external') else ''
    return f'''<a class="tile" href="{href}"{ext}>{cover}<div class="cap"><h3>{E(p["title"])}{arrow}</h3><p class="m">{E(meta)}</p><p>{E(p["summary"])}</p></div></a>'''

def figure(name, up='../'):
    w, h = img_size(name)
    wide = ' wide' if w / h > 1.25 else (' tall' if w / h < 0.8 else '')
    return f'<figure class="f{wide}"><img src="{up}img/{name}.jpg" width="{w}" height="{h}" alt="" loading="lazy"></figure>'

def build_index():
    parts = [f'<main class="index"><section class="intro"><p class="lede">{E(SITE["tagline"])}</p></section>']
    for key, label in SECTIONS:
        items = [p for p in PROJECTS if p['section'] == key]
        parts.append(f'<section class="group" id="{key}"><h2><span>{E(label)}</span><span class="ct">{len(items):02d}</span></h2><div class="grid g-{key}">')
        parts += [tile(p) for p in items]
        parts.append('</div></section>')
    parts.append('</main>')
    (ROOT / 'index.html').write_text(page('Kelsey Wang', '\n'.join(parts), 0, cls='home'))

def build_project(p, i, seq):
    meta = ''.join(f'<dt>{E(k)}</dt><dd>{E(v)}</dd>' for k, v in p['meta'])
    links = ''.join(f'<a class="cta" href="{u}" target="_blank" rel="noopener">{E(n)} ↗</a>' for n, u in p.get('links', []))
    body = ''.join(f'<p>{E(t)}</p>' for t in p['body'])
    secs = []
    for title, paras, imgs in p.get('sections', []):
        txt = ''.join(f'<p>{E(t)}</p>' for t in paras)
        figs = ''.join(figure(n) for n in imgs)
        head = f'<h2>{E(title)}</h2>' if title else ''
        secs.append(f'<section class="chapter">{"<div class=txt>" + head + txt + "</div>" if (head or txt) else ""}<div class="figs">{figs}</div></section>')
    prev, nxt = seq[i - 1], seq[(i + 1) % len(seq)]
    hero = f'<div class="hero"><img src="../img/{p["cover"]}.jpg" alt="{E(p["title"])}"></div>' if p.get('cover') else ''
    html_ = f'''<main class="project">
<div class="phead"><div class="side"><h1>{E(p["title"])}</h1><dl>{meta}</dl>{links}</div>
<div class="body"><p class="sum">{E(p["summary"])}</p>{body}</div></div>
{hero}
{''.join(secs)}
<nav class="pn"><a href="{prev["slug"]}.html">← {E(prev["title"])}</a><a href="../index.html">INDEX</a><a href="{nxt["slug"]}.html">{E(nxt["title"])} →</a></nav>
</main>'''
    (ROOT / 'work' / f"{p['slug']}.html").write_text(page(f"{p['title']} · Kelsey Wang", html_, 1, p['summary'], 'proj'))

def build_about():
    cv = ''.join(f'<h2>{E(h)}</h2><ul>' + ''.join(f'<li><span>{E(y)}</span>{E(t)}</li>' for y, t in rows) + '</ul>' for h, rows in CV)
    body = f'''<main class="about"><div class="side"><h1>ABOUT</h1></div><div class="body">{''.join(f"<p>{E(t)}</p>" for t in ABOUT)}{cv}
    <h2>Elsewhere</h2><ul>{''.join(f'<li><span></span><a href="{u}">{E(n)}</a></li>' for n, u in SITE["links"])}</ul></div></main>'''
    (ROOT / 'about.html').write_text(page('About · Kelsey Wang', body, 0))

if __name__ == '__main__':
    (ROOT / 'work').mkdir(exist_ok=True)
    build_index()
    seq = [p for p in PROJECTS if not p.get('external')]
    for i, p in enumerate(seq):
        build_project(p, i, seq)
    build_about()
    print('built', len(seq), 'project pages')
