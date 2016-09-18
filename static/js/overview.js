var map, heatmap, points;

var ok = "ok";
var medic = "injured";
var medic2 = "heavily_injured";


var need_shelter = "shelter";
var need_water = "water";
var need_medic = "medic";
var need_food = "food";


function redrawPoints(selector) {
    $('#loading-bar').show();

    socket.emit('reports list', {}, function (data) {
        points.clear();

        for (var i = 0; i < data.length; i++) {
            var report = data[i];
            if (selector != null) {
                if (report.status != selector) {
                    continue;
                }
            }
            points.push({location: new google.maps.LatLng(report.location.lat, report.location.lng), weight: 0.65});
        }

        console.log('done redrawing');
        $('#loading-bar').hide();
    });
}


function redrawAllPoints() {
    socket.emit('reports list', {}, function (data) {
        points.clear();

        for (var i = 0; i < data.length; i++) {
            var report = data[i];
            points.push({location: new google.maps.LatLng(report.location.lat, report.location.lng), weight: 0.65});
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
                "elementType": "geometry",
                "stylers": [
                    {
                        "hue": "#ff4400"
                    },
                    {
                        "saturation": -68
                    },
                    {
                        "lightness": -4
                    },
                    {
                        "gamma": 0.72
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.icon"
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry",
                "stylers": [
                    {
                        "hue": "#0077ff"
                    },
                    {
                        "gamma": 3.1
                    }
                ]
            },
            {
                "featureType": "water",
                "stylers": [
                    {
                        "hue": "#00ccff"
                    },
                    {
                        "gamma": 0.44
                    },
                    {
                        "saturation": -33
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "stylers": [
                    {
                        "hue": "#44ff00"
                    },
                    {
                        "saturation": -23
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "hue": "#007fff"
                    },
                    {
                        "gamma": 0.77
                    },
                    {
                        "saturation": 65
                    },
                    {
                        "lightness": 99
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "gamma": 0.11
                    },
                    {
                        "weight": 5.6
                    },
                    {
                        "saturation": 99
                    },
                    {
                        "hue": "#0091ff"
                    },
                    {
                        "lightness": -86
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [
                    {
                        "lightness": -48
                    },
                    {
                        "hue": "#ff5e00"
                    },
                    {
                        "gamma": 1.2
                    },
                    {
                        "saturation": -23
                    }
                ]
            },
            {
                "featureType": "transit",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "saturation": -64
                    },
                    {
                        "hue": "#ff9100"
                    },
                    {
                        "lightness": 16
                    },
                    {
                        "gamma": 0.47
                    },
                    {
                        "weight": 2.7
                    }
                ]
            }
        ]
    });

    points = new google.maps.MVCArray([]);

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: points,
        map: map,
        radius: 32
    });
    redrawPoints();
}

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    //socket.emit('my event', {data: 'I\'m connected!'});
    console.log("Established socket.io connection");
});

socket.on('reports new', function (report) {
    console.log('New report', report);

    points.push({location: new google.maps.LatLng(report.location.lat, report.location.lng), weight: 1});
});
