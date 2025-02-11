document.addEventListener('DOMContentLoaded', function() {
    // JavaScript-Code, der ausgeführt wird, sobald das HTML-Dokument vollständig geladen ist

    // 1. Karte initialisieren und auf den Container setzen
    var map = L.map('interactive-map-container').setView([52.5200, 13.4050], 13); // Berlin Zentrum als Startpunkt

    // 2. Kartenkachelebene (Tile Layer) hinzufügen (OpenStreetMap)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Optional: Marker zum Testen hinzufügen (z.B. Berlin Brandenburger Tor)
    var marker = L.marker([52.5163, 13.3777]).addTo(map);
    marker.bindPopup("<b>Brandenburger Tor, Berlin</b><br>Ein Beispiel-Marker.").openPopup();

});