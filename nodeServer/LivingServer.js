let express = require('express')
let app = express()
let http = require('http').Server(app)
// io-server
let io = require("socket.io")(http)
http.listen(4115, function () {
  console.log('listen 4115 port.')
})

io.on('connection', function (socket) {

  let url = socket.request.headers.referer
  let split_arr = url.split('/')
  let roomid = split_arr[split_arr.length - 1] || 'index'
  let user = ''
  roomid = 1
  let roomUser = []
  socket.on('join', function (username) {
    user = username
    // 将用户归类到房间
    if (!roomUser[roomid]) {
      roomUser[roomid] = [];
    }
    roomUser[roomid].push(user);
    socket.join(roomid);
    socket.to(roomid).emit('sys', user + '加入了房间');
    socket.emit('sys', user + '加入了房间');
  })


  socket.on('sendOpenMsg', function (msg) {
    io.sockets.emit('openLive', { data: msg })
  })

  socket.on('sendCloseMsg', function (msg) {
    io.sockets.emit('closeLive', { data: msg })
  })
})



