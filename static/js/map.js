var map, points = [];

function redrawMapPoints(map, selector) {
    socket.emit('reports list', {}, function (data) {
        for (var i = 0; i < points.length; i++) {
            points[i].setMap(null);
        }
        points = [];

        for (i = 0; i < data.length; i++) {
            var report = data[i];
            if (selector != null) {
                if (report.status != selector) {
                    continue;
                }
            }
            var marker = new google.maps.Marker({
                map: map,
                position: new google.maps.LatLng(report.location.lat, report.location.lng)
            });
            console.log(marker);
            points.push(marker);
        }

        console.log('done redrawing');
    });
}

function initMap() {
    var mapDiv = document.getElementById('map');
    var map = new google.maps.Map(mapDiv, {
        center: {lat: 47.39, lng: 8.515},
        zoom: 16,
        mapTypeControlOptions: {
            mapTypeIds: [google.maps.MapTypeId.ROADMAP]
        },
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        styles: [
            {
                featureType: 'all',
                stylers: [
                    {saturation: -80}
                ]
            }, {
                featureType: 'road.arterial',
                elementType: 'geometry',
                stylers: [
                    {hue: '#00ffee'},
                    {saturation: 50}
                ]
            }, {
                featureType: 'poi.business',
                elementType: 'labels',
                stylers: [
                    {visibility: 'off'}
                ]
            }
        ]
    });

    redrawMapPoints(map);
}

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    //socket.emit('my event', {data: 'I\'m connected!'});
    console.log("Established socket.io connection");
});

socket.on('reports new', function (data) {
    console.log('Reports NEW', data);
});
