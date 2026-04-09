const map = L.map('map').setView([-5.2, -80.6], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);

const marker = L.marker([-5.2, -80.6]).addTo(map);

document.getElementById("info").innerText =
  "Ubicación de prueba cargada correctamente.";