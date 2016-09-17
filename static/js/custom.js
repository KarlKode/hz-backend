$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }

    /*
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
        console.log("Established socket.io connection");
    });

    socket.on('my response', function(data) {
        console.log('socket -> my event', data);
    });
    */
});

function initMap() {
  var var_location = new google.maps.LatLng(45.430817,12.331516);


  var mapDiv = document.getElementById('map');
  var map = new google.maps.Map(mapDiv, {
      center: {lat: 44.540, lng: -78.546},
      zoom: 8
  });
}

$("#addRow").click(function(){
console.log("add pressed");
var row = $("<tr><td>123</td><td>MaxMuster</td><td>ios</td><td>+41791231234</td><td>status</td><td>12.000</td><td>13.000</td><td>medic</td><td>open</td><td>skills</td><td><ahref=#></a></td></tr>");
$("#logtable > tbody").append(row);
});

