<template>
  <div class="timetable-body">
    <div class="row-line" v-if="originCourses.length !== 0">
      <div 
        class="timetable-body-item" 
        v-for="col of column" 
        :key="col">
        <date
          v-for="(dateItem, index) of courses[col]"
          :key="index"
          v-bind:class="[dateItem.isColor ? 'color-blue' : 'color-grey']"
          v-bind:dateInfo="dateItem"
        ></date>
      </div>
    </div>
    <div class="empty-timetable" v-else>
      <p>本周暂无安排</p>
    </div>
  </div>
</template>

<script>
import Date from './Date'
export default {
  props: ['newWeek'],
  name: 'timetableBody',
  components: {
    Date
  },
  data() {
    return {
      maxHeight: 400,
      originCourses: [],
      courses: [],
      percentHeight: 0.0,
      column: [],
      lastTime: []
    }
  },
  methods: {
    initData() {
      const startTime = '00:00'
      let lastTime = Array(7).fill(startTime)
      this.lastTime = lastTime
      this.courses = []
    },
    getData(week) {
      let requestData = {
        room_id: this.$store.state.room_id,
        week: week
      }
      this.$axios
        .post('/students/list_room_calendar', this.$Qs.stringify(requestData))
        .then(response => {
          let requestData = response.data
          if (requestData.code === this.$successCode) {
            this.originCourses = requestData.data
            this.courses = this.dealData(this.originCourses)
          } else {
            _this.$message.error(responseData.msg)
          }
        })
        .catch(error => {
          this.$message.error(error)
        })
    },
    dealData(originCourses) {
      let courses = []
      const night = '24:00'
      for (let course of originCourses) {
        let week = parseInt(course.day) - 1
        if (courses[week] === undefined) {
          courses[week] = []
        } else {
          courses[week].pop()
        }
        courses[week].push(
          this.spaceDataItem(this.lastTime[week], course.open_time)
        )
        this.lastTime[week] = course.open_time
        courses[week].push(this.realDataItem(course))
        this.lastTime[week] = course.end_time
        courses[week].push(this.spaceDataItem(this.lastTime[week], night))
      }
      let fillCourses = this.fillCourses(courses)
      return fillCourses
    },
    spaceDataItem(startTime, endTime) {
      const isColor = false
      let interval = this.computedHeight(startTime, endTime)
      const time = ''
      return { isColor: isColor, interval: interval, time: time }
    },
    realDataItem(course) {
      const isColor = true
      let interval = this.computedHeight(course.open_time, course.end_time)
      let time = course.open_time + '~' + course.end_time
      return { isColor: isColor, interval: interval, time: time }
    },
    computedHeight(startTime, endTime) {
      let startList = startTime.split(':')
      let endList = endTime.split(':')
      let startMinutes = parseInt(startList[0]) * 60 + parseInt(startList[1])
      let endMinutes = parseInt(endList[0]) * 60 + parseInt(endList[1])
      let livingTime = (endMinutes - startMinutes) / 60
      let height = livingTime * this.percentHeight
      let finalHeight = Math.round(height)
      if (finalHeight == 0) {
        finalHeight = 1
      }
      return finalHeight
    },
    fillCourses(courses) {
      let date = { isColor: false, interval: this.maxHeight, time: '' }
      for (let index = 0; index < 7; index++) {
        if (courses[index] === undefined) {
          courses[index] = [date]
        }
      }
      return courses
    }
  },
  watch: {
    newWeek() {
      this.initData()
      this.getData(this.newWeek)
    }
  },
  created() {
    this.percentHeight = this.maxHeight / 24
    this.column = Array.from({ length: 7 }, (v, k) => k)
  }
}
</script>

<style scoped>
.timetable-body {
  height: 400px;
  border-width: 0;
}
.timetable-body-item {
  flex: auto;
  width: 50px;
  word-wrap:break-word ;
  border: 1px solid #898a8b;
}
.row-line {
  width: 550px;
  display: flex;
  flex-direction: row;
}
.color-blue {
  background-color: #409EFF;
}
.color-grey {
  background-color: #F3F3F4;
}
.empty-timetable{
  width: 550px;
  background-color: #F3F3F4;
  text-align: center; 
}
</style>
