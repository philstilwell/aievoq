'use strict';
// All values, sources and tables are present without JavaScript.
document.querySelectorAll('.human-chart').forEach(chart => {
  const control=chart.querySelector('.human-chart-controls');
  if(!control)return;
  const select=control.querySelector('select');
  control.hidden=false;
  select.addEventListener('change',()=>{chart.dataset.view=select.value;});
});
