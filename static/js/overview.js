function initMap() {
  var var_location = new google.maps.LatLng(45.430817,12.331516);


  var mapDiv = document.getElementById('map');
  var map = new google.maps.Map(mapDiv, {
      center: {lat: 44.540, lng: -78.546},
      zoom: 8
  });
}
