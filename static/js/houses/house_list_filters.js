document.addEventListener("DOMContentLoaded",(function(){const e=document.getElementById("district-select"),t=document.getElementById("municipality-select"),n=document.getElementById("parish-select"),i=document.getElementById("locale-select");e.value||(t.setAttribute("disabled","disabled"),n.setAttribute("disabled","disabled"),i.setAttribute("disabled","disabled")),e.addEventListener("change",(function(){const e=this.value;Array.from(t.options).forEach((t=>{t.style.display=t.getAttribute("data-district")===e?"block":"none"})),t.removeAttribute("disabled"),t.value=""})),t.addEventListener("change",(function(){const e=this.value;Array.from(n.options).forEach((t=>{t.style.display=t.getAttribute("data-municipality")===e?"block":"none"})),n.removeAttribute("disabled"),n.value=""})),n.addEventListener("change",(function(){const e=this.value;Array.from(i.options).forEach((t=>{t.style.display=t.getAttribute("data-parish")===e?"block":"none"})),i.removeAttribute("disabled"),i.value=""})),document.getElementById("reset-filters").addEventListener("click",(function(){window.location.href=window.location.pathname}))}));