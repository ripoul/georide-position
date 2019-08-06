var map = L.map('mapid').setView([46.116667, 3.416667], 11);

var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { // LIGNE 16
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
});

map.addLayer(osmLayer);

fetch('/positions')
    .then(function (response) {
        return response.text();
    }).then(positions => {
        listPoints = []
        positions = JSON.parse(positions)
        positions.forEach(element => {
            listPoints.push(new L.LatLng(element.latitude, element.longitude));
        });
        var firstpolyline = new L.Polyline(listPoints, {
            color: 'red',
            weight: 5,
            opacity: 1,
            smoothFactor: 1

        });

        map.addLayer(firstpolyline);
        last = positions[positions.length - 1];

        var marker = L.marker([last.latitude, last.longitude]);
        marker.addTo(map);
        let popupContent = `localisation actuelle : ${last.address}<br> Je roule à ${last.speed}km/h <br> A ${last.altitude}m d'altitude`
        marker.bindPopup(popupContent).openPopup();
        document.querySelectorAll('.leaflet-popup-content').forEach(function (element) {
            // Now do something with my button
            element.classList.add("text-center");
        });

        map.setView([last.latitude, last.longitude], 11);

    })