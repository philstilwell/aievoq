"""Accessible charts and tables shared by the article and recurring census."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
DATA_URL='/statistics/data/2026-10-30/adjacent-ecosystems-2026-10-30-r2.json'
DATA=json.loads((ROOT/DATA_URL.lstrip('/')).read_text())

def render_adjacent_chart(kind):
    d=DATA['charts'][kind];paired=len(d['periods'])==2
    out=[f'<figure class="human-chart" id="chart-{kind}"><figcaption><h3>{e(d["title"])}</h3><p>{e(d["population"])}</p></figcaption>']
    out.append('<p class="human-note"><strong>What this means:</strong> '+e(d['definition'])+'</p>')
    if 'reading_example' in d:out.append('<p class="human-comparison"><strong>Reading the percentage:</strong> '+e(d['reading_example'])+'</p>')
    if paired:out.append(f'<div class="human-chart-controls" hidden><label for="view-{kind}">Chart view</label><select id="view-{kind}"><option value="compare">Compare both reports</option><option value="latest">Latest report only</option></select></div>')
    out.append('<p class="human-legend">'+''.join(f'<span class="{"prior" if paired and i==0 else "current"}">{e(p)}</span>' for i,p in enumerate(d['periods']))+'</p>')
    out.append('<div class="human-plot" role="img" aria-label="'+e(d['title']+'. Exact values and periods in the table below.',quote=True)+'"><div class="human-axis">'+''.join(f'<span>{v}%</span>' for v in ([0,7.5,15,22.5,30] if paired else [0,25,50,75,100]))+'</div>')
    for r in d['rows']:
        out.append('<div class="human-row"><p class="human-row-label">'+e(r['label'])+'</p>')
        for j,v in enumerate(r['values']):
            cls='prior' if paired and j==0 else 'current'
            out.append(f'<div class="human-bar-row {cls}"><span class="human-period">{e(r.get("periods",d["periods"])[j])}</span><div class="human-track"><span class="human-bar" style="width:{v/d["axis_max"]*100:.4f}%"></span></div><strong>{v:g}%</strong></div>')
        out.append('</div>')
    out.append('</div><p class="human-comparison"><strong>Comparison:</strong> '+e(d['comparison'])+'</p><p class="human-note">'+e(d['limits'])+'</p>')
    out.append('<p class="human-note"><strong>Source dates:</strong> '+e('; '.join(d['publication_dates']))+'. <strong>Retrieved:</strong> October 30, 2026.</p>')
    if 'license' in d:out.append('<p class="human-note">Statcounter Global Stats data and these adapted referral charts: <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>. Other content retains its existing rights.</p>')
    out.append('<p class="human-sources">'+' · '.join(f'<a href="{e(DATA["sources"][str(n)]["url"],quote=True)}">{e(DATA["sources"][str(n)]["title"])}</a>' for n in d['refs'])+'</p>')
    out.append('<details class="human-data"><summary>Data, definitions and downloads</summary><div class="human-table-scroll" tabindex="0" role="region" aria-label="Chart data"><table><caption>'+e(d['population'])+'</caption><thead><tr><th scope="col">Measure</th><th scope="col">Period</th><th scope="col">Percent</th></tr></thead><tbody>')
    for r in d['rows']:
        for j,v in enumerate(r['values']):out.append(f'<tr><th scope="row">{e(r["label"])}</th><td>{e(r.get("periods",d["periods"])[j])}</td><td>{v:g}%</td></tr>')
    out.append('</tbody></table></div><p><strong>Update rule:</strong> '+e(d['cadence'])+'</p>')
    out.append(f'<p><a download href="/statistics/data/2026-10-30/{kind}-2026-10-30-r2.csv">Download chart data (CSV)</a> · <a download href="{DATA_URL}">Snapshot with clarified definitions (r2)</a> · <a href="/assets/issue-01/{kind}.svg">Print chart</a></p><p>Revision r2 clarifies wording only; observations and values are unchanged.</p></details></figure>')
    return '\n'.join(out)

def referral_definitions():
    return '<aside class="referral-definitions" aria-label="Reading the river gauges"><p class="eyebrow">Reading the river gauges</p><h3>What is a referral?</h3><p>'+e(DATA['definitions']['referral'])+'</p><dl><dt>Search referral</dt><dd>'+e(DATA['definitions']['search_referral'])+'</dd><dt>AI-chatbot referral</dt><dd>'+e(DATA['definitions']['ai_chatbot_referral'])+'</dd></dl><p>'+e(DATA['definitions']['no_click'])+'</p><p>'+e(DATA['definitions']['separate_pools'])+'</p><p class="human-note">'+e(DATA['definitions']['classification'])+' <a href="/issues/2026-q4/sources/#source-117">Measurement notes</a></p></aside>'

def financial_table():
    out=['<p class="human-note">On narrow screens, scroll the table horizontally to see amounts and source dates.</p><div class="human-table-scroll adjacent-revenue" tabindex="0" role="region" aria-label="Company revenue data"><table><caption>Company periods, revenue and release dates. US dollars; Salesforce amounts are rounded to $0.1 billion.</caption><thead><tr><th scope="col">Company / measure</th><th scope="col">Period / end</th><th scope="col">Revenue (billions)</th><th scope="col">Annual growth</th><th scope="col">Published</th></tr></thead><tbody>']
    for r in DATA['financial_observations']:
        for j in range(2):out.append(f'<tr><th scope="row">{e(r["company"])} / {e(r["metric"])}</th><td>{e(r["periods"][j])}<br>{r["period_ends"][j]}</td><td>${r["revenue_usd_billion"][j]:.{1 if r["amount_precision_usd_billion"]==.1 else 3}f}</td><td>{r["reported_yoy_growth_pct"][j]:g}%</td><td><a href="{e(DATA["sources"][str(r["refs"][j])]["url"],quote=True)}">{r["published_on"][j]}</a></td></tr>')
    return ''.join(out)+'</tbody></table></div><p><a download href="/statistics/data/2026-10-30/adjacent_revenue-2026-10-30.csv">Download revenue, dates and source links (CSV)</a></p>'
