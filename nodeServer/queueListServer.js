const express = require('express')
const app = express()
const http = require('http').Server(app)
const io = require('socket.io')(http)
const port = 4111

app.use(express.static(__dirname + '/public'))

let queueList = []
function onConnection(socket) {
  socket.on('update', (data) => {
    queueList = data
    socket.broadcast.emit('update', data)
  })
  socket.on('getList', () => {
    socket.emit('update', queueList)
    io.sockets.emit('disable', queueList)
  })
  socket.on('switch', () => {
    queueList = queueList.slice(1)
    io.sockets.emit('update', queueList)
    io.sockets.emit('disable', queueList)
  })
  socket.on('joinQueue', student => {
    queueList.push(student)
    io.sockets.emit('update', queueList)
    io.sockets.emit('disable', queueList)
  })
}

io.on('connection', onConnection)

http.listen(port, () => console.log('listening on port ' + port))