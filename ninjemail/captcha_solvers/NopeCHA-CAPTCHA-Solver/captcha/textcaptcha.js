(()=>{var p=chrome;var y="https://api.nopecha.com",i="https://www.nopecha.com",B="https://developers.nopecha.com",ie={doc:{url:B,automation:{url:`${B}/guides/extension_advanced/#automation-build`}},api:{url:y,recognition:{url:`${y}/recognition`},status:{url:`${y}/status`}},www:{url:i,annoucement:{url:`${i}/json/announcement.json`},demo:{url:`${i}/demo`,hcaptcha:{url:`${i}/demo/hcaptcha`},recaptcha:{url:`${i}/demo/recaptcha`},funcaptcha:{url:`${i}/demo/funcaptcha`},awscaptcha:{url:`${i}/demo/awscaptcha`},turnstile:{url:`${i}/demo/turnstile`},textcaptcha:{url:`${i}/demo/textcaptcha`},perimeterx:{url:`${i}/demo/perimeterx`}},manage:{url:`${i}/manage`},pricing:{url:`${i}/pricing`},setup:{url:`${i}/setup`}},discord:{url:`${i}/discord`},github:{url:`${i}/github`,release:{url:`${i}/github/release`}}};function M(e){let t=("6146a541f7b2046020e84d44aa2e1e120f2ad8b75ac9b6fc236f65f737a7006f"+e).split("").map(n=>n.charCodeAt(0));return I(t)}var T=new Uint32Array(256);for(let e=256;e--;){let t=e;for(let n=8;n--;)t=t&1?3988292384^t>>>1:t>>>1;T[e]=t}function I(e){let t=-1;for(let n of e)t=t>>>8^T[t&255^n];return(t^-1)>>>0}async function g(e,t){let n=""+[+new Date,performance.now(),Math.random()],[a,o]=await new Promise(s=>{p.runtime.sendMessage([n,e,...t],s)});if(a===M(n))return o}function H(){let e;return t=>e||(e=t().finally(()=>e=void 0),e)}var G=H(),m;function $(){return G(async()=>(m||(m=await g("settings::get",[])),m))}function E(e){m&&(m={...m,...e},L(m))}function f(){return m}function r(e){return new Promise(t=>setTimeout(t,e))}var P=[];function D(e,t){e.timedout=!1,P.push(e);let n,a=setInterval(async()=>{await R(e,f())||(clearTimeout(n),clearInterval(a))},400);t&&(n=setTimeout(()=>clearInterval(a),t),e.timedout=!0)}async function R(e,t){if(e.timedout)return!1;let n=e.condition(t);if(n===e.running())return!1;if(!n&&e.running())return e.quit(),!1;if(n&&!e.running()){for(;!e.ready();)await r(200);return e.start(),!1}}function L(e){P.forEach(t=>R(t,e))}function A(){p.runtime.connect({name:"stream"}).onMessage.addListener(t=>{t.event==="settingsUpdate"&&E(t.settings)})}function C(e){if(document.readyState!=="loading")setTimeout(e,0);else{let t;t=()=>{removeEventListener("DOMContentLoaded",t),e()},addEventListener("DOMContentLoaded",t)}}function J(e,t){let n=document.createElement("canvas");return n.width=e,n.height=t,n}function q(e){return e.toDataURL("image/jpeg").replace(/data:image\/[a-z]+;base64,/g,"")}function X(e){try{e.getContext("2d").getImageData(0,0,1,1)}catch{return!0}return!1}async function h(e,t,n=1e4){if(!t&&!e.complete&&!await new Promise(c=>{let u=setTimeout(()=>{c(!1)},n);e.addEventListener("load",()=>{clearTimeout(u),c(!0)})}))return;let a=J(e.naturalWidth||t?.clientWidth,e.naturalHeight||t?.clientHeight);return a.getContext("2d").drawImage(e,0,0),!X(a)&&a}async function N(e){let n=getComputedStyle(e).backgroundImage;if(!n||n==="none")if("src"in e&&e.src)n=`url("${e.src}")`;else return;if("computedStyleMap"in e){let d=e.computedStyleMap().get("background-image");if(d instanceof CSSImageValue){let l=await h(d,e);if(l)return l}}let a=/"(.+)"/.exec(n);if(!a)return;n=a[1];let o=document.createElement("a");if(o.href=n,new URL(o.href).origin===document.location.origin){let d=new Image;d.crossOrigin="anonymous",d.src=n;let l=await h(d);if(l)return l}let s=await g("fetch::asData",[n,{}]),c=new Image;c.crossOrigin="anonymous",c.src=s.data;let u=await h(c);if(u)return u}function Y(e,t,n,a){let o=(a*t+n)*4;return[e[o],e[o+1],e[o+2]]}function Z(e,t){return e.every(n=>n<=t)}function ee(e,t){return e.every(n=>n>=t)}function U(e,t=0,n=230,a=.99){let o=e.getContext("2d"),s=o.canvas.width,c=o.canvas.height;if(s===0||c===0)return!0;let u=o.getImageData(0,0,s,c).data,d=0;for(let x=0;x<c;x++)for(let w=0;w<s;w++){let k=Y(u,s,w,x);(Z(k,t)||ee(k,n))&&d++}return d/(s*c)>a}function W(){return[]}function z(e){return new Promise(t=>{e.push(t)})}function b(e){e.forEach(t=>t()),e.splice(0)}async function O(e,t){let n={v:p.runtime.getManifest().version,key:te(e)};return n.url=await g("tab::getURL",[]),n}function te(e){return!e.keys||!e.keys.length?e.key:e.keys[Math.floor(Math.random()*e.keys.length)]}var v=W(),S,_=!1;function j(){let e=f(),t=document.querySelector(e.textcaptcha_image_selector),n=document.querySelector(e.textcaptcha_input_selector);return!t||!n?!1:(g("tab::registerDetectedCaptcha",["textcaptcha"]),!0)}function K(){_=!0,b(v),S=new MutationObserver(async()=>{setTimeout(()=>b(v),200)}),S.observe(document.body,{subtree:!0,childList:!0,attributes:!0}),ae()}function V(){S.disconnect(),_=!1,b(v)}function Q(){return _}async function ne(e){if(e instanceof HTMLCanvasElement)return e;if(e instanceof HTMLImageElement&&(e.src||e.srcset)){let t=await h(e);if(t)return t}return await N(e)}var F=!1;async function ae(){if(F)return;F=!0;let e;for(;_;){let t=f(),n=document.querySelector(t.textcaptcha_image_selector),a=document.querySelector(t.textcaptcha_input_selector);if(!n){await r(500);continue}if(!a){await r(500);continue}if(a.click(),a.focus(),await r(200),a.value!==""){await r(500);continue}let o=await ne(n);if(!o){await r(500);continue}if(U(o)){await r(500);continue}let s=q(o);if(e===s){await r(500);continue}e=s;let c=new Date().valueOf(),u=await g("api::recognition",[{type:"textcaptcha",image_data:[s],...await O(t)}]);if(!u||"error"in u){console.warn("[@nope/textcaptcha] api error",u),await r(2e3);continue}let d=new Date().valueOf();if(t.textcaptcha_solve_delay){let l=t.textcaptcha_solve_delay_time-d+c;l>0&&await r(l)}if(u.data&&u.data.length>0&&!a.value){a.click(),a.focus(),await r(200),a.value=u.data[0];for(let l of u.data[0])a.dispatchEvent(new KeyboardEvent("keydown",{key:l})),await r(50),a.dispatchEvent(new KeyboardEvent("keypress",{key:l})),await r(50),a.dispatchEvent(new KeyboardEvent("keyup",{key:l})),await r(50)}await z(v)}}async function oe(){A(),await $(),await g("tab::registerDetectedCaptcha",["textcaptcha"]);let e=location.hostname;D({name:"textcaptcha/auto-solve",condition:t=>t.enabled&&t.textcaptcha_auto_solve&&!t.disabled_hosts.includes(e)&&!!t.textcaptcha_image_selector&&!!t.textcaptcha_input_selector,ready:j,start:K,quit:V,running:Q})}C(oe);})();
