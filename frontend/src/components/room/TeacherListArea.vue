<template>
  <el-tabs id="list-area" v-model="switchList" type="card" @tab-click="handleClick">
    <el-tab-pane label="提问序列" name="question-list">
      <queue-list/>
    </el-tab-pane>
    <el-tab-pane label="当前在线人数" name="online-list">
      <tea-online-person-box/>
    </el-tab-pane>
    <el-tab-pane label="聊天列表" name="chat-list">
      <chat/>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import Chat from '../student/Chat'
import TeaOnlinePersonBox from '../online_person/TeaOnlinePersonBox'
import QueueList from '../queue/QueueList'

export default {
  name: 'listArea',
  components: {
    Chat,
    TeaOnlinePersonBox,
    QueueList
  },
  data() {
    return {
      switchList: 'online-list'
    }
  },
  methods: {
    handleClick() {}
  }
}
</script>

<style scoped>
#list-area {
  height: 80.5vh;
}
</style>

