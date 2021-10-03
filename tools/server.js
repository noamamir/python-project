var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
    
});

io.on('connection', function(socket){
    console.log('a user connected');
    socket.on('start', function(data){
        console.log('Sending file' + data.fileName);
        io.emit('start', data);
    });
    socket.on('finish', function(){
        console.log('The wizard finished');
        io.emit('finish');
    });
    socket.on('send-scenario', function(){
        console.log('please send me some scenario...');
        io.emit('send-scenario');
    });
	socket.on('send-multiCastGroupUpdate', function(data){
        console.log('please send me some multiCastGroups...');
        io.emit('send-multiCastGroupUpdate', data);
    });
	socket.on('send-platformsUpdate', function(data){
        console.log('please send me some platforms...');
        io.emit('send-platformsUpdate', data);
    });
    socket.on('get-platformsUpdate', function(data){
        console.log('The methods: ' + data);
        io.emit('get-platformsUpdate', data);
    });
    socket.on('get-receiver-scenario', function(data){
        console.log('The methods: ' + data);
        io.emit('get-receiver-scenario', data);
    });
	socket.on('livelinessUpdate', function(data){
        console.log('The methods: ' + data);
        io.emit('livelinessUpdate', data);
    });
	socket.on('multicastgroup-stats', function(data){
        console.log('The methods: ' + data);
        io.emit('multicastgroup-stats', data);
    });
	socket.on('multicastGroup-update', function(data){
        console.log('The methods: ' + data);
        io.emit('multicastGroup-update', data);
    });
	socket.on('receieved-by-platforms-stats', function(data){
        console.log('The methods: ' + data);
        io.emit('receieved-by-platforms-stats', data);
    });
	socket.on('networks-update', function(data){
        console.log('The methods: ' + data);
        io.emit('networks-update', data);
    });
	socket.on('network-templates-update', function(data){
        console.log('The methods: ' + data);
        io.emit('network-templates-update', data);
    });
	socket.on('topology-update', function(data){
        console.log('The methods \"topology-update\": ' + data);
        io.emit('topology-update', data);
        //io.emit('topology-mivraka-update', data);
    });
	socket.on('topology-mivraka-update', function (data) {
		console.log('The methods \"topology-mivraka-update\": ' + data);
		io.emit('topology-mivraka-update', data);
	})
	socket.on('task-force-update', function(data){
        console.log('The methods \"task-force-update\": ' + data);
        io.emit('task-force-update', data);
    });
	socket.on('task-force-pending-update', function(data){
        console.log('The methods \"taskForce-pending-update\": ' + data);
        io.emit('task-force-pending-update', data);
    });
	socket.on('notification-update', function(data){
		console.log('The methods \"notification-update\": ' + data);
		io.emit('notification-update', data);
	});
	socket.on('wan-connection-params-update', function(data){
        console.log('The methods \"wan-connection-params-update\": ' + data);
        io.emit('wan-connection-params-update', data);
    });
	socket.on('wan-connection-update', function(data){
        console.log('The methods \"wan-connection-update\": ' + data);
        io.emit('wan-connection-update', data);
    });
	socket.on('disk-size', function(data){
        console.log('The methods: ' + data);
        io.emit('disk-size', data);
    });
	socket.on('dh-liveliness', function(data){
        console.log('The methods: ' + data);
        io.emit('dh-liveliness', data);
    });
	
	socket.on('channelsInfoUpdate', function(data){
        console.log('The methods: ' + data);
        io.emit('channelsInfoUpdate', data);
    });
	socket.on('time-update', function(data){
        io.emit('time-update', data);
    });
	socket.on('version-update', function(data){
        io.emit('version-update', data);
    });
	socket.on('serverAddress-update', function(data){
        io.emit('serverAddress-update', data);
    });
	socket.on('disconnect', function() {
		console.log('user disconnected');
		io.emit('refresh');
	});
	socket.on('uncaughtException', function(data) {
		console.log(data);
	});
	
	// Shkedia
	socket.on('shkd-liveliness', function(data) {
		io.emit('shkd-liveliness', data);
	});
	socket.on('shkd-new-physical-channel', function(data) {
		console.log(data);
		io.emit('shkd-new-physical-channel', data);
	});
	socket.on('shkd-physical-channel-disconnected', function(data) {
		console.log(data);
		io.emit('shkd-physical-channel-disconnected', data);
	});
	socket.on('shkd-physical-channel-users', function(data) {
		io.emit('shkd-physical-channel-users', data);
	});
	socket.on('shkd-physical-channel-status', function(data) {
		io.emit('shkd-physical-channel-status', data);
	});
	socket.on('shkd-logical-channels-change', function(data) {
		console.log("logical-channel-changed "+data);
		io.emit('shkd-logical-channels-change', data);
	});
	
	//mermail
	socket.on('Received', function(data) {
		console.log(data);
		io.emit('Received', data);
	});
	socket.on('Saved', function(data) {
		console.log(data);
		io.emit('Saved', data);
	});
	socket.on('Read', function(data) {
		console.log(data);
		io.emit('Read', data);
	});
	socket.on('Restored', function(data) {
		console.log(data);
		io.emit('Restored', data);
	});
	socket.on('Sent', function(data) {
		console.log(data);
		io.emit('Sent', data);
	});
	socket.on('Updated', function(data) {
		console.log(data);
		io.emit('Updated', data);
	});
	socket.on('Deleted', function(data) {
		console.log(data);
		io.emit('Deleted', data);
	});
	socket.on('PermanantDeleted', function(data) {
		console.log(data);
		io.emit('PermanantDeleted', data);
	});
	socket.on('Pending', function(data) {
		console.log(data);
		io.emit('Pending', data);
	});
	socket.on('channel-update', function(data) {
		console.log(data);
		io.emit('channel-update', data);
	});
	socket.on('channels-update', function(data) {
		console.log(data);
		io.emit('channels-update', data);
	});
	socket.on('logical-channels-update', function(data) {
		console.log(data);
		io.emit('logical-channels-update', data);
	});
	socket.on('shob-liveliness-change', function(data) {
		console.log(data);
		io.emit('shob-liveliness-change', data);
	});
	socket.on('wl-liveliness-change', function(data) {
		console.log(data);
		io.emit('wl-liveliness-change', data);
	});
	socket.on('update-shob-tx-policy', function(data) {
		console.log(data);
		io.emit('update-shob-tx-policy', data);
	});
	
	socket.on('station-update', function(data){
        console.log('The methods: ' + data);
        io.emit('station-update', data);
    });
	socket.on('system-state-update', function(data){
        io.emit('system-state-update', data);
    });
	
	socket.on('vhf-sending-tx-policy', function(data){
        io.emit('vhf-sending-tx-policy', data);
    });
	
	socket.on('vhf-modem-alert', function(data){
        io.emit('vhf-modem-alert', data);
    });

	socket.on('vhf-liveliness', function(data){
		io.emit('vhf-liveliness', data);
	});

	socket.on('shared-channel-changed', function(data){
		io.emit('shared-channel-changed', data);
	});

	socket.on('shared-inter-channel-changed', function(data){
		io.emit('shared-inter-channel-changed', data);
	});
});

http.listen(15006, "0.0.0.0", function(){

    console.log('listening on *:15006');
});

