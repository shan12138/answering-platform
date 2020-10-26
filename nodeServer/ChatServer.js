let express = require('express')
let app = express()
let http = require('http').Server(app)
// 思考：socket.io作为一个函数，当前http作为参数传入生成一个io对象？
// io-server
let io = require("socket.io")(http)
http.listen(4112, function () {
  console.log('listen 4113 port.')
})
let historyMsg = []
let roomUser = []

io.on('connection', function (socket) {
  let user = ''
  let roomid
  socket.on('join', function (data) {
    user = data.username
    roomid = data.roomid
    // 将用户归类到房间
    if (!roomUser[roomid]) {
      roomUser[roomid] = []
    }
    if (!historyMsg[roomid]) {
      historyMsg[roomid] = []
    }
    roomUser[roomid].push(user)
    socket.join(roomid)
    socket.to(roomid).emit('sys', user + '加入了房间')
    socket.emit('sys', user + '加入了房间')
    socket.emit('initMsg', { data: historyMsg[roomid] })
  })

  socket.on('releaseBan', function (msg) {
    io.sockets.emit('changeState', { data: msg })
  })

  socket.on('openBan', function (msg) {
    io.sockets.emit('changeState', { data: msg })
  })

  socket.on('sendStudentInfo', function (msg) {
    io.sockets.emit('insertStudent', { data: msg })
  })


  socket.on('sendMsg', function (msg) {
    if (!historyMsg[msg.roomid]) {
      historyMsg[msg.roomid] = []
    }
    historyMsg[msg.roomid].push(msg)
    socket.to(msg.roomid).emit('news', { data: msg })
  })

  socket.on('disconnect', function () {
    // 从房间名单中移除
    console.log('disconnection')
  })
})



