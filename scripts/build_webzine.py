"""Build the complete web issue from preserved editorial sources (stdlib only)."""
from pathlib import Path
from html import escape
import collections
import hashlib
import json
import math
import re
import unicodedata
from adoption_components import render_chart

ROOT = Path(__file__).resolve().parents[1]
BASE = '/issues/2026-q4/'
ORIGIN = 'https://aievoq.com'
VERSION = '0.23'
DATE = '2026-10-30'
REVIEW_DATE = 'October 30, 2026'
SOURCE = ROOT/'content'/f'q4-2026-v{VERSION}.md'
raw = SOURCE.read_text()
assets = json.loads((ROOT/'content/web-assets.json').read_text())
panels = json.loads((ROOT/'content'/f'key-statistics-v{VERSION}.json').read_text())['panels']
OUT = ROOT/BASE.strip('/')
OUT.mkdir(parents=True,exist_ok=True)

def slug(text):
    ascii_text = unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',ascii_text).strip('-')

def inline(text):
    """The manuscript uses bold, emphasis, bare URLs and numbered references."""
    pattern = r'https?://[^\s<>]+|\*\*([^*]+)\*\*|\*([^*]+)\*|\[(\d+)\]'
    result=[]; start=0
    for m in re.finditer(pattern,text):
        result.append(escape(text[start:m.start()]))
        if m.group(1): result.append('<strong>'+inline(m.group(1))+'</strong>')
        elif m.group(2): result.append('<em>'+inline(m.group(2))+'</em>')
        elif m.group(3): result.append(f'<a class="reference" href="{BASE}sources/#source-{m.group(3)}" aria-label="Source {m.group(3)}">[{m.group(3)}]</a>')
        else:
            url=m.group().rstrip('.,;')
            result.append(f'<a href="{escape(url,quote=True)}">{escape(url)}</a>'+escape(m.group()[len(url):]))
        start=m.end()
    result.append(escape(text[start:]))
    return ''.join(result)

TITLE_INDEX = {m[1]: i for i, part in enumerate(raw.split('---PAGE---')) if (m := re.search(r'^# (.+)', part, re.M))}
GROUP_BOUNDS = [('Welcome to the AI jungle', 'Where the analogy earns its keep', 'The evolutionary lens'), ('The Ledgerfinch', 'The Proofweaver', 'Meet the species'), ('The quarterly census', 'The metabolic bill', 'The quarterly census'), ('October: the trail so far', 'October 14-16', 'October field notes'), ('October 21', 'October 22 / employment', 'Humans, learning & work'), ('October 22', 'Three seasons ahead', 'Demand & resources'), ('October 25-26', 'The Habitat Engineers', 'Mathematics & the habitat'), ('The Naturalist Was Wrong', 'The three sealed envelopes', 'Expectations & forecasts'), ('New tricks and unexpected turns', 'November-December', 'The field journal'), ('The human cast', 'Paths into the wider world', 'The human cast')]
GROUPS = [(TITLE_INDEX[lo], TITLE_INDEX[hi], name) for lo, hi, name in GROUP_BOUNDS]
def category(index):
    if index == TITLE_INDEX.get('Fork it: the right to branch'): return 'Humans, learning & work'
    if index == TITLE_INDEX.get('October 22 / design'): return 'October field notes'
    for lo,hi,name in GROUPS:
        if lo<=index<=hi: return name
    return 'About this edition'

sections=[]
for index,section in enumerate(raw.split('---PAGE---')):
    title=re.search(r'^# (.+)',section,re.M)
    if not title: continue
    subtitle=re.search(r'^## (.+)',section,re.M)
    title=title.group(1)
    sections.append({'index':index,'title':title,'subtitle':subtitle.group(1) if subtitle else '', 'slug':slug(title),'raw':section.strip(),'category':category(index),'minutes':max(1,math.ceil(len(section.split())/220)), 'source':title.startswith('Sources')})
articles=[a for a in sections if not a['source']]
source_sections=[a for a in sections if a['source']]
refs={}
for a in source_sections:
    for n,body in re.findall(r'^\[(\d+)\] (.+)$',a['raw'],re.M):
        assert n not in refs, f'Duplicate source {n}'
        refs[n]=body
assert set(map(int, refs)) == set(range(1, len(refs)+1))
ARTICLE_COUNT = raw.count('[CONCEPT:')
STATS_COUNT = raw.count('[STATS:')
SOURCE_COUNT = len(refs)

