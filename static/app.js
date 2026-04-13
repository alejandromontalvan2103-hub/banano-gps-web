const map = L.map('map').setView([-5.194, -80.632], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);

let marker = null;

async function actualizarUbicacion() {
  try {
    const respuesta = await fetch('/api/ubicacion');
    const data = await respuesta.json();

    const latlng = [data.latitud, data.longitud];

    if (!marker) {
      marker = L.marker(latlng).addTo(map);
    } else {
      marker.setLatLng(latlng);
    }

    map.setView(latlng, 15);

    document.getElementById("info").innerText =
      `Vehículo: ${data.vehiculo} | Latitud: ${data.latitud} | Longitud: ${data.longitud} | Velocidad: ${data.velocidad} km/h | Hora: ${data.hora}`;
  } catch (error) {
    document.getElementById("info").innerText = "Error al obtener ubicación";
    console.error(error);
  }
}

actualizarUbicacion();
setInterval(actualizarUbicacion, 3000);