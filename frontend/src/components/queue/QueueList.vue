<template>
  <div id="queue-frame">
    <div
      class="queue"
      v-for="index in queueList.length"
      :key="index"
      :id="queueList[index-1].id"
      draggable="true"
      @dragstart="drag"
      @drop="drop"
      @dragover="allowDrop"
    >{{queueList[index-1].name}}</div>
  </div>
</template>

<script>
import socketio from 'socket.io-client'
const SocketInstance = socketio('http://localhost:4111')
export default {
  name: 'QueueList',
  data() {
    return {
      queueList: [
        { id: '2016215158', name: '徐书林' },
        { id: '2016215153', name: '徐书林1' },
        { id: '2016215159', name: '徐书林2' },
        { id: '2016215154', name: '徐书林3' }
      ]
    }
  },
  created() {
    SocketInstance.on('update', list => {
      this.queueList = list
    })
  },
  mounted() {
    SocketInstance.emit('getList')
  },
  methods: {
    allowDrop: function(ev) {
      ev.preventDefault()
    },

    drag: function(ev) {
      ev.dataTransfer.setData('student', ev.target.id)
    },

    drop: function(ev) {
      ev.preventDefault()
      let data = ev.dataTransfer.getData('student')
      // 拖放元素
      document
        .getElementById('queue-frame')
        .insertBefore(document.getElementById(data), ev.target)

      // 获取当前元素列表
      let list = document.getElementsByClassName('queue')

      // 重置queueList
      for (let index = 0; index < list.length; ++index) {
        this.queueList[index] = {
          id: list[index].id,
          name: list[index].innerHTML
        }
      }

      // 发送更新数据
      SocketInstance.emit('update', this.queueList)
    }
  }
}
</script>

<style scoped>
.queue {
  border-bottom: 1px solid black;
  padding-bottom: 3px;
  min-height: 10px;
  width: 19vw;
  text-overflow: ellipsis;
  margin: 0 auto;
}
</style>
