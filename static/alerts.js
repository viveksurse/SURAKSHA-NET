function renderAlerts(rows){const el=document.getElementById("alertList");if(!rows.length){el.textContent="No alerts yet.";return;}
 el.innerHTML=rows.map(a=>`<div class="alert"><div><b>${escapeText(a.risk)} · ${escapeText(a.station_name)}</b><br>${escapeText(a.message)}<br><small>${escapeText(a.timestamp)}</small></div>
 ${a.acknowledged?"<small>ACKNOWLEDGED</small>":`<button onclick="ackAlert(${a.id})">Acknowledge</button>`}</div>`).join("");}
function escapeText(v){return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
async function ackAlert(id){await fetch(`/api/alerts/${id}/acknowledge`,{method:"POST"});refresh();}
