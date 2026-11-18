async function demo(condition){const r=await fetch("/api/demo",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({condition})});const x=await r.json();if(!r.ok)alert(x.error);else refresh();}
async function refresh(){try{
 const r=await fetch("/api/dashboard"),d=await r.json();document.getElementById("mode").textContent=d.mode+" MODE";
 const rows=d.readings||[];if(rows.length){const x=rows[0];
 document.getElementById("temp").textContent=x.temperature.toFixed(1)+" °C";
 document.getElementById("humidity").textContent=x.humidity.toFixed(1)+" %";
 document.getElementById("water").textContent=x.water_distance_cm.toFixed(1)+" cm";
 document.getElementById("rain").textContent=x.rainfall_percent.toFixed(1)+" %";
 const risk=document.getElementById("risk");risk.className="risk "+x.risk;
 document.getElementById("riskValue").textContent=x.risk;
 document.getElementById("riskMessage").textContent=x.risk==="NORMAL"?"Within prototype normal range":x.risk==="WARNING"?"Potential risk detected; monitor readings":"Critical prototype condition; verify readings";
 rows.forEach(updateMarker);
 const h=await fetch("/api/history?station_id="+encodeURIComponent(x.station_id));updateChart(await h.json());
 }renderAlerts(d.alerts||[]);
 }catch(e){document.getElementById("mode").textContent="SERVER OFFLINE";console.error(e);}}
function tick(){document.getElementById("clock").textContent=new Date().toLocaleString();}
document.addEventListener("DOMContentLoaded",()=>{tick();refresh();setInterval(tick,1000);setInterval(refresh,3000);});
