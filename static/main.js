var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log("Established socket.io connection");
});

socket.on('my response', function(data) {
    console.log('socket -> my event', data);
});

