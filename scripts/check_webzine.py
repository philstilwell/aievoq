"""Audit the migration for lost manuscript text, missing assets and broken links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import collections
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
BASE='/issues/2026-q4/'
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.text=[];self.tags=[];self.images=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append((tag,attrs))
        if 'id' in attrs:self.ids.append(attrs['id'])
        for key in ['href','src']:
            if key in attrs:self.links.append(attrs[key])
        if tag=='img':self.images.append(attrs)
    def handle_data(self,text):self.text.append(text)

def compact(text):return re.sub(r'[^\w]','',text).lower()

manifest=json.loads((ROOT/'content/migration-manifest.json').read_text())
source=ROOT/'content'/f"q4-2026-v{manifest['version']}.md"
assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['source_sha256']
sections=source.read_text().split('---PAGE---')
docs={p:Document(p.read_text()) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
failures=[];local_links=0
for path,doc in docs.items():
    if len(doc.ids)!=len(set(doc.ids)):failures.append(f'Duplicate IDs: {path.relative_to(ROOT)}')
    for image in doc.images:
        if not image.get('alt'):failures.append(f'Missing image description: {path}')
    for link in doc.links:
        url=urlsplit(urljoin('https://aievoq.com/'+str(path.relative_to(ROOT)),link))
        if url.netloc!='aievoq.com' or url.scheme not in ['https','http']:continue
        target=ROOT/unquote(url.path).lstrip('/')
        if target.is_dir():target=target/'index.html'
        local_links+=1
        if not target.is_file():failures.append(f'Missing {link} in {path.relative_to(ROOT)}')
        elif url.fragment and target.suffix=='.html' and unquote(url.fragment) not in docs[target].ids:
            failures.append(f'Missing anchor {link} in {path.relative_to(ROOT)}')

sources=docs[ROOT/(BASE.strip('/'))/'sources/index.html']
source_text=compact(' '.join(sources.text))
panels=json.loads((ROOT/'content'/f"key-statistics-v{manifest['version']}.json").read_text())['panels']
checked_lines=0
for i,section in enumerate(sections):
    if i==0:continue
    if re.search(r'^# Sources',section,re.M):rendered=source_text
    else:
        entry=next(x for x in manifest['pages'] if x['source_index']==i)
        rendered=compact(' '.join(docs[ROOT/entry['path'].strip('/')/'index.html'].text))
    for line in section.splitlines():
        line=line.strip()
        if not line:continue
        if re.match(r'\[(FIGURE|PLATE):',line):continue
        if re.match(r'^\|[\s:|\-]+\|$',line):continue
        stat=re.fullmatch(r'\[STATS:([^\]]+)\]',line)
        if stat:
            d=panels[stat[1]]
            texts=[d[k] for k in ['scope','comparison','limits','source']]+[v for m in d['metrics'] for v in m.values()]
        elif line.startswith('[CONCEPT:'):texts=[line[len('[CONCEPT:'):-1]]
        elif line.startswith('|'):texts=line.strip('|').split('|')
        else:texts=[re.sub(r'^#+ ','',line)]
        for text in texts:
            checked_lines+=1
            if compact(text) not in rendered:failures.append(f'Lost text in section {i}: {text[:100]}')

article_docs=[docs[ROOT/p['path'].strip('/')/'index.html'] for p in manifest['pages']]
tags=[t for d in article_docs for t in d.tags]
concepts=sum('concept-intro' in a.get('class','').split() for t,a in tags)
stats=sum('key-statistics' in a.get('class','').split() for t,a in tags)
plates=sum('editorial-plate' in a.get('class','').split() for t,a in tags)
assert (concepts,stats,plates)==(manifest['concept_panels'],manifest['statistic_panels'],manifest['plate_placements']),(concepts,stats,plates)
assert {f'source-{i}' for i in range(1,manifest['source_count']+1)} <= set(sources.ids)
summary={'passed':not failures,'html_pages':len(docs),'checked_manuscript_lines_and_cells':checked_lines,'local_links_and_assets_checked':local_links,'concept_panels':concepts,'key_statistics_panels':stats,'illustration_placements':plates,'numbered_sources':manifest['source_count'],'failures':failures}
print(json.dumps(summary,indent=2))
if failures:raise SystemExit(1)
