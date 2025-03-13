$(window).on("hashchange", pass_oauthCode);

function pass_oauthCode(){
  currentURL = window.location.href;
  if (currentURL.includes("code=")){
      starti = currentURL.indexof("code=");
      endi = currentURL.indexof("&state=");
  }
};
