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
            
            if(report.needs.length == 1){
            	if(report.needs[0] == "water"){
            		marker.setIcon("static/images/droplet.png");
            	}else if(report.needs[0] == "medic"){
            	    marker.setIcon("static/images/medic.png");
            	}else if(report.needs[0] == "shelter"){
            	    marker.setIcon("static/images/shelter.png");
            	}else if(report.needs[0] == "food"){
            	    marker.setIcon("static/images/food.png");
            	}
            }
            
            var contentString = '<div id="content">' +report.needs.toString() +'</div>';

  			var infowindow = new google.maps.InfoWindow({
    		content: contentString
  			});
            
            google.maps.event.addListener(marker,'click', (function(marker,contentString,infowindow){ 
    			return function() {
        		infowindow.setContent(contentString);
        		infowindow.open(map,marker);
    		};
			})(marker,contentString,infowindow));
            
            console.log(marker);
            if(report.needs.length == 1){
            	points.push(marker);
            }
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
