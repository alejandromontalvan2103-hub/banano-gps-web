const map = L.map('map').setView([-5.194, -80.632], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);

let markerActual = null;
let lineaRuta = null;
let poligonoContorno = null;
let marcadorInicio = null;
let marcadorFin = null;

async function actualizarUbicacion() {
  try {
    const respuesta = await fetch('/api/ubicacion');
    const data = await respuesta.json();

    const latlng = [data.latitud, data.longitud];

    if (!markerActual) {
      markerActual = L.marker(latlng).addTo(map);
    } else {
      markerActual.setLatLng(latlng);
    }

    document.getElementById("info").innerText =
      `Vehículo: ${data.vehiculo} | Latitud: ${data.latitud} | Longitud: ${data.longitud} | Velocidad: ${data.velocidad} km/h | Hora: ${data.hora}`;

  } catch (error) {
    document.getElementById("info").innerText = "Error al obtener ubicación actual";
    console.error(error);
  }
}

async function actualizarRuta() {
  try {
    const respuesta = await fetch('/api/historial');
    const data = await respuesta.json();

    if (!Array.isArray(data) || data.length === 0) return;

    const puntos = data.map(p => [parseFloat(p.latitud), parseFloat(p.longitud)]);

    if (lineaRuta) map.removeLayer(lineaRuta);
    if (poligonoContorno) map.removeLayer(poligonoContorno);
    if (marcadorInicio) map.removeLayer(marcadorInicio);
    if (marcadorFin) map.removeLayer(marcadorFin);

    lineaRuta = L.polyline(puntos, {
      color: 'red',
      weight: 4
    }).addTo(map);

    marcadorInicio = L.marker(puntos[0]).addTo(map).bindPopup("Inicio");
    marcadorFin = L.marker(puntos[puntos.length - 1]).addTo(map).bindPopup("Fin");

    if (puntos.length >= 3) {
      poligonoContorno = L.polygon(puntos, {
        color: 'red',
        fillColor: 'red',
        fillOpacity: 0.15
      }).addTo(map);
    }

    map.fitBounds(lineaRuta.getBounds());

  } catch (error) {
    console.error("Error al cargar historial:", error);
  }
}

async function actualizarMapaCompleto() {
  await actualizarUbicacion();
  await actualizarRuta();
}

actualizarMapaCompleto();
setInterval(actualizarMapaCompleto, 3000);