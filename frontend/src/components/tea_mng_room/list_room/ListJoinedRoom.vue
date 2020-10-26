<template>
  <div class="backgrand-blue">
    <p>您加入了{{roomList.length}}个房间</p>
    <el-row>
      <el-col v-for="room in roomList" :key="room.id" :span="5.9">
        <room-card v-bind:room="room"></room-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import RoomCard from './RoomCard'

export default {
  name: 'ListJoinedRoom',
  beforeCreate() {
    this.$axios
      .post(
        '/teachers/resolved_rooms',
        this.$Qs.stringify({
          user_id: this.$store.state.user_id
        })
      )
      .then(response => {
        this.roomList = response.data.data
      })
      .catch(err => {
        alert(err)
      })
  },
  data() {
    return {
      roomList: []
    }
  },
  components: {
    'room-card': RoomCard
  }
}
</script>

<style scoped>
.backgrand-blue {
  background: rgb(236, 210, 161);
}
p {
  text-align: center;
}
</style>