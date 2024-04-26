(function() {
  window.addEventListener('message', function(event) {
    if (event.data.type !== 'capsolverCallback') return;
    window[event.data.callback]&& window[event.data.callback]();
  })
})();