def image(item,alt,cls='',eager=False):
    return f'<img src="{item["src"]}" width="{item["width"]}" height="{item["height"]}" alt="{escape(alt,quote=True)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def figure(kind):
    if kind.startswith('human_'):
        return render_chart(kind)
    if kind=='cast_cover':
        return '<div class="issue-cast">'+''.join(f'<figure><img src="/assets/{k}.webp" width="1122" height="1402" alt="{n}, an imagined AI species" loading="lazy"><figcaption>{n}</figcaption></figure>' for k,n in [('ledgerfinch','The Ledgerfinch'),('relay-octopus','The Relay Octopus'),('proofweaver','The Proofweaver')])+'</div>'
    if kind.startswith('people_pair'):
        pairs=[('sam-altman','dario-amodei'),('demis-hassabis','fei-fei-li'),('jensen-huang','arthur-mensch'),('mark-zuckerberg','elon-musk')]
        html='<div class="people-pair">'
        for key in pairs[int(kind[-1])-1]:
            p=assets['portraits'][key]
            html+=f'<figure>{image(p,"Editorial caricature of "+p["name"]+". Imagined scene.")}<figcaption><h3>{escape(p["name"])}</h3><p class="portrait-title">{escape(p["title"])}</p><p>{inline(p["role_line"])}</p><p>{inline(p["caption"])}</p></figcaption></figure>'
        return html+'</div>'
    item=assets['figures'][kind]
    if item['type']=='portrait':
        name={'ledgerfinch':'The Ledgerfinch','relay_octopus':'The Relay Octopus','proofweaver':'The Proofweaver'}[kind]
        return f'<figure class="species-reading"><img src="{item["src"]}" width="1122" height="1402" alt="{name}, an imagined functional metaphor" loading="lazy"><figcaption><h3>Reading the portrait</h3><dl>'+''.join(f'<div><dt>{escape(a)}</dt><dd>{escape(b)}</dd></div>' for a,b in item['entries'])+'</dl><p>Imagined anatomy / functional metaphor</p></figcaption></figure>'
    title=item['text'].splitlines()[0].strip().title()
    readable_text='\n'.join(re.sub(r'\s+',' ',line).strip() for line in item['text'].splitlines() if line.strip())
    return f'<figure class="issue-diagram"><div class="diagram-scroll" tabindex="0" role="region" aria-label="{escape(title,quote=True)}; scroll to see the full figure">{image(item,title+". Full text follows below.")}</div><figcaption><a href="{item["src"]}">Enlarge figure</a> <span>Scroll across on small screens.</span></figcaption><details><summary>Read the figure’s text <span aria-hidden="true">+</span></summary><pre>{inline(readable_text)}</pre></details></figure>'

def statistics(key):
    d=panels[key]
    return f'<aside class="key-statistics" data-panel="{key}" aria-label="Key statistics"><p class="key-statistics-title">Key statistics</p><p class="key-statistics-scope">{inline(d["scope"])}</p><dl>'+''.join(f'<div><dt>{inline(m["label"])}</dt><dd>{inline(m["value"])}</dd></div>' for m in d['metrics'])+f'</dl><p class="key-statistics-comparison"><strong>Comparison:</strong> {inline(d["comparison"])}</p><p class="key-statistics-limit">{inline(d["limits"])}</p><p class="key-statistics-source"><strong>Source:</strong> {inline(d["source"])} '+', '.join(inline(f'[{n}]') for n in d['refs'])+'</p></aside>'

