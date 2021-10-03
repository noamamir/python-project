var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {
  cors: {
    origin: '*',
  }
});

app.get('/', function(req, res) {
	
});

io.on('connection', function(socket){
	console.log('a user connected');
	socket.on('start-level', function(data){
		console.log('starting level ' + data);
		io.emit('start-level', data);
	});
	socket.on('user-login', function(data){
		console.log('user logged in ' + data);
		io.emit('user-login', data);
	});
	socket.on('stop-level', function(data){
		console.log('stopping level ' + data);
		io.emit('stop-level', data);
	});
	socket.on('end-level', function(data){
		console.log('ending level ' + data);
		io.emit('end-level', data);
	});
	socket.on('continue-level', function(data){
		console.log('continuing level ' + data);
		io.emit('continue-level', data);
	});
	socket.on('next-level', function(data){
		console.log('next level ' + data);
		io.emit('next-level', data);
	});
	socket.on('update-scoreboard', function(data){
		console.log('updating scoreboard ' + data);
		io.emit('update-scoreboard', data);
	});
	socket.on('new-user-submission', function(data){
		console.log('new user submission:' + data);
		io.emit('new-user-submission', data);
	});
});

http.listen(15006, "localhost", function(){
	console.log('listening at *:15006');
});