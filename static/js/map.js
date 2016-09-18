var map, points = [];

function redrawMapPoints(map, selector) {
    $('#loading-bar').show();

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

            if (report.needs.length == 1) {
                if (report.needs[0] == "water") {
                    marker.setIcon("static/images/droplet.png");
                } else if (report.needs[0] == "medic") {
                    marker.setIcon("static/images/medic.png");
                }
            } else {
                if (report.needs.indexOf("shelter") >= 0) {
                    marker.setIcon("static/images/shelter.png");
                } else if (report.needs.indexOf("food") >= 0) {
                    marker.setIcon("static/images/food.png");
                }
            }

            var contentString = '<div id="id"> ID: ' + report.id + '</div><br><div id="name"> ' + report.name + '</div><br><div id="phone"> PhoneNr.: ' + report.number + '</div><br><div id="content"> Needs : ' + report.needs.toString() + '</div>';

            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });

            google.maps.event.addListener(marker, 'click', (function (marker, contentString, infowindow) {
                return function () {
                    infowindow.setContent(contentString);
                    infowindow.open(map, marker);
                };
            })(marker, contentString, infowindow));

            console.log(marker);
            if (report.needs.length == 1) {
                points.push(marker);
            }
        }

        console.log('done redrawing');
        $('#loading-bar').hide();
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
                "featureType": "landscape",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": 65
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": 51
                    },
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": 30
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": 40
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "transit",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "administrative.province",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "lightness": -25
                    },
                    {
                        "saturation": -100
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [
                    {
                        "hue": "#ffff00"
                    },
                    {
                        "lightness": -25
                    },
                    {
                        "saturation": -97
                    }
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

socket.on('reports new', function (report) {
    console.log('New report', report);

    var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(report.location.lat, report.location.lng)
    });
    console.log(marker);
    points.push(marker);
});
