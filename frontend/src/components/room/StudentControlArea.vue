<template>
  <el-card :body-style="{ padding: '5px' }">
    <el-row :gutter="20">
      <el-col :span="6" :offset="20">
        <el-button type="primary" @click="joinQueue" :disabled="isJoining">排队提问</el-button>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import socketio from 'socket.io-client'
const SocketInstance = socketio('http://localhost:4111')

export default {
  name: 'StudentControlArea',
  data() {
    return {
      isJoining: false
    }
  },
  computed: {
    isJoinIn: {
      get: function() {
        return this.isJoining
      }
    }
  },
  mounted() {
    let _this = this
    SocketInstance.on('update', list => {
      _this.isJoining = false
      for (let stu of list) {
        if (stu.id === _this.student.id) {
          _this.isJoining = true
        }
      }
    })
  },
  props: {
    student: {
      id: String,
      name: String
    }
  },
  methods: {
    joinQueue: function() {
      this.isJoining = true
      SocketInstance.emit('joinQueue', this.student)
    }
  }
}
</script>

<style scoped>
.el-row {
  margin-top: 10px;
}
</style>
