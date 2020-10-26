<template>
  <el-col :span="24">
    <el-table :data="courses" :span-method="paintTable" id="timetable" empty-text="暂无课程" border>
      <el-table-column prop="Mon" label="周一"></el-table-column>
      <el-table-column prop="Tues" label="周二"></el-table-column>
      <el-table-column prop="Wed" label="周三"></el-table-column>
      <el-table-column prop="Thur" label="周四"></el-table-column>
      <el-table-column prop="Fri" label="周五"></el-table-column>
      <el-table-column prop="Sat" label="周六"></el-table-column>
      <el-table-column prop="Sun" label="周日"></el-table-column>
    </el-table>
  </el-col>
</template>

<script>
export default {
  props: ['week'],
  name: 'timetable',
  data() {
    const startTime = '00:00'
    return {
      newWeek: this.week,
      lastTime: Array(7).fill(startTime),
      originCourses: [],
      courses: [{ Mon: '1' }], // 12 的数据表格
      weeks: ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'],
      spanQueue: []
    }
  },
  methods: {
    updateTimetable() {
      let _this = this
      // 请求数据更新课表
      this.$axios
        .post('/students/signup', this.$Qs.stringify({ week: _this.newWeek }))
        .then(response => {
          let responseData = response.data
          if (responseData.code === '0000') {
            this.originCourses = responseData.data.courses
          } else {
            this.$message.error(responseData.msg)
          }
        })
        .catch(error => {
          this.$message.error('请求异常请重试！')
        })
    },
    initSpanQueue() {
      let spanQueue = Array(12 * 7).fill(0)
      for (let i = 0; i < 7; i++) {
        spanQueue[i] = 12
      }
      this.spanQueue = spanQueue
    },
    convertMinute(time) {
      let timeList = time.split(':')
      let hour = parseInt(timeList[0])
      let minutes = parseInt(timeList[1])
      return hour * 60 + minutes
    },
    // 生成显示课表
    initCourses(courses) {
      for (let course of courses) {
        let week = parseInt(course.week) - 1
        let weekStr = this.weeks[week] //获取key
        //生成占位格数据
        let interval = this.computeRowspan(
          this.lastTime[week],
          course.open_time
        )
        if (interval !== 0) {
          this.createIntervalItem(week, interval, weekStr, this.lastTime[week])
        }
        // 生成数据格数据
        this.lastTime[week] = course.open_time
        this.createDataItem(week, weekStr, course.open_time, course.end_time)
      }
    },
    fillInterval(rowSpan, position) {
      this.spanQueue[position + 7] = 12 - rowSpan
    },
    createDataItem(week, weekStr, startTime, endTime) {
      let rowSpan = this.computeRowspan(startTime, endTime)
      let startRow = this.getstartRow(startTime)
      let weekObj = this.courses[startRow]
      if (weekObj === undefined) {
        weekObj = {}
      }
      weekObj[weekStr] = startTime + '~' + endTime
      this.courses[startRow] = weekObj
      let position = 0
      if (week === 0) {
        position = startRow
      } else if (startRow === 0) {
        position = week
      } else {
        position = startRow * 7 + week
      }
      this.spanQueue[position] = rowSpan
      this.fillInterval(rowSpan, position)
    },
    createIntervalItem(week, interval, weekStr, startTime) {
      let startRow = this.getstartRow(startTime)
      let weekObj = this.courses[startRow]
      if (weekObj === undefined) {
        weekObj = {}
      }
      weekObj[weekStr] = ''
      this.courses[startRow] = weekObj
      if (week === 0) {
        this.spanQueue[startRow] = interval
      } else if (startRow === 0) {
        this.spanQueue[week] = interval
      } else {
        let position = startRow * 7 + week
        this.spanQueue[position] = interval
      }
    },
    getstartRow(startTime) {
      let _this = this
      let convertHour = _this.convertMinute(startTime) / (60 * 2)
      return Math.round(convertHour)
    },
    computeRowspan(startTime, endTime) {
      let spend = this.convertMinute(endTime) - this.convertMinute(startTime)
      let rowSpan = Math.round(spend / (60 * 2))
      return rowSpan
    },
    expendCourses() {
      for (let i = 0; i < 12; i++) {
        if (this.courses[i] === undefined) {
          this.courses[i] = {}
        }
      }
    },
    paintTable({ row, column, rowIndex, columnIndex }) {
      let rowSpanIndex = 0
      if (rowIndex === 0) {
        rowSpanIndex = columnIndex
      } else if (columnIndex === 0) {
        rowSpanIndex = rowIndex * 7
      } else {
        rowSpanIndex = rowIndex * 7 + columnIndex
      }
      let rowSpan = this.spanQueue[rowSpanIndex]
      let colSpan = 1
      return [rowSpan, colSpan]
    }
  },
  watch: {
    week() {
      this.newWeek = this.week
      this.initSpanQueue()
      this.updateTimetable()
    },
    originCourses() {
      if (this.originCourses !== []) {
        this.initCourses(this.originCourses)
        this.spanQueue.reverse()
        this.expendCourses()
      }
    }
  },
  beforeMount() {
    this.initSpanQueue()
    this.updateTimetable()
  }
}
</script>

<style scoped>
#timetable {
  margin-top: 20px;
  min-height: 300px;
}
</style>
