!function(n){function e(n){0===n.data.indexOf("capture:")&&t(n.data.substring(8))}function t(e){var t,e,o,r,i,s,a,c,d;if(t=e.indexOf(";"),0>t)throw new Error("Capture xdreceiver: Missing flags separator.");if(o=e.substring(0,t).split(","),s=e.substring(t+1),t=s.indexOf(":"),0>t)throw new Error("Capture xdreceiver: Missing func separator.");if(i=s.substring(0,t),r=decodeURIComponent(s.substring(t+1)),a=function(n,e){for(var t=0;t<n.length;t++)if(n[t]==e)return t;return-1},d={refresh:function(){n.document.cookie="janrain_sso_checked=;expires="+(new Date).toGMTString()+";path=/;"},logout:function(e){d.refresh(),n.document.location.href=e}},a(o,"sso")>=0)return c=d[i],c(r),void 0;try{if(c=window.eval(i),"undefined"==typeof c)throw new Error("unable to eval "+i);window.setTimeout(function(){c(r)},0)}catch(u){window.console&&console.log&&console.log("xdcomm: error running function "+i)}}window.addEventListener?window.addEventListener("message",e,!1):window.attachEvent?window.attachEvent("onmessage",e):document.attachEvent&&document.attachEvent("onmessage",e)}(this);