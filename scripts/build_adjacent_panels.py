"""Refresh only the neighboring-habitats census section."""
from pathlib import Path
from html import escape as e
import json,re
from adjacent_components import render_adjacent_chart,financial_table,referral_definitions,DATA_URL
ROOT=Path(__file__).resolve().parents[1]
panels=json.loads((ROOT/'content/key-statistics-v0.27.json').read_text())['panels']
def panel(key):
    d=panels[key]
    return '<aside class="key-statistics" data-panel="'+key+'" aria-label="Key statistics"><p class="key-statistics-title">Key statistics</p><p class="key-statistics-scope">'+e(d['scope'])+'</p><dl>'+''.join('<div><dt>'+e(m['label'])+'</dt><dd>'+e(m['value'])+'</dd></div>' for m in d['metrics'])+'</dl><p class="key-statistics-comparison"><strong>Comparison:</strong> '+e(d['comparison'])+'</p><p class="key-statistics-limit">'+e(d['limits'])+'</p><p class="key-statistics-source"><strong>Source:</strong> '+e(d['source'])+' '+ ' · '.join(f'<a href="/issues/2026-q4/sources/#source-{n}">[{n}]</a>' for n in d['refs'])+'</p></aside>'
section='''<!-- adjacent-ecosystems:start -->
<section class="stat-section" id="neighboring-habitats" aria-labelledby="adjacent-title">
<div class="stat-heading"><div><p class="eyebrow">Neighboring habitats / snapshot 30 October 2026</p><h2 id="adjacent-title">Follow the clicks. Follow the spending.</h2></div><span class="cadence">Recurring record</span></div>
<div class="concept-intro"><span class="concept-label">AI concept</span><p>AI can redirect web discovery and change the tasks people pay software to perform. Traffic, revenue and customer behavior reveal different parts of that change. These measures track the surrounding businesses without assuming that AI caused every movement.</p></div>
<p class="section-intro">Three field stations: visits sent to websites, search revenue and the health of businesses selling software by subscription over the internet, known as software-as-a-service (SaaS). <a href="/issues/2026-q4/neighboring-habitats/">Read the illustrated article and comparison rules →</a></p>
<p class="data-note">Q4 remains open. September referral shares and earlier company quarters provide the opening record; October earnings releases report earlier periods. No completed Q4 outcome is shown.</p>
'''
section+=referral_definitions()+panel('adjacent-search')+render_adjacent_chart('adjacent_search')+render_adjacent_chart('adjacent_assistants')
section+='<h3>Search revenue and software businesses</h3><p>The initial software watchlist is Salesforce, ServiceNow and Adobe. It is illustrative, not a sector index. Google Search &amp; other is a business segment; the software measures cover entire companies.</p>'+panel('adjacent-software')+render_adjacent_chart('adjacent_growth')+financial_table()
section+='''<h3>AI disclosures: keep the measuring stick visible</h3><p>Salesforce reported Agentforce annual recurring revenue above $1.5 billion at July 31, but added Slackbot and Headless 360 to its scope in Q2 FY2027. This is a definition break, not a comparable sequential trend. ServiceNow’s October 28 AI annual contract value target of $1.7 billion for 2026 is a forecast, not an achieved result. Annual recurring revenue and annual contract value express recurring business or contracts on a one-year basis under each company’s definition. Neither figure is quarterly revenue. <a href="/issues/2026-q4/sources/#source-121">Salesforce disclosure</a> · <a href="/issues/2026-q4/sources/#source-123">ServiceNow target</a></p>
<h3>What we will keep measuring</h3><p>Capture referral shares monthly and compare matching quarter-end months. Refresh revenue after each earnings release, preserving fiscal dates and same-quarter-last-year growth. Keep companies in the history after mergers, failures or changes in reporting. Publish corrections as new dated snapshots.</p><p>Future records will track how often a search leads to a website click (click-through rate), how often it ends without one (zero-click rate), and how often visits produce a purchase or signup (conversion rate). Software measures will include keeping customers (retention), paid user licenses (seats), pricing and the share of sales left after specified costs (margins). These remain candidates until consistent sources and repeat observations are verified. Missing figures are unavailable, not zero. Changes in shares and growth rates use percentage points; revenue changes use percentages.</p>'''
section+=f'<p class="data-note"><a download href="{DATA_URL}">Download this snapshot, definitions and update rules</a>. Revision r2 clarifies the wording; all observations and values are unchanged. Earlier census snapshots remain available below.</p></section>\n<!-- adjacent-ecosystems:end -->'
p=ROOT/'statistics/index.html';text=p.read_text()
if '<!-- adjacent-ecosystems:start -->' in text:text=re.sub(r'<!-- adjacent-ecosystems:start -->.*?<!-- adjacent-ecosystems:end -->',lambda _:section,text,flags=re.S)
else:
    anchor='<section class="stat-section" id="employment"';assert anchor in text;text=text.replace(anchor,section+'\n\n'+anchor,1)
if 'href="#neighboring-habitats"' not in text:text=text.replace('<a href="#human-adoption">People and AI</a>','<a href="#human-adoption">People and AI</a><a href="#neighboring-habitats">Neighboring habitats</a>')
if '<!-- adjacent-archive -->' not in text:text=text.replace('<div class="archive-entry">',f'<!-- adjacent-archive --><div class="archive-entry"><div><h3>30 October 2026 / neighboring habitats</h3><p>Search and AI referral routes · search revenue · SaaS watchlist</p></div><a class="button" download href="{DATA_URL}">Download snapshot</a></div><div class="archive-entry">',1)
if '<!-- adjacent-r2-archive -->' not in text:text=text.replace('<!-- adjacent-archive -->',f'<!-- adjacent-r2-archive --><div class="archive-entry"><div><h3>30 October 2026 / neighboring habitats / r2</h3><p>Clearer definitions and examples; numerical observations unchanged</p></div><a class="button" download href="{DATA_URL}">Download clarified snapshot</a></div><!-- adjacent-archive -->',1)
p.write_text(text)
print('Neighboring-habitats census panels refreshed.')
