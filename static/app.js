(() => {
  "use strict";

  const _ = (e) => document.querySelector(e);

  //   Add version
  fetch("https://resume-retriever.herokuapp.com/resume/version")
    .then((res) => res.json())
    .then((data) => {
      const _d = new Date();
      const _v = ` ${_d.getFullYear()}.${_d.getMonth() + 1}.${data.version}`;
      _("#version").innerHTML = _v;
    });

  _("#download-resume").addEventListener("click", () => {
    window.location = "https://resume-retriever.herokuapp.com/resume";
  });
})();
