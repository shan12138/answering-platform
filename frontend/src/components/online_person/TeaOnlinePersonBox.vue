<template>
  <div class="chat">
    <div class="chat-area message">
      <ul style="padding: 0;">
        <li
          v-for="(onlinePerson, index) in onlinePersonList"
          :key="index"
          :class="onlinePerson.userState ? 'an-move-right' : 'an-move-left'"
        >
          <tea-each-person-mng :onlinePerson="onlinePerson"></tea-each-person-mng>
        </li>
      </ul>
    </div>
    <hr>
    <div class="input-area">
      <el-input v-model="input" placeholder="请输入内容" class="input"></el-input>
      <el-button type="primary" class="button" @click="search">搜索栏</el-button>
    </div>
  </div>
</template>

<script>
import TeaEachPersonMng from './TeaEachPersonMng'
import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

const SocketInstance = socketio('http://localhost:4117')

export default {
  name: 'PersonOne',
  data() {
    return {
      onlinePersonList: [],
      input: '',
      username: 'Jack',
      userid: 'JACK',
      roomid: 1,
      userState: false,   // true 表示禁言状态， false表示活跃状态
      userVeriry: false
    }
  },
  created() {
    let _this = this
    //教师加入直播间，
    SocketInstance.emit('join', {
      userid: _this.userid,
      userState: _this.userState,
      userVeriry: _this.userVeriry,
      roomid: _this.roomid
    })
    //教师初始化在线人数列表
    this.initOnlineList()
  },
  mounted() {
    this.initOnlineList()
  },
  methods: {
    search() {},
    initOnlineList() {
      let _this = this
      SocketInstance.on('initOnlineList', function(data) {
        let msg = data.data
        _this.onlinePersonList = []
        for (let i = 0; i < msg.length; i++) {
          _this.onlinePersonList.push({
            userid: msg[i].userid,
            userState: msg[i].userState,
            userVeriry: msg[i].userVeriry
          })
        }
      })
    },
    //插入人员
    insertUser() {
      let _this = this
      // 监听到有新人员加入后，触发该事件，向在线人数列表中追加新人员
      SocketInstance.on('insertStudent', function(data) {
        _this.onlinePersonList.push({
          userid: data.data.userid,
          userState: data.data.is_verify,
          userVeriry: data.data.user_state
        })
      })
    },
    getInitStudentList() {
      let form = new FormData()
      form.append('room_id', this.$store.state.room_id)
      this.$axios
        .post('/teachers/', form, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          let responseData = response.data
          let { code, msg } = responseData
          if (code === '0000') {
            this.onlinePersonList = msg.onlinePersonList
          } else {
            this.$message({
              message: msg,
              type: 'error'
            })
          }
        })
        .catch(error => {
          this.$message.error('加载用户数据失败！')
        })
    }
  },
  components: {
    TeaEachPersonMng
  }
}
</script>
<style scoped>
.chat {
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