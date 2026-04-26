const map = L.map('map').setView([-5.09, -81.09], 14);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let marcador = null;

// 🔴 CONTORNO
async function cargarContorno() {
  const res = await fetch('/api/contorno');
  const data = await res.json();

  const puntos = data.map(p => [p.latitud, p.longitud]);

  if (puntos.length >= 3) {
    L.polygon(puntos, {
      color: 'red',
      fillOpacity: 0.2
    }).addTo(map);

    map.fitBounds(puntos);
  }
}

// 📍 GPS
async function actualizarGPS() {
  const res = await fetch('/api/ubicacion');
  const data = await res.json();

  const pos = [data.latitud, data.longitud];

  if (!marcador) {
    marcador = L.marker(pos).addTo(map);
  } else {
    marcador.setLatLng(pos);
  }

  document.getElementById("info").innerText =
    `Lat: ${data.latitud} | Lon: ${data.longitud} | Hora: ${data.hora}`;
}

cargarContorno();
actualizarGPS();
setInterval(actualizarGPS, 3000);