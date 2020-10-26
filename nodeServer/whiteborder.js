const express = require('express')
const app = express()
const http = require('http').Server(app)
const io = require('socket.io')(http)
const port = 4110

app.use(express.static(__dirname + '/public'))

function onConnection(socket) {
  socket.on('drawing', (data) => socket.broadcast.emit('drawing', data))
  socket.on('clear', (data) => socket.broadcast.emit('clear', data))
  socket.on('drawRec', (data) => socket.broadcast.emit('drawRec', data))
  socket.on('select', (data) => socket.broadcast.emit('select', data))
}

io.on('connection', onConnection)

http.listen(port, () => console.log('listening on port ' + port))