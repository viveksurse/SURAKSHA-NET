let chart;
function initChart(){const c=document.getElementById("chart");if(!c||typeof Chart==="undefined")return;
 chart=new Chart(c,{type:"line",data:{labels:[],datasets:[
 {label:"Temperature °C",data:[],borderColor:"#54d7f5",tension:.25},
 {label:"Water distance cm",data:[],borderColor:"#facc15",tension:.25}]},
 options:{responsive:true,scales:{x:{ticks:{color:"#cbd9e8"}},y:{ticks:{color:"#cbd9e8"}}},plugins:{legend:{labels:{color:"#fff"}}}}});}
function updateChart(rows){if(!chart)return;chart.data.labels=rows.map(x=>new Date(x.timestamp).toLocaleTimeString());
 chart.data.datasets[0].data=rows.map(x=>x.temperature);chart.data.datasets[1].data=rows.map(x=>x.water_distance_cm);chart.update();}
document.addEventListener("DOMContentLoaded",initChart);
