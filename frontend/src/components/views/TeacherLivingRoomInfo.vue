<template>
  <el-container class="room-container">
    <el-main>
      <el-row>
        <el-col :span="4" :offset="3">
          <room-info v-bind:roomInfo="roomInfo"/>
        </el-col>
        <el-col :span="14" :offset="2">
          <timetable2/>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="14" :offset="4">
          <el-button id="join-btn" type="primary" @click="joinLivingRoom">加入直播间</el-button>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import Timetable2 from '../timetable/Timetable2'
import RoomInfo from '../room_introducte/RoomIntroduction'
export default {
  name: 'livingRoomInfo',
  components: {
    Timetable2,
    RoomInfo
  },
  data() {
    return {
      roomInfo: {},
      isPassword: true
    }
  },
  methods: {
    getLivingRoomInfo() {
      let requestData = {
        room_id: this.$store.state.room_id,
        user_id: this.$store.state.user_id
      }
      this.$axios
        .post('/students/search_room_info', this.$Qs.stringify(requestData))
        .then(response => {
          let responseData = response.data
          if (responseData.code === this.$successCode) {
            this.roomInfo = responseData.data.room_info
            this.isPassword = responseData.data.is_password
          } else {
            this.$message.error(responseData.msg)
          }
        })
        .catch(error => {
          this.$message.error(error)
        })
    },
    verification(password) {
      let requestData = {
        room_id: this.$store.state.room_id,
        password: password
      }
      this.$axios
        .post('/teachers/enter_password', this.$Qs.stringify(requestData))
        .then(response => {
          let responseData = response.data
          if (responseData.code === this.$successCode) {
            this.$message({
              type: 'success',
              message: '欢迎进入直播间'
            })
            this.$router.push('/teacher/livingRoom') //直播间页的路由
          } else {
            this.$message.error(responseData.msg)
          }
        })
        .catch(error => {
          this.$message.error(error)
        })
    },
    joinLivingRoom() {
      if (this.isPassword) {
        this.$prompt('请输入房间密码', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType: 'password',
          inputErrorMessage: '密码格式不正确',
          inputValidator(value) {
            if (value.length <= 10) {
              return true
            } else {
              return false
            }
          },
          beforeClose(action, instance, done) {
            if (action === 'confirm') {
              instance.confirmButtonLoading = true
              instance.confirmButtonText = '验证中...'
              setTimeout(() => {
                done()
                setTimeout(() => {
                  instance.confirmButtonLoading = false
                }, 100)
              }, 1000)
            } else {
              done()
            }
          }
        })
          .then(({ value }) => {
            this.verification(value)
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消输入'
            })
          })
      } else {
        this.$router.push('/teacher/livingRoom') //直播间页的路由
      }
    }
  },
  created() {
    this.getLivingRoomInfo()
  }
}
</script>

<style scoped>
#join-btn {
  width: 55vw;
}
</style>


