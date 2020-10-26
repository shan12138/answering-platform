<template>
  <div class="chat">
    <div class="chat-area message">
      <ul style="padding: 0;">
        <li
          v-for="(chatMsg, index) in chatMsgList"
          :key="index"
          :class="chatMsg.pos ? 'an-move-right' : 'an-move-left'"
        >
          <chat-block :chatMsg="chatMsg"></chat-block>
        </li>
      </ul>
    </div>
    <hr>
    <div class="input-area">
      <el-input v-model="input" placeholder="请输入内容" class="input"></el-input>
      <el-button type="primary" class="button" @click="sendMsg">发送</el-button>
    </div>
  </div>
</template>

<script>
import ChatBlock from './ChatBlock'
import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

const SocketInstance = socketio('http://localhost:4113')

export default {
  name: 'PersonOne',
  mounted() {
    let _this = this
    SocketInstance.on('news', function(data) {
      let pos = data.data.username === _this.username
      _this.chatMsgList.push({
        username: data.data.username,
        content: data.data.content,
        pos: pos
      })
    })
  },
  created() {
    let _this = this
    SocketInstance.emit('join', {
      username: this.username,
      roomid: this.roomid
    })
    SocketInstance.on('initMsg', function(data) {
      let msg = data.data
      for (let i = 0; i < msg.length; i++) {
        msg[i].pos = msg[i].username === _this.username
        _this.chatMsgList.push(msg[i])
      }
    })
  },
  data() {
    return {
      chatMsgList: [],
      input: '',
      username: 'Jack',
      roomid: '111',
      userState: false // true 表示禁言状态， false表示活跃状态
    }
  },
  methods: {
    sendMsg() {
      if (this.input === '') {
      } else {
        this.chatMsgList.push({
          username: this.username,
          content: this.input,
          roomid: this.roomid,
          pos: true
        })
        SocketInstance.emit('sendMsg', {
          username: this.username,
          content: this.input,
          roomid: this.roomid,
          pos: false
        })
        this.input = ''
      }
    }
  },
  components: {
    ChatBlock
  }
}
</script>
<style scoped>
.chat {
  /* position: absolute; */
  border: none !important;
  width: 22vw;
  height: 92vh;
  border: 1px solid black;
  margin: 0 auto;
}

.chat-area {
  max-height: 600px;
  height: 78vh;
  margin: 0 auto;
  overflow: auto;
  overflow-x: hidden;
  padding: 0;
}

.message {
  padding: 10px 10px;
}
.message li {
  margin-bottom: 15px;
  left: 0;
  position: relative;
  display: block;
}

.input-area {
  padding: 5px;
  display: inline;
}

.input {
  padding: 5px;
  margin: 5px 20px 5px 5px;
  width: 200px;
}

.an-move-left {
  left: 0;
  animation: moveLeft 0.7s ease;
  -webkit-animation: moveLeft 0.7s ease;
}
.an-move-right {
  left: 0;
  animation: moveRight 0.7s ease;
  -webkit-animation: moveRight 0.7s ease;
}
</style>