"""Refresh the human-adoption section without touching existing census data."""
from pathlib import Path
from html import escape
import json,re
from adoption_components import render_chart, DATA, DATA_URL

ROOT=Path(__file__).resolve().parents[1]
panels=json.loads((ROOT/'content/key-statistics-v0.22.json').read_text())['panels']

def stat(key):
    d=panels[key]
    refs=' · '.join(f'<a href="/issues/2026-q4/sources/#source-{n}">Source {n}</a>' for n in d['refs'])
    return '<aside class="key-statistics" data-panel="'+key+'" aria-label="Key statistics"><p class="key-statistics-title">Key statistics</p><p class="key-statistics-scope">'+escape(d['scope'])+'</p><dl>'+''.join('<div><dt>'+escape(m['label'])+'</dt><dd>'+escape(m['value'])+'</dd></div>' for m in d['metrics'])+'</dl><p class="key-statistics-comparison"><strong>Comparison:</strong> '+escape(d['comparison'])+'</p><p class="key-statistics-limit">'+escape(d['limits'])+'</p><p class="key-statistics-source"><strong>Source:</strong> '+escape(d['source'])+' '+refs+'</p></aside>'

section='''<!-- human-adoption:start -->
<section class="stat-section" id="human-adoption" aria-labelledby="human-adoption-title">
<div class="stat-heading"><div><p class="eyebrow">Human adoption / reviewed 30 October 2026</p><h2 id="human-adoption-title">People in the changing habitat</h2></div><span class="cadence">Three recurring panels</span></div>
<div class="concept-intro"><span class="concept-label">AI concept</span><p>AI adoption describes whether people use AI, how often they return and what they gain from it. Frequency, reasons for non-use and perceived benefits measure different things. Keeping these records separate shows how use develops without treating enthusiasm as proof of better work.</p></div>
<p class="section-intro">Track the regular visitors, the barriers at the forest edge and what the partnership delivers. These surveys do not assign people to the nine editorial categories in <a href="/issues/2026-q4/the-adoption-gradient/">The adoption gradient</a>.</p>
<p class="data-note">Observation dates appear on every chart. This October 30 snapshot contains earlier surveys and one report published in Q4; it is not a measure of completed Q4 adoption.</p>
<nav class="section-jumps" aria-label="Human-adoption panels"><a href="#use-frequency">Frequency</a><a href="#adoption-barriers">Barriers</a><a href="#adoption-benefits">Benefits</a></nav>
'''
cadence_notes={
    'use-frequency':'Reviewed quarterly. Each survey keeps its own population and questions; matching observations show changes in percentage points.',
    'adoption-barriers':'Updated when a comparable survey appears. Earlier observations remain visible until a matching new reading is available.',
    'adoption-benefits':'Updated as new evidence appears. Reported experiences and measured outcomes remain separate, with observation and publication dates shown.'
}
for item in DATA['recurring_panels']:
    section+=f'<section class="human-recurring-panel" id="{item["id"]}" aria-labelledby="{item["id"]}-title"><p class="eyebrow">{escape(item["ambiance"])}</p><h3 id="{item["id"]}-title">{escape(item["title"])}</h3><p class="human-cadence">{escape(cadence_notes[item["id"]])}</p>'
    panel={'use-frequency':'human-frequency','adoption-barriers':'human-barriers','adoption-benefits':'human-benefits'}[item['id']]
    section+=stat(panel)
    section+=''.join(render_chart(kind) for kind in item['chart_ids'])
    if item['id']=='adoption-benefits':
        section+='<h4>Measured outcomes: separate studies, separate units</h4><p>The percentage of users reporting a benefit cannot be compared directly with a measured productivity effect. These two earlier studies show why tasks, methods and checking matter.</p>'+stat('adoption-responses')+'<p class="data-note">Neither study establishes a typical 100-times multiplier. See the <a href="/issues/2026-q4/the-adoption-gradient/#the-100-times-field-test-1">100-times field test</a> for the questions an extraordinary claim should answer.</p>'
    section+='</section>'
section+=f'<p class="data-note"><a download href="{DATA_URL}">Download the complete human-adoption snapshot and update rules</a>. New releases will be preserved as separate dated records. The October 28 census data remain unchanged.</p></section>\n<!-- human-adoption:end -->'
p=ROOT/'statistics/index.html';html=p.read_text()
if '<!-- human-adoption:start -->' in html:
    html=re.sub(r'<!-- human-adoption:start -->.*?<!-- human-adoption:end -->',lambda _:section,html,flags=re.S)
else:
    match=re.search(r'<section\b[^>]*id="employment"[^>]*>',html);assert match
    html=html[:match.start()]+section+'\n\n'+html[match.start():]
if 'human-adoption.css' not in html:
    html=html.replace('</head>','<link rel="stylesheet" href="human-adoption.css?v=0.22"><script src="human-adoption.js?v=0.22" defer></script>\n</head>')
    html=html.replace('>01 Adoption</a>','>01 Adoption</a><a href="#human-adoption">People and AI</a>',1)
    html=html.replace('<section class="archive-section"', '<section class="archive-section"',1)
if '<!-- human-adoption-archive -->' not in html:
    anchor='<div class="archive-entry">'
    addition=f'<!-- human-adoption-archive --><div class="archive-entry"><div><h3>30 October 2026 / human adoption</h3><p>Three recurring panels · four charts<br>Frequency, barriers and reported versus measured benefits</p></div><a class="button" download href="{DATA_URL}">Download adoption snapshot ↓</a></div>'
    i=html.index(anchor,html.index('id="archive"'));html=html[:i]+addition+html[i:]
html=html.replace('No earlier publication snapshots exist yet.','The October 30 human-adoption snapshot supplements the initial October 28 census release.')
p.write_text(html)
print('Updated three recurring adoption panels; earlier census series preserved.')
