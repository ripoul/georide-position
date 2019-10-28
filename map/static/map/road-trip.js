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
    var url = "/positions/"+username+"?startDate="+start.format('YYYY/MM/DD')+"&endDate="+end.format('YYYY/MM/DD');
    generateRoute(url);
});

var osmLayer = L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', { // LIGNE 16
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
});

map.addLayer(osmLayer);

function generateRoute(url) {
    fetch(url)
    .then(function (response) {
        if(response.status==401){
            throw "Token must be expired or not correct."
        }
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
        let popupContent = `current location : ${last.address}<br> speed : ${last.speed}km/h <br> altitude : ${last.altitude}m`
        lastPoint.bindPopup(popupContent).openPopup();
        document.querySelectorAll('.leaflet-popup-content').forEach(function (element) {
            // Now do something with my button
            element.classList.add("text-center");
        });

        map.setView([last.latitude, last.longitude], 11);

        lastDate = new Date(last.fixtime)

        // Format date
        const dateStr = lastDate.getDate().toString().padStart(2, '0');
        const monthStr = (lastDate.getMonth() + 1).toString().padStart(2, '0');
        const yearStr = lastDate.getFullYear().toString().padStart(4, '0');
        const hourStr = lastDate.getHours().toString().padStart(2, '0');
        const minuteStr = lastDate.getMinutes().toString().padStart(2, '0');

        toPrint = `Last info on selected dates : ${dateStr}/${monthStr}/${yearStr} at ${hourStr}h${minuteStr}`;
        document.getElementById("lastDate").innerHTML = toPrint;
    }).catch(error => {
        $('.alert').alert();
    })
}

generateRoute("/positions/"+username)