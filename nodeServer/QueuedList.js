let express = require('express')
let app = express()
let http = require('http').Server(app)
// io-server
let io = require('socket.io')(http)
http.listen(4117, function () {
  console.log('listen 4117 port.')
})
let onlinePersons = []

io.on('connection', function (socket) {
  let userid = 1
  let roomid = 1
  socket.on('join', function (data) {
    userid = data.userid
    roomid = data.roomid

    // 将用户归类到房间
    if (!onlinePersons[roomid]) {
      onlinePersons[roomid] = []
    }
    let tag = false
    for (let i = 0; i < onlinePersons[roomid].length; i++) {
      if (onlinePersons[roomid][i].userid === userid) {
        tag = true
      }
    }
    if (!tag) {
      onlinePersons[roomid].push(data)
    }
    io.sockets.emit('initOnlineList', { data: onlinePersons[roomid] })

    io.sockets.emit('insertStudent', { data: data })
    console.log(onlinePersons[roomid])
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

  socket.on('kikStudent', function (msg) {
    userid = msg.userid
    roomid = msg.roomid
    let index = -1
    for (let i = 0; i < onlinePersons[roomid].length; i++) {
      if (onlinePersons[roomid][i].userid === userid) {
        index = i
        break
      }
    }
    if (index !== -1) {
      onlinePersons[roomid].splice(index, 1)
    }
    io.sockets.emit('initOnlineList', { data: onlinePersons[roomid], userid: userid })
  })

  socket.on('disconnect', function () {
    // 从房间名单中移除
    console.log('disconnection')
  })
})



