<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="4">
        <span>{{onlinePerson.userid}}</span>
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
  methods: {},
  mounted() {
    let _this = this
    SocketInstance.on('changeState', function(data) {
      if (data.data.userid === _this.userid) {
        _this.$message({
          showClose: true,
          message: '同学，你已经被禁言，有什么问题，请联系房间管理员'
        })
      }
    })
  }
}
</script>