document.addEventListener('DOMContentLoaded', function() {
    // JavaScript-Code, der ausgeführt wird, sobald das HTML-Dokument vollständig geladen ist

    // 1. Karte initialisieren und auf den Container setzen
    var map = L.map('interactive-map-container').setView([0, 0], 2); // Startposition und Zoom global

    // 2. Kartenkachelebene (Tile Layer) hinzufügen (OpenStreetMap)
    L.tileLayer('https://tile.openstreetmap.org/{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Marker für Plymouth
    var plymouthMarker = L.marker([50.3755, -4.1427]).addTo(map);
    plymouthMarker.bindPopup("<b>Plymouth, England</b><br>Ausgangspunkt der Expedition (Juli 1772)");

    // Marker für Madera
    var madeiraMarker = L.marker([32.7607, -16.9595]).addTo(map);
    madeiraMarker.bindPopup("<b>Madeira</b><br>Erste Zwischenstation für Vorräte");

    // Marker für Kapstadt (Kap der Guten Hoffnung)
    var capetownMarker = L.marker([-33.9249, 18.4241]).addTo(map);
    capetownMarker.bindPopup("<b>Kapstadt, Südafrika</b><br>Aufenthalt zum Auffüllen der Vorräte und Reparaturen (Okt.-Nov. 1772)<br><a href='https://de.wikipedia.org/wiki/Kapstadt' target='_blank'>Wikipedia</a>");

    // Zentrum der Karte auf Europa setzen, damit Plymouth und Madera sichtbar sind
    map.setView([40, -10], 4); // Angepasste Zentrumskoordinaten und Zoom
});
