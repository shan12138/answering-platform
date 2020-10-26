<template>
  <div>
    <time-table-header v-bind:currWeek="currWeek"></time-table-header>
    <router-view/>
  </div>
</template>

<script>
import TimeTableHeader from './TimetableHeader'
export default {
  name: 'timetable',
  data() {
    return {
      currWeek: 1
    }
  },
  components: { TimeTableHeader },
  beforeCreate() {
    //获取当前周的课表信息
    let user_id = this.$store.state.user_id
    this.$axios
      .post('/host/students/', this.$Qs.stringify({ user_id: user_id }))
      .then(response => {
        let responseData = response.data
        if (responseData.code === this.$successCode) {
          let timeData = responseData.data
          this.currWeek = parseInt(timeData.currweek)
        } else {
          this.$message.error(responseData.msg)
        }
      })
      .catch(error => {
        this.$message.error('数据请求失败,请重试！')
      })
  }
}
</script>
