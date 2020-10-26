<template>
  <el-container id="timetable">
    <el-header class="row-line show-height">
      <i class="el-icon-arrow-left fix-size" @click="getLastWeek"></i>
      <el-select class="text-center" v-model="newWeek">
        <el-option
          v-for="weekNum in weeksList"
          :key="weekNum"
          :label="'第'+weekNum+'周'"
          :value="weekNum"
        ></el-option>
      </el-select>
      <i class="el-icon-arrow-right fix-size" @click="getNextWeek"></i>
    </el-header>
    <el-main>
      <el-container>
        <el-header class="row-line show-height">
          <div class="main-header" v-for="(week, index) of weeks" :key="index">{{week}}</div>
        </el-header>
        <el-main>
          <timetable-body2 class="row-line" v-bind:newWeek="newWeek"></timetable-body2>
        </el-main>
      </el-container>
    </el-main>
  </el-container>
</template>

<script>
import TimetableBody2 from './TimetableBody2'
export default {
  name: 'timetable2',
  components: {
    TimetableBody2
  },
  data() {
    return {
      weeks: ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'],
      currWeek: Number,
      newWeek: Number,
      maxWeek: Number,
      minWeek: 1,
      weeksList: []
    }
  },
  methods: {
    getCurrWeek() {
      let room_id = this.$store.state.room_id
      this.$axios
        .post(
          '/students/get_curr_max_week',
          this.$Qs.stringify({ room_id: room_id })
        )
        .then(response => {
          let responseData = response.data
          if (responseData.code === this.$successCode) {
            this.currWeek = responseData.data.current_week //后期需要更改
            this.maxWeek = responseData.data.max_week
            this.newWeek = this.currWeek
            this.weeksList = Array.from({ length: this.maxWeek}, (v,k) => k + 1)
          } else {
            this.$message.error(responseData.msg)
          }
        })
        .catch(error => {
          this.$message.error(error)
        })
    },
    getLastWeek() {
      if (this.newWeek > this.minWeek) {
        let newWeek = this.newWeek - 1
        this.newWeek = newWeek
      } else {
        this.$message('当前周已经是本学期第一周')
      }
    },
    getNextWeek() {
      if (this.newWeek < this.maxWeek) {
        let newWeek = this.newWeek + 1
        this.newWeek = newWeek
      } else {
        this.$message('当前周已经是本学期最后一周')
      }
    }
  },
  created() {
    this.getCurrWeek()
  }
}
</script>

<style scoped>
#timetable {
  width: 42vw;
  height: 80vh;
  margin-top: 10px;
}
.main-header {
  border-bottom: 1px solid black;
  padding: 0;
  flex: auto;
  text-align: center;
}
.fix-size {
  font-size: 37px;
}
.row-line {
  display: flex;
  flex-direction: row;
}
.text-center {
  text-align: center;
  margin: 0 auto;
}
.show-height{
  height: 30px !important;
}
</style>
