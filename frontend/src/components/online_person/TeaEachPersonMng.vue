<template>
  <div class="item-line show-border">
    <el-row :gutter="10">
      <el-col :span="4">
        <span>{{userid}}</span>
      </el-col>
      <el-col :span="2" :offset="9">
        <el-tooltip class="item" effect="dark" content="踢除学生" placement="top">
          <el-button type="info" size="mini" @click="KikStudent" circle>
            <i class="kik-icon"></i>
          </el-button>
        </el-tooltip>
      </el-col>
      <el-col :span="2" :offset="2">
        <div v-if="userVeriry">
          <el-tooltip class="item" effect="dark" content="取消认证" placement="top">
            <el-button type="danger" size="mini" @click="verifyStudent" circle></el-button>
          </el-tooltip>
        </div>
        <div v-else>
          <el-tooltip class="item" effect="dark" content="认证学生" placement="top">
            <el-button type="success" size="mini" @click="cancleAuth" circle></el-button>
          </el-tooltip>
        </div>
      </el-col>
      <el-col :span="2" :offset="2">
        <div v-if="userState">
          <el-tooltip class="item" effect="dark" content="开启禁言" placement="top">
            <el-button type="danger" size="mini" @click="openBan" circle></el-button>
          </el-tooltip>
        </div>
        <div v-else>
          <el-tooltip class="item" effect="dark" content="解除禁言" placement="top">
            <el-button type="success" size="mini" @click="releaseBan" circle></el-button>
          </el-tooltip>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

const SocketInstance = socketio('http://localhost:4117')
export default {
  data() {
    return {
      name: '',
      userVeriry: Boolean,
      userState: Boolean,
      userid: String,
      roomid: 1
    }
  },
  props: ['onlinePerson'],
  created() {
    this.roomid = this.$store.state.room_id
  },
  methods: {
    releaseBan: function() {
      this.userState = !this.userState
      SocketInstance.emit('releaseBan', {
        userid: this.userid
      })
      let form = new FormData()
      form.append('userid', this.userid)
      this.$axios
        .post('/students/', form, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          let responseData = response.data
          let { token, user_id, username, code } = responseData
          if (code === '0000') {
            this.$router.push({ path: './student/home' })
          } else {
            this.$message({
              message: msg,
              type: 'error'
            })
          }
        })
        .catch(error => {})
    },
    openBan: function() {
      this.userState = !this.userState
      SocketInstance.emit('openBan', {
        userid: this.userid
      })

      let form = new FormData()
      form.append('userid', this.userid)
      this.$axios
        .post('/students/', form, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          let responseData = response.data
          let { token, user_id, username, code } = responseData
          if (code === '0000') {
            this.$router.push({ path: './student/home' })
          } else {
            this.$message({
              message: msg,
              type: 'error'
            })
          }
        })
        .catch(error => {})
    },
    verifyStudent: function() {
      this.userVeriry = !this.userVeriry
      this.$axios
        .post(
          '/teachers/confirm_students',
          this.$Qs.stringify({
            name: this.userid,
            room_id: this.roomid
          })
        )
        .then(response => {
          let responseData = response.data
          let { code, msg, data } = responseData
          if (code === '0000') {
            this.$message({
              type: 'info',
              message: msg
            })
          } else {
            this.$message.error(msg)
          }
        })
        .catch(error => {
          this.$message.error('数据请求失败，请重试！')
        })
    },
    cancleAuth: function() {
      this.userVeriry = !this.userVeriry
      this.$axios.post(
        '/teachers/cancel_confirm_students',
        this.$Qs.stringify({
          name: this.userid,
          room_id : this.roomid
        })
      )
      .then(response => {
        let responseData = response.data
          let { code, msg, data } = responseData
          if (code === '0000') {
            this.$message({
              type: 'info',
              message: msg
            })
          } else {
            this.$message.error(msg)
          }
      })
      .catch(error => {
        this.$message.error('数据请求失败，请重试！')
      })
    },
    getInfo() {
      let onlinePerson = this.onlinePerson
      this.userVeriry = onlinePerson.userVeriry
      this.userState = onlinePerson.userState
      this.userid = onlinePerson.userid
    },
    KikStudent() {
      SocketInstance.emit('kikStudent', {
        userid: this.userid,
        roomid: this.roomid
      })
    }
  },
  watch: {
    onlinePerson() {
      this.getInfo()
    }
  },
  beforeMount() {
    this.getInfo()
  },
  mounted() {},
  components: {}
}
</script>

<style scoped>
.show-border {
  padding-bottom: 10px;
  border-bottom: 1px solid black;
}
.kik-icon {
  background-image: url(..\..\assets\kik.png);
}
</style>