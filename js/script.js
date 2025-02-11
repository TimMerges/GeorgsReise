document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('interactive-map-container').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Marker für Plymouth
    var plymouthMarker = L.marker([50.3755, -4.1427]).addTo(map);
    plymouthMarker.bindPopup("<b>Plymouth, England</b><br>Ausgangspunkt der Expedition (Juli 1772)<br><a href='https://www.wikidata.org/wiki/Q47525' target='_blank'>Wikidata: Plymouth</a>");

    // Marker für Madera
    var madeiraMarker = L.marker([32.7607, -16.9595]).addTo(map);
    madeiraMarker.bindPopup("<b>Madeira</b><br>Erste Zwischenstation für Vorräte<br><a href='https://www.wikidata.org/wiki/Q17712' target='_blank'>Wikidata: Madeira</a>");

    // Marker für Kapstadt (Kap der Guten Hoffnung) mit Wikidata-Link
    var capetownMarker = L.marker([-33.9249, 18.4241]).addTo(map);
    capetownMarker.bindPopup("<b>Kapstadt, Südafrika</b><br>Aufenthalt zum Auffüllen der Vorräte und Reparaturen (Okt.-Nov. 1772)<br><a href='https://www.wikidata.org/wiki/Q5465' target='_blank'>Wikidata: Kapstadt</a>");


    map.setView([0, 0], 2);
});
