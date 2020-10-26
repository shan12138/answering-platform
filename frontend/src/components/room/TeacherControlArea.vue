<template>
  <el-card :body-style="{ padding: '5px' }">
    <el-row :gutter="3">
      <el-col :span="4">
        <el-button type="success" @click="startLiving">开启直播</el-button>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="sendLiving">发送直播</el-button>
      </el-col>
      <el-col :span="4">
        <el-button type="info" @click="pauseLiving">暂停直播</el-button>
      </el-col>
      <el-col :span="4">
        <el-button type="danger" @click="hangLiving">挂断当前学生</el-button>
      </el-col>
      <el-col :span="4">
        <el-button type="danger" @click="switchLiving">切换当前的学生</el-button>
      </el-col>
      <el-col :span="4">
        <el-button type="danger" @click="stopLiving">关闭直播</el-button>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import bus from '../../assets/eventsBus.js'
import socketio from 'socket.io-client'
const SocketInstance = socketio('http://localhost:4111')

export default {
  name: 'controlArea',
  methods: {
    startLiving: function() {
      bus.$emit('startLiving', 'start')
    },
    sendLiving: function() {
      bus.$emit('sendLiving', 'send')
    },
    pauseLiving: function() {
      bus.$emit('pauseLiving', 'pause')
    },
    hangLiving: function() {
      bus.$emit('hangLiving', 'hang')
    },
    switchLiving: function() {
      bus.$emit('switchLiving', 'switch')
      SocketInstance.emit('switch', null)
    },
    stopLiving: function() {
      bus.$emit('stopLiving', 'stop')
    }
  }
}
</script>

<style scoped>
.el-row {
  margin-top: 10px;
}
</style>

