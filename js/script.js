document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('interactive-map-container').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var testMarker = L.marker([0, 0]).addTo(map); // Marker bei 0,0 (Nullmeridian, Äquator)
    testMarker.bindPopup("Test-Marker");

    map.setView([0, 0], 2); // Zentriere Karte auf 0,0
});
