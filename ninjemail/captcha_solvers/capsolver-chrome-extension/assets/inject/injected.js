const capsolverListeningList = [
  '/recaptcha/api2/reload',
  '/recaptcha/api2/userverify',
  '/recaptcha/enterprise/reload',
  '/recaptcha/enterprise/userverify',
  'hcaptcha.com/getcaptcha',
  '/gfct',
  '/problem',
  '/verify',
];

(function (xhr) {
  var XHR = XMLHttpRequest.prototype;

  var open = XHR.open;
  var send = XHR.send;

  XHR.open = function (method, url) {
    this._method = method;
    this._url = url;
    return open.apply(this, arguments);
  };

  XHR.send = function (postData) {
    const _url = this._url;
    this.addEventListener('load', function () {
      const isInList = capsolverListeningList.some(url => _url.indexOf(url) !== -1);
      if (isInList) {
        window.postMessage({ type: 'xhr', data: this.response, url: _url }, '*');
      }
    });

    return send.apply(this, arguments);
  };
})(XMLHttpRequest);

(function () {
  let origFetch = window.fetch;
  window.fetch = async function (...args) {
    const _url = args[0];
    const response = await origFetch(...args);

    response
      .clone()
      .blob()
      .then(async data => {
        const isInList = capsolverListeningList.some(url => _url.indexOf(url) !== -1);
        if (isInList) {
          window.postMessage(
            {
              type: 'fetch',
              data: await data.text(),
              url: _url,
            },
            '*',
          );
        }
      })
      .catch(err => {
        console.log(err);
      });

    return response;
  };
})();