def render(section,source_mode=False):
    lines=section.strip().splitlines(); out=[];i=0; headings=collections.Counter()
    while i<len(lines):
        line=lines[i].strip();i+=1
        if not line or line.startswith('# '): continue
        if line.startswith('[CONCEPT:'):
            out.append('<div class="concept-intro"><span class="concept-label">AI concept</span><p>'+inline(line[len('[CONCEPT:'):-1].strip())+'</p></div>');continue
        m=re.fullmatch(r'\[STATS:([^\]]+)\]',line)
        if m:out.append(statistics(m[1]));continue
        m=re.fullmatch(r'\[FIGURE:(\w+)\]',line)
        if m:out.append(figure(m[1]));continue
        m=re.fullmatch(r'\[PLATE:([a-z-]+):(\d+)\]',line)
        if m:
            item=assets['plates'][m[1]]
            cls='editorial-plate editorial-plate-small' if int(m[2])<=100 else 'editorial-plate'
            artwork=image(item,item['alt'])
            full_link=''
            if item.get('full_size'):
                href=escape(item['full_size'],quote=True)
                artwork=f'<a href="{href}" aria-label="Open illustration at full size">{artwork}</a>'
                full_link=f' <a href="{href}">View full-size overview</a>'
            out.append(f'<figure class="{cls}">'+artwork+f'<figcaption><span>Imagined scene / Figure {item["number"]:02}</span> {inline(item["caption"])}{full_link}</figcaption></figure>');continue
        if line.startswith('|'):
            block=[line]
            while i<len(lines) and lines[i].strip().startswith('|'):block.append(lines[i].strip());i+=1
            rows=[[cell.strip() for cell in r.strip('|').split('|')] for r in block if not re.match(r'^\|[\s:|\-]+\|$',r)]
            table='<div class="article-table" role="region" tabindex="0" aria-label="Data table; scroll horizontally if needed"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'
            for row in rows[1:]:table+='<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>'
            out.append(table+'</tbody></table></div>');continue
        if line.startswith('##'):
            level=3 if line.startswith('### ') else 2
            text=line[level+1:];key=slug(text);headings[key]+=1
            out.append(f'<h{level} id="{key}-{headings[key]}">{inline(text)}</h{level}>');continue
        block=[line]
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','[FIGURE:','[PLATE:','[CONCEPT:','[STATS:')):
            block.append(lines[i].strip());i+=1
        text=' '.join(block)
        ref=re.match(r'^\[(\d+)\] ',text) if source_mode else None
        if ref:
            out.append(f'<p class="source-entry" id="source-{ref[1]}"><span class="source-number">[{ref[1]}]</span> '+inline(text[ref.end():])+'</p>')
        else:out.append('<p>'+inline(text)+'</p>')
    return '\n'.join(out)

def shell(title,description,path,body,extra_head='',body_class=''):
    if 'class="human-chart"' in body:
        extra_head += '<link rel="stylesheet" href="/statistics/human-adoption.css?v=0.22"><script src="/statistics/human-adoption.js?v=0.22" defer></script>'
    canonical=ORIGIN+path
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — AIEVOQ</title><meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#132432">
<link rel="canonical" href="{canonical}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/webzine.css?v={VERSION}">
<meta property="og:type" content="article"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{ORIGIN}/assets/watering-hole.webp"><meta name="twitter:card" content="summary_large_image">{extra_head}</head>
<body class="{body_class}"><a class="skip-link" href="#main">Skip to content</a><div class="page">
<header class="masthead"><a class="wordmark" href="/" aria-label="AI Evolution Quarterly home"><span class="wordmark-title"><span class="wordmark-ai">AI</span> EVOLUTION</span><span class="wordmark-sub">Quarterly <span aria-hidden="true">/</span> AIEVOQ</span></a><nav aria-label="Main navigation"><a href="{BASE}">Read the issue</a><a href="/statistics/">Statistics</a><a href="{BASE}sources/">Sources</a></nav></header>
<main id="main">{body}</main><footer><div><a class="footer-brand" href="/">AIEVOQ</a><p>AI Evolution Quarterly · Phil Stilwell<br>An illustrated webzine. A print edition may follow.</p></div><p class="footer-motto">Observe. Question. Revisit.</p><p class="copyright">© 2026 Phil Stilwell</p></footer></div></body></html>'''

def write(path,html):
    dest=ROOT/path.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html)

search=[]
for pos,a in enumerate(articles):
    path=BASE+a['slug']+'/'
    headline=a['subtitle'] if a['title'].startswith('October') else a['title']
    article_context=a['category']+(' · '+a['title'] if headline!=a['title'] else '')
    concept=re.search(r'\[CONCEPT: (.+)\]',a['raw'])
    description=concept[1] if concept else a['subtitle']
    header=f'<div class="reading-toolbar"><a href="{BASE}">← Contents</a><span>Issue 01 · Q4 2026 · Draft {VERSION}</span></div><article class="reading-article"><header class="article-heading"><p class="eyebrow">{escape(article_context)} <span class="slash">/</span> {a["minutes"]} min read</p><h1>{escape(headline)}</h1><p class="edition-date">By Phil Stilwell · Reviewed {REVIEW_DATE} · Q4 in progress</p></header>'
    body_source=a['raw'].replace('## '+a['subtitle']+'\n','',1) if headline!=a['title'] else a['raw']
    body=render(body_source)
    numbers=sorted(set(re.findall(r'\[(\d+)\]',a['raw']))|{str(n) for k in re.findall(r'\[STATS:([^\]]+)\]',a['raw']) for n in panels[k]['refs']},key=int)
    source_note=''
    if numbers:
        source_note='<aside class="article-sources"><h2>Sources for this article</h2><p>'+', '.join(inline(f'[{n}]') for n in numbers)+f'</p><p>Open a numbered reference for its full citation, date and limitations in the <a href="{BASE}sources/">source ledger</a>.</p></aside>'
    previous=articles[pos-1] if pos else None
    nxt=articles[pos+1] if pos<len(articles)-1 else None
    nav='<nav class="article-pagination" aria-label="Continue reading">'
    nav+=f'<a href="{BASE+previous["slug"]+"/" if previous else BASE}"><span>← Previous</span><strong>{escape(previous["title"]) if previous else "Issue contents"}</strong></a>'
    nav+=f'<a href="{BASE+nxt["slug"]+"/" if nxt else BASE+"sources/"}"><span>Next →</span><strong>{escape(nxt["title"]) if nxt else "Sources and figure notes"}</strong></a></nav>'
    data={'@context':'https://schema.org','@type':'Article','headline':headline,'description':description,'author':{'@type':'Person','name':'Phil Stilwell'},'dateModified':DATE,'isPartOf':{'@type':'PublicationIssue','name':'AI Evolution Quarterly — Q4 2026','issueNumber':'1'},'mainEntityOfPage':ORIGIN+path}
    write(path,shell(headline,description,path,header+body+source_note+'</article>'+nav, '<script type="application/ld+json">'+json.dumps(data).replace('<','\\u003c')+'</script>','article-page'))
    search.append({'slug':a['slug'],'title':a['title'],'subtitle':a['subtitle'],'category':a['category'],'text':re.sub(r'\[(?:CONCEPT|STATS|FIGURE|PLATE):',' ',a['raw'])})

# Source sections stay together, with unique numbered destinations.
source_toc='<nav class="source-toc" aria-label="Source sections">'+''.join(f'<a href="#source-section-{a["index"]}">{escape(a["title"])}</a>' for a in source_sections)+'</nav>'
source_html=f'<div class="reading-toolbar"><a href="{BASE}">← Contents</a><span>Issue 01 · Draft {VERSION}</span></div><header class="sources-heading"><p class="eyebrow">The evidence trail</p><h1>Sources &amp; figure notes</h1><p>All {SOURCE_COUNT} references, with the original research notes, attribution and limits. Selected evidence reviewed through {REVIEW_DATE}.</p></header>'+source_toc+'<div class="reading-article source-ledger">'
for a in source_sections:
    source_html+=f'<section id="source-section-{a["index"]}" class="source-section"><h2 class="source-section-title">{escape(a["title"])}</h2>'+render(a['raw'],True)+'</section>'
source_html+=f'</div><p class="end-link"><a href="{BASE}">Return to the complete issue ↑</a></p>'
write(BASE+'sources/',shell('Sources & figure notes',f'All {SOURCE_COUNT} sources and research notes for the first issue of AI Evolution Quarterly.',BASE+'sources/',source_html))

hero=f'''<section class="issue-cover"><div><p class="eyebrow">Volume 1 / Issue 1 / October–December 2026</p><h1>The struggle<br>for a <em>niche.</em></h1><p class="issue-deck">Biological Metaphors that Reflect the Discoveries and Complexities within This Quarter's AI Ecosystem</p><p class="issue-description">A complete, evolving web edition. Follow the numbers, meet the creatures, and explore the changing relationship between AI and its human habitat.</p><div class="issue-actions"><a class="button" href="{BASE}welcome-to-the-ai-jungle/">Start reading <span aria-hidden="true">→</span></a><a href="#contents">Browse all articles ↓</a></div><p class="issue-version">Draft {VERSION} · Reviewed {REVIEW_DATE}<br>Q4 remains open. November and December reporting will follow.</p></div><figure><a href="{BASE}ai-evolution-quarterly/">{image(assets['cover'],'AI Evolution Quarterly, issue 01: an illustrated AI ecosystem on warm ivory paper.',eager=True)}</a><figcaption>The first issue · Phil Stilwell</figcaption></figure></section>
<div class="issue-facts"><span><strong>{ARTICLE_COUNT}</strong> articles &amp; field notes</span><span><strong>{STATS_COUNT}</strong> Key statistics panels</span><span><strong>{SOURCE_COUNT}</strong> sources</span><a href="/statistics/">Interactive census &amp; data →</a></div>'''
contents='''<section id="contents" class="issue-contents"><div class="contents-heading"><div><p class="eyebrow">Explore the complete issue</p><h2>A trail through the ecosystem.</h2></div><p>Read in order, or follow a question.</p></div><form class="contents-tools" id="contents-tools" role="search" hidden><div><label for="article-search">Find an article, concept or name</label><input id="article-search" type="search" placeholder="Try employment, mathematics, learning…" autocomplete="off"></div><div><label for="department">Department</label><select id="department"><option value="">All departments</option>'''+''.join(f'<option>{escape(name)}</option>' for _,_,name in GROUPS)+'''<option>About this edition</option></select></div><button type="reset">Clear</button></form><p id="search-status" role="status" hidden></p><p id="no-results" hidden>No matching articles. Try a broader term or choose all departments.</p>'''
for _,_,name in GROUPS+[(1,1,'About this edition')]:
    group=[a for a in articles if a['category']==name]
    contents+=f'<section class="contents-group" aria-labelledby="group-{slug(name)}"><h3 id="group-{slug(name)}">{escape(name)}</h3><ol>'
    for a in group:
        label=a['subtitle'] if a['title'].startswith('October') else a['title']
        sub=a['title'] if a['title'].startswith('October') else a['subtitle']
        contents+=f'<li class="contents-entry" data-slug="{a["slug"]}" data-category="{escape(name,quote=True)}"><a href="{BASE+a["slug"]}/"><span class="contents-number">{a["index"]:02}</span><span><strong>{escape(label)}</strong><small>{escape(sub)}</small></span><span class="reading-time">{a["minutes"]} min <span aria-hidden="true">↗</span></span></a></li>'
    contents+='</ol></section>'
contents+=f'</section><aside class="issue-evidence"><div><p class="eyebrow">Keep the evidence close</p><h2>An inspectable evidence trail.</h2><p>Find all {SOURCE_COUNT} citations and the complete research notes, including the limits of each comparison and the provenance of the illustrations.</p><a href="{BASE}sources/">Open the source ledger →</a></div><div><h3>Web first. Print later.</h3><p>This developing issue is available to read in full online. Its dated manuscript, original artwork and statistical record are preserved for a possible print edition.</p><p><a href="{BASE}our-continuing-workshop/">Editorial workshop &amp; version notes →</a></p></div></aside>'
write(BASE,shell('Issue 01 — The struggle for a niche',f'Read the full illustrated Q4 2026 webzine: {ARTICLE_COUNT} articles and field notes, {STATS_COUNT} Key statistics panels and {SOURCE_COUNT} sources.',BASE,hero+contents,'<script src="/webzine.js" defer></script>','issue-page'))
(OUT/'search-index.json').write_text(json.dumps(search,ensure_ascii=False)+'\n')

# Explicit, reproducible inventory used by the migration audit.
manifest={'version':VERSION,'reviewed_on':DATE,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_sections':len(sections),'editorial_articles':sum('[CONCEPT:' in a['raw'] for a in articles),'article_pages':len(articles),'concept_panels':raw.count('[CONCEPT:'),'statistic_panels':raw.count('[STATS:'),'source_count':len(refs),'source_sections_count':len(source_sections),'plate_placements':raw.count('[PLATE:'),'figure_placements':raw.count('[FIGURE:'),'pages':[{'source_index':a['index'],'title':a['title'],'path':BASE+a['slug']+'/','category':a['category']} for a in articles]}
(ROOT/'content/migration-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
urls=['/','/statistics/',BASE,BASE+'sources/']+[a['path'] for a in manifest['pages']]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{ORIGIN+url}</loc><lastmod>{DATE}</lastmod></url>\n' for url in urls)+'</urlset>\n')
print(f'Built {len(articles)} reading pages, contents and source ledger. {manifest["concept_panels"]} concept panels; {manifest["statistic_panels"]} statistic panels; {len(refs)} sources.')
