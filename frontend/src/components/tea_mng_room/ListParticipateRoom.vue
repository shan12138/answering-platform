<template>
  <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
    <el-tab-pane label="我创建的房间" name="first">
      <list-self-room></list-self-room>
    </el-tab-pane>
    <el-tab-pane label="我加入的房间" name="second">
      <list-joined-room></list-joined-room>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import ListSelfRoom from './list_room/ListSelfRoom'
import ListJoinedRoom from './list_room/ListJoinedRoom'

export default {
  name: 'ListParticipateRoom',
  data() {
    return {
      activeName: 'first'
    }
  },
  methods: {
    handleClick(tab, event) {}
  },
  components: {
    'list-self-room': ListSelfRoom,
    'list-joined-room': ListJoinedRoom
  }
}
</script>

<style scoped>
</style>