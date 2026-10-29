/* Search only enhances the server-rendered, fully readable table of contents. */
(() => {
  const form = document.querySelector('#contents-tools');
  if (!form) return;
  const input = form.querySelector('#article-search');
  const department = form.querySelector('#department');
  const status = document.querySelector('#search-status');
  const entries = [...document.querySelectorAll('.contents-entry')];
  const groups = [...document.querySelectorAll('.contents-group')];
  const normalize = text => text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  fetch('./search-index.json').then(response => {
    if (!response.ok) throw new Error('Search index unavailable');
    return response.json();
  }).then(records => {
    const index = new Map(records.map(record => [record.slug, normalize(`${record.title} ${record.subtitle} ${record.category} ${record.text}`)]));
    const update = () => {
      const terms = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
      let count = 0;
      for (const entry of entries) {
        const text = index.get(entry.dataset.slug) || '';
        const match = (!department.value || department.value === entry.dataset.category) && terms.every(term => text.includes(term));
        entry.hidden = !match;
        count += Number(match);
      }
      groups.forEach(group => { group.hidden = ![...group.querySelectorAll('.contents-entry')].some(entry => !entry.hidden); });
      status.hidden = false;
      status.textContent = `${count} of ${entries.length} reading sections shown`;
      document.querySelector('#no-results').hidden = count !== 0;
    };
    input.addEventListener('input', update);
    department.addEventListener('change', update);
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('reset', () => { input.value = ''; department.value = ''; update(); input.focus(); });
    form.hidden = false;
  }).catch(() => { /* The complete contents remain usable without search. */ });
})();
