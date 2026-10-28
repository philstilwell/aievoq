'use strict';
// One reviewed snapshot powers the charts; static tables remain usable without JavaScript.
const SNAPSHOT = 'data/snapshot-2026-10-28.json';
const C = {blue:'#1255c7', copper:'#ac5538', ink:'#132432', muted:'#53636d', grid:'#d5d1c5'};
const ns = 'http://www.w3.org/2000/svg';
function el(tag, attrs={}, text) {
  const n=document.createElementNS(ns,tag);
  Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));
  if(text!==undefined)n.textContent=text;
  return n;
}
function chart(id,height,title,description) {
  const svg=el('svg',{viewBox:`0 0 800 ${height}`,role:'img','aria-labelledby':`${id}-svg-title ${id}-svg-desc`});
  svg.append(el('title',{id:`${id}-svg-title`},title),el('desc',{id:`${id}-svg-desc`},description));
  document.getElementById(`${id}-chart`).replaceChildren(svg);
  return svg;
}
function text(s,x,y,value,opts={}) {s.append(el('text',{x,y,fill:C.muted,'font-family':'Arial, sans-serif','font-size':13,...opts},value));}
function line(s,x1,y1,x2,y2,opts={}) {s.append(el('line',{x1,y1,x2,y2,stroke:C.grid,'stroke-width':1,...opts}));}
function dot(s,x,y,color,value){const n=el('circle',{cx:x,cy:y,r:4,fill:color});n.append(el('title',{},value));s.append(n);}
const signed=v=>v===0?'0.0%':`${v>0?'+':''}${v.toFixed(1)}%`;
function adoption(data,mode) {
  const rows=mode==='quarters'?data.adoption_snapshots:data.adoption;
  const s=chart('adoption',300,'Business adoption',`${rows.length} reference windows. Recent use ends at 24.6%; expected use at 28.6%. Whiskers are one standard error. Full values are in the data table and download.`);
  const x=i=>58+i*654/(rows.length-1), y=v=>249-v*5.8;
  for(const v of [0,10,20,30,35]){line(s,58,y(v),712,y(v));text(s,45,y(v)+4,`${v}%`,{'text-anchor':'end'});}
  for(const [key,se,color,dash] of [['recent_pct','recent_se_pp',C.blue,''],['expected_pct','expected_se_pp',C.copper,'7 5']]) {
    s.append(el('polyline',{points:rows.map((r,i)=>`${x(i)},${y(r[key])}`).join(' '),fill:'none',stroke:color,'stroke-width':2.5,'stroke-dasharray':dash}));
    rows.forEach((r,i)=>{line(s,x(i),y(r[key]-r[se]),x(i),y(r[key]+r[se]),{stroke:color,'stroke-width':1.4});const point=el('circle',{cx:x(i),cy:y(r[key]),r:2.3,fill:color});point.append(el('title',{},`${r.reference_start}–${r.reference_end}: ${r[key].toFixed(1)}%, ±${r[se]} points (1 SE)`));s.append(point);for(const v of [r[key]-r[se],r[key]+r[se]])line(s,x(i)-3.5,y(v),x(i)+3.5,y(v),{stroke:color,'stroke-width':1});});
    text(s,724,y(rows.at(-1)[key])+5,`${rows.at(-1)[key].toFixed(1)}%`,{fill:color,'font-weight':700,'font-size':16});
  }
  const labels=mode==='quarters'?[[0,'Q4 2025'],[1,'Q1 2026'],[2,'Q2 2026'],[3,'Q3 2026'],[4,'Latest*']]:[[0,'Nov 2025'],[4,'Jan 2026'],[11,'Apr'],[17,'Jul'],[23,'Oct']];
  labels.forEach(([i,v])=>text(s,x(i),276,v,{'text-anchor':'middle'}));
  document.getElementById('adoption-caption').textContent=mode==='quarters'?'Final reference window wholly inside each completed quarter; *latest window crosses Q3/Q4. Reconstructed from the October workbook, not quarterly averages. Whiskers: ±1 standard error.':'Reference windows, November 2025–October 2026. Whiskers show ±1 standard error.';
}
function employment(data,group) {
  const rows=data.employment,age=group==='young'?'Ages 22–25':'All ages';
  const s=chart('employment',300,`${age}: annual employment growth`,`${age}, June to September 2026. High exposure and least exposure groups. Values are in the table below; exposure is not proof of an AI-caused job loss.`);
  const x=i=>75+i*208,y=v=>242-(v+5)*31;
  for(const v of [-4,-2,0,2]){line(s,60,y(v),722,y(v),{stroke:v===0?C.ink:C.grid});text(s,46,y(v)+4,`${v>0?'+':''}${v}%`,{'text-anchor':'end'});}
  for(const [key,color] of [[`${group}_high_yoy_pct`,C.copper],[`${group}_least_yoy_pct`,C.blue]]) {
    s.append(el('polyline',{points:rows.map((r,i)=>`${x(i)},${y(r[key])}`).join(' '),fill:'none',stroke:color,'stroke-width':2.5}));
    rows.forEach((r,i)=>{dot(s,x(i),y(r[key]),color,`${r.month}: ${signed(r[key])}`);text(s,x(i),y(r[key])-12,signed(r[key]),{'text-anchor':'middle',fill:color,'font-weight':700,'font-size':16});});
  }
  ['June','July','August','September'].forEach((m,i)=>text(s,x(i),273,m,{'text-anchor':'middle'}));
}
function capability(data) {
  const rows=data.capability.filter(r=>r.score_pct>0);
  const s=chart('capability',280,'FrontierMath Erdős results','Five nonzero results, with one-standard-error bars. The highest is 4.4%. Eight further configurations have zero observed successes. All 13 are in the table.');
  const x=v=>252+v*44;
  for(const v of [0,2,4,6,8,10]){line(s,x(v),18,x(v),228);text(s,x(v),252,`${v}%`,{'text-anchor':'middle'});}
  rows.forEach((r,i)=>{const y=38+i*42,lo=Math.max(0,r.score_pct-r.se_pp),hi=r.score_pct+r.se_pp;
    text(s,9,y+5,r.model,{fill:C.ink,'font-size':14});line(s,x(lo),y,x(hi),y,{stroke:C.blue,'stroke-width':2});
    [lo,hi].forEach(v=>line(s,x(v),y-6,x(v),y+6,{stroke:C.blue,'stroke-width':2}));dot(s,x(r.score_pct),y,C.blue,`${r.model}: ${r.score_pct.toFixed(2)}%, ±${r.se_pp.toFixed(2)} points`);
    text(s,x(hi)+12,y+5,`${r.score_pct.toFixed(1)}%`,{fill:C.ink,'font-weight':700,'font-size':15});
  });
}
function prices(data) {
  const s=chart('prices',220,'Fixed text-price basket','Claude Haiku 5.5: $0.225. GPT-6.1 Terra: $2.250. Input and output charges are stacked. This compares a fixed billed volume, not equivalent quality.');
  const x0=218,scale=195;
  for(const v of [0,1,2]){line(s,x0+v*scale,18,x0+v*scale,176);text(s,x0+v*scale,201,`$${v}`,{'text-anchor':'middle'});}
  data.prices.forEach((r,i)=>{const y=38+i*80,a=r.input_usd_per_million,b=.25*r.output_usd_per_million;text(s,10,y+23,r.model,{fill:C.ink,'font-size':15});
    s.append(el('rect',{x:x0,y,width:a*scale,height:35,fill:C.copper}),el('rect',{x:x0+a*scale,y,width:b*scale,height:35,fill:C.blue}));text(s,x0+(a+b)*scale+12,y+23,`$${r.basket_usd.toFixed(3)}`,{fill:C.ink,'font-weight':700,'font-size':17});
  });
}
// Separate function to keep the forecast visually distinct from observed history.
function energyChart(data) {
  const s=chart('energy',230,'Global data-centre electricity','2025 estimated consumption: 485 terawatt-hours. 2030 central projection: 950 terawatt-hours. Both include non-AI work; the second is a forecast.');
  const x0=225,scale=.45;
  for(const v of [0,500,1000]){line(s,x0+v*scale,18,x0+v*scale,184);text(s,x0+v*scale,212,String(v),{'text-anchor':'middle'});}
  data.energy.forEach((r,i)=>{const y=37+i*85,color=i?C.copper:C.blue;text(s,10,y+26,`${r.year} / ${i?'projection':'estimate'}`,{fill:C.ink,'font-size':15});s.append(el('rect',{x:x0,y,width:r.value_twh*scale,height:40,fill:i?'none':color,stroke:color,'stroke-width':2,'stroke-dasharray':i?'7 5':''}));text(s,x0+r.value_twh*scale+14,y+27,String(r.value_twh),{fill:color,'font-size':19,'font-weight':700});});
}
async function init(){
  try {
    const res=await fetch(SNAPSHOT);if(!res.ok)throw new Error('Snapshot unavailable');const data=await res.json();
    if(data.schema_version!==1)throw new Error('Unrecognized data format');
    adoption(data,'waves');employment(data,'young');capability(data);prices(data);energyChart(data);
    document.querySelectorAll('.chart-controls').forEach(n=>n.hidden=false);
    document.getElementById('adoption-view').addEventListener('change',e=>adoption(data,e.target.value));
    document.getElementById('employment-view').addEventListener('change',e=>employment(data,e.target.value));
  } catch(err){const n=document.getElementById('chart-status');n.hidden=false;n.textContent='The charts could not load. The verified tables, source notes and data downloads below are still available.';}
}
init();
