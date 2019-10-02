var firstpolyline;
var lastPoint;
var map = L.map('mapid').setView([46.116667, 3.416667], 11);

$('#rangepicker').daterangepicker({
    "startDate": startDate,
    "endDate": endDate,
    "minDate": startDate,
    "maxDate": endDate,
    "locale": {
        format: 'DD/MM/YYYY'
    }
}, function (start, end, label) {
    map.removeLayer(firstpolyline) ;
    map.removeLayer(lastPoint);
    var url = "/positions?startDate="+start.format('YYYY/MM/DD')+"&endDate="+end.format('YYYY/MM/DD');
    generateRoute(url);
});

var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { // LIGNE 16
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
});

map.addLayer(osmLayer);

function generateRoute(url) {
    fetch(url)
    .then(function (response) {
        return response.text();
    }).then(positions => {
        listPoints = []
        positions = JSON.parse(positions)
        positions.forEach(element => {
            listPoints.push(new L.LatLng(element.latitude, element.longitude));
        });
        firstpolyline = new L.Polyline(listPoints, {
            color: 'red',
            weight: 5,
            opacity: 1,
            smoothFactor: 1

        });

        map.addLayer(firstpolyline);
        last = positions[positions.length - 1];

        lastPoint = L.marker([last.latitude, last.longitude]);
        lastPoint.addTo(map);
        let popupContent = `localisation actuelle : ${last.address}<br> Je roule à ${last.speed}km/h <br> A ${last.altitude}m d'altitude`
        lastPoint.bindPopup(popupContent).openPopup();
        document.querySelectorAll('.leaflet-popup-content').forEach(function (element) {
            // Now do something with my button
            element.classList.add("text-center");
        });

        map.setView([last.latitude, last.longitude], 11);

        lastDate = new Date(last.fixtime)
        toPrint = `Dernier mouvement reçu le ${lastDate.getDate()}/${lastDate.getMonth() + 1}/${lastDate.getFullYear()} à ${lastDate.getHours()}h${lastDate.getMinutes()}`;
        document.getElementById("lastDate").innerHTML = toPrint;
    })
}

generateRoute("/positions")