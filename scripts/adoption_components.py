"""Shared, accessible adoption charts for the article and recurring census panels."""
from pathlib import Path
from html import escape
import json

ROOT=Path(__file__).resolve().parents[1]
DATA_URL='/statistics/data/2026-10-30/human-adoption-2026-10-30.json'
DATA=json.loads((ROOT/DATA_URL.lstrip('/')).read_text())

def render_chart(kind):
    d=DATA['charts'][kind];paired=len(d['periods'])==2
    out=[f'<figure class="human-chart" id="chart-{kind}"><figcaption><h3>{escape(d["title"])}</h3><p>{escape(d["population"])}</p></figcaption>']
    if paired:
        out.append(f'<div class="human-chart-controls" hidden><label for="view-{kind}">Chart view</label><select id="view-{kind}"><option value="compare">Compare both observations</option><option value="latest">Later observation only</option></select></div>')
    out.append('<p class="human-legend">'+''.join(f'<span class="{"prior" if paired and i==0 else "current"}">{escape(period)}</span>' for i,period in enumerate(d['periods']))+'</p>')
    out.append('<div class="human-plot" role="img" aria-label="'+escape(d['title']+'. Values and dates are listed in the data table immediately below.',quote=True)+'"><div class="human-axis"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>')
    for row in d['rows']:
        out.append('<div class="human-row"><p class="human-row-label">'+escape(row['label'])+'</p>')
        for j,value in enumerate(row['values']):
            cls='prior' if paired and j==0 else 'current'
            out.append(f'<div class="human-bar-row {cls}"><span class="human-period">{escape(d["periods"][j])}</span><div class="human-track"><span class="human-bar" style="width:{value:g}%"></span></div><strong>{value:g}%</strong></div>')
        out.append('</div>')
    out.append('</div>')
    out.append(f'<p class="human-comparison"><strong>Comparison:</strong> {escape(d["comparison"])}</p><p class="human-note">{escape(d["limits"])}</p>')
    out.append('<p class="human-note"><strong>'+('Source dates' if kind=='human_reach' else 'Published')+':</strong> '+escape('; '.join(d['publication_dates']))+'. <strong>Reviewed:</strong> October 30, 2026.</p>')
    out.append('<p class="human-sources">'+ ' · '.join(f'<a href="{escape(DATA["sources"][str(n)]["url"],quote=True)}">{escape(DATA["sources"][str(n)]["title"])}</a>' for n in d['refs'])+'</p>')
    out.append('<details class="human-data"><summary>Data, definitions and downloads</summary><div class="human-table-scroll" tabindex="0" role="region" aria-label="Chart data table"><table><caption>'+escape(d['population'])+'</caption><thead><tr><th scope="col">Measure</th>'+''.join('<th scope="col">'+escape(v)+'</th>' for v in d['periods'])+('<th scope="col">Change (percentage points)</th>' if paired else '')+'</tr></thead><tbody>')
    for row in d['rows']:
        out.append('<tr><th scope="row">'+escape(row['label'])+'</th>'+''.join(f'<td>{v:g}%</td>' for v in row['values'])+(f'<td>{row["change_pp"]:+g}</td>' if paired else '')+'</tr>')
    out.append('</tbody></table></div><p>'+escape(d['uncertainty'])+'</p><p><strong>Update rule:</strong> '+escape(d['cadence'])+'</p>')
    out.append(f'<p><a download href="/statistics/data/2026-10-30/{kind}-2026-10-30.csv">Download chart data (CSV)</a> · <a href="{DATA_URL}" download>Complete adoption snapshot</a> · <a href="/assets/issue-01/{kind}.svg">Print chart</a></p></details></figure>')
    return '\n'.join(out)
