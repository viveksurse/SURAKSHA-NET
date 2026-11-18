let hazardMap; const markers={};
function color(r){return r==="CRITICAL"?"#ef4444":r==="WARNING"?"#eab308":"#22c55e"}
function initMap(){
 if(!document.getElementById("map")||typeof L==="undefined")return;
 hazardMap=L.map("map").setView([22.5,79],5);
 L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:"© OpenStreetMap"}).addTo(hazardMap);
 [
 {station_id:"demo-srinagar",station_name:"Srinagar",latitude:34.0837,longitude:74.7973,risk:"NORMAL"},
 {station_id:"demo-dehradun",station_name:"Dehradun",latitude:30.3165,longitude:78.0322,risk:"WARNING"},
 {station_id:"demo-guwahati",station_name:"Guwahati",latitude:26.1445,longitude:91.7362,risk:"CRITICAL"},
 {station_id:"demo-mumbai",station_name:"Mumbai",latitude:19.076,longitude:72.8777,risk:"WARNING"},
 {station_id:"demo-chennai",station_name:"Chennai",latitude:13.0827,longitude:80.2707,risk:"NORMAL"}
 ].forEach(updateMarker);
}
function updateMarker(s){
 if(!hazardMap)return;
 let c=color(s.risk),m=markers[s.station_id];
 if(!m)m=L.circleMarker([s.latitude,s.longitude],{radius:9,color:c,fillColor:c,fillOpacity:.9}).addTo(hazardMap);
 m.setLatLng([s.latitude,s.longitude]);m.setStyle({color:c,fillColor:c});
 m.bindPopup(`<b>${s.station_name}</b><br>Risk: ${s.risk}<br>Source: ${s.source||"demo"}`);
 markers[s.station_id]=m;
}
document.addEventListener("DOMContentLoaded",initMap);
