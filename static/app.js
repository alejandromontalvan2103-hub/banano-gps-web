const map = L.map('map').setView([-5.194, -80.632], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);

let markerActual = null;
let lineaRuta = null;
let poligonoContorno = null;
let marcadorInicio = null;
let marcadorFin = null;

// CARGA EL RECORRIDO/POLIGONO UNA SOLA VEZ
async function cargarRecorridoFijo() {
  try {
    const respuesta = await fetch('/api/historial');
    const data = await respuesta.json();

    if (!Array.isArray(data) || data.length === 0) return;

    const puntos = data.map(p => [parseFloat(p.latitud), parseFloat(p.longitud)]);

    // Dibujar línea roja permanente
    lineaRuta = L.polyline(puntos, {
      color: 'red',
      weight: 4
    }).addTo(map);

    // Marcar inicio y fin
    marcadorInicio = L.marker(puntos[0]).addTo(map).bindPopup("Inicio");
    marcadorFin = L.marker(puntos[puntos.length - 1]).addTo(map).bindPopup("Fin");

    // Dibujar polígono rojo semitransparente
    if (puntos.length >= 3) {
      poligonoContorno = L.polygon(puntos, {
        color: 'red',
        fillColor: 'red',
        fillOpacity: 0.12
      }).addTo(map);
    }

    map.fitBounds(lineaRuta.getBounds());

  } catch (error) {
    console.error("Error al cargar recorrido fijo:", error);
  }
}

// ACTUALIZA SOLO LA POSICIÓN GPS ACTUAL
async function actualizarUbicacionActual() {
  try {
    const respuesta = await fetch('/api/ubicacion');
    const data = await respuesta.json();

    const latlng = [parseFloat(data.latitud), parseFloat(data.longitud)];

    if (!markerActual) {
      markerActual = L.marker(latlng).addTo(map).bindPopup("GPS actual");
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

// SE CARGA UNA SOLA VEZ EL RECORRIDO ROJO
cargarRecorridoFijo();

// SE ACTUALIZA SIEMPRE EL GPS EN TIEMPO REAL
actualizarUbicacionActual();
setInterval(actualizarUbicacionActual, 3000);