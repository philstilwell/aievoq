const horizon = document.querySelector('#forecast-horizon');
if (horizon) {
  const cards = [...document.querySelectorAll('.forecast-card')];
  const update = () => {
    let shown = 0;
    for (const card of cards) {
      card.hidden = Boolean(horizon.value && card.dataset.horizon !== horizon.value);
      if (!card.hidden) shown += 1;
    }
    document.querySelector('#forecast-filter-status').textContent = `${shown} draft forecasts`;
  };
  document.querySelector('.forecast-filter').hidden = false;
  horizon.addEventListener('change', update);
  update();
}
