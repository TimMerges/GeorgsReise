document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('interactive-map-container').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Marker für Plymouth
    var plymouthMarker = L.marker([50.3755, -4.1427]).addTo(map);
    plymouthMarker.bindPopup("<b>Plymouth, England</b><br>Ausgangspunkt der Expedition (Juli 1772)");

    // Marker für Madera
    var madeiraMarker = L.marker([32.7607, -16.9595]).addTo(map);
    madeiraMarker.bindPopup("<b>Madeira</b><br>Erste Zwischenstation für Vorräte");


    map.setView([0, 0], 2); // Zentriere Karte auf 0,0
});
