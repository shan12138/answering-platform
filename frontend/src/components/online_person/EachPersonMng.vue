<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="4">
        <span>{{onlinePerson.userid}}</span>
      </el-col>
      <el-col :span="3" :offset="7">
        <el-button type="success" size="mini" @click="KikStudent" circle>踢除学生</el-button>
      </el-col>
      <el-col :span="3" :offset="4">
        <el-button type="success" size="mini" @click="verifyStudent" circle>认证学生</el-button>
      </el-col>
      <el-col :span="3" :offset="4" circle>
        <div v-if="onlinePerson.userState">
          <el-button type="danger" size="mini" @click="openBan" circle>开启禁言</el-button>
        </div>
        <div v-else>
          <el-button type="success" size="mini" @click="releaseBan" circle>解除禁言</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

const SocketInstance = socketio('http://localhost:4113')
export default {
  data() {
    return {
      name: '真实'
    }
  },
  props: ['onlinePerson'],
  methods: {
    releaseBan: function() {
      this.onlinePerson.userState = !this.onlinePerson.userState
    },
    openBan: function() {
      this.onlinePerson.userState = !this.onlinePerson.userState
    }
  },

  mounted() {
    let _this = this
    SocketInstance.on('changeState', function(data) {
      if (data.data.userid === _this.onlinePerson.userid) {
      }

      let pos = data.data.username === _this.username
      _this.chatMsgList.push({
        username: data.data.username,
        content: data.data.content,
        pos: pos
      })
    })
  }
}
</script>
