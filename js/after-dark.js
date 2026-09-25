(function(){var K='ag_after_dark_18';function open(){document.body.classList.remove('locked');load()}
try{if(localStorage.getItem(K)==='yes')open()}catch(e){}
document.getElementById('enter').addEventListener('click',function(){try{localStorage.setItem(K,'yes')}catch(e){}open()});
document.getElementById('leave').addEventListener('click',function(){try{localStorage.setItem(K,'no')}catch(e){}});
var done=false;function load(){if(done)return;done=true;document.querySelectorAll('.vid').forEach(function(f){var u=f.getAttribute('data-src');
fetch(u,{method:'HEAD'}).then(function(r){var t=r.headers.get('content-type')||'';if(r.ok&&t.indexOf('video')===0){var v=f.querySelector('video');v.src=u+'#t=4';f.classList.add('ok')}}).catch(function(){})})}})();
