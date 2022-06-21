
var http = require('http').createServer();
var io = require('socket.io')(http, {
    cors: {
        origin: "*",
    }
});

var redis = require('redis');

var redisClient = redis.createClient(6379, 'redis')

io.on('connection', function (socket){
    let userChannel = '';
    console.log('A user has connected...');
    socket.on('subscribe', function (userId) {
        userChannel = userId;
        console.log('subscription request ', userId);
        redisClient.subscribe(userId);
    });
    redisClient.on('message', function(channel, message){
        console.log('Channel ', channel);

        if (channel === userChannel){
            socket.emit('result', message);
        } 
    })
});

http.listen(3000, function (){
    console.log('Listening on port 3000 ..')
})

