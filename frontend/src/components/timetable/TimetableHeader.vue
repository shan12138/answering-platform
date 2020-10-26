<template>
  <el-row id="timetable-header">
    <el-col :span="1" :offset="7" id="left-btn">
      <el-button type="primary" @click="lastWeek">
        <i class="el-icon-arrow-left"></i>
      </el-button>
    </el-col>
    <el-col :span="5" id="show-week">
      <el-input :readonly="true" v-bind:value="'第'+newWeek+'周'"></el-input>
    </el-col>
    <el-col :span="1">
      <el-button type="primary" @click="nextWeek">
        <i class="el-icon-arrow-right el-icon--right"></i>
      </el-button>
    </el-col>
  </el-row>
</template>

<script>
//路由跳转问题，重新渲染子组件
export default {
  props: ['currWeek'],
  name: 'timetableHeader',
  data() {
    return {
      minWeek: 1,
      maxWeek: 20, //后期获得
      newWeek: 1,
      isUpBtn: true,
      isDownBtn: true
    }
  },
  methods: {
    lastWeek() {
      let week = this.newWeek
      if (week > this.minWeek) {
        this.newWeek = week - 1
        if (this.isDownBtn === false) {
          this.isDownBtn = true
        }
      } else {
        this.isUpBtn = false
      }
    },
    nextWeek() {
      let week = this.newWeek
      if (week < this.maxWeek) {
        this.newWeek = week + 1
        if (this.isUpBtn === false) {
          this.isUpBtn = true
        }
      } else {
        this.isDownBtn = false
      }
    }
  },
  watch: {
    newWeek() {
      this.$router.replace(`/timetable/${this.newWeek}`)
    },
    currWeek() {
      this.newWeek = this.currWeek
      this.$router.replace(`/timetable/${this.currWeek}`)
    }
  }
}
</script>

<style scoped>
#left-btn {
  padding-left: 8px;
}
</style>