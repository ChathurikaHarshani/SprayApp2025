$(window).load("load", pass_oauthCode);

function pass_oauthCode(){
  currentURL = window.location.href;
  //if (currentURL.includes("code=")){
    //  starti = currentURL.indexOf("code=");
    //  endi = currentURL.indexOf("&state=");
	  //parse auth code
	//  orgAuthCode = currentURL.substring((starti+5),endi);
	  //redirectURI = "http://johndeere.spray-safely.com/callback/.concat(orgAuthCode);
	  //window.location.replace(redirectURI);
  //}
  //redirectURL = "http://johndeere.spray-safely.com/callback".concat(window.location.search);
  window.location.replace(redirectURL);
}
