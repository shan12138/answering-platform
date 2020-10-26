let express = require('express')
let app = express()
let http = require('http').Server(app)
// 思考：socket.io作为一个函数，当前http作为参数传入生成一个io对象？
// io-server
let io = require('socket.io')(http)
http.listen(4113, function () {
  console.log('listen 4113 port')
})

io.on('connection', function (socket) {
  let url = socket.request.headers.referer
  let split_arr = url.split('/')
  let roomid = split_arr[split_arr.length - 1] || 'index'
  let roomUser = []
  let user = ''
  roomid = 1

  socket.on('join', function (username) {
    user = username
    // 将用户归类到房间
    if (!roomUser[roomid]) {
      roomUser[roomid] = []
    }
    roomUser[roomid].push(user)
    socket.join(roomid)
    socket.to(roomid).emit('sys', user + '加入了房间')
    socket.emit('sys', user + '加入了房间')
  })

  socket.on('sendMsg', function (msg) {
    if (roomUser[roomid].indexOf(user) < 0) {
      return false
    }
    socket.broadcast.to(roomid).emit('news', { data: msg })
  })

  socket.on('disconnect', function () {
    // 从房间名单中移除
    socket.leave(roomid, function (err) {
      if (err) {
        console.log(err)
      }
    })
  })
})



