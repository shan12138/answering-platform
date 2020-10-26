<template>
  <div class="manage-position">
    <el-row>
      <el-col :span="12" :offset="16">
        <create-timetable/>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12" :offset="6">
        <modify-timetable/>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import CreateTimetable from './CreateTimetable'
import ModifyTimetable from './ModifyTimetable'
export default {
  name: 'manageTimetable',
  data() {
    return {}
  },
  components: {
    CreateTimetable,
    ModifyTimetable
  }
}
</script>

<style scoped>
.manage-position {
  margin: 20px auto;
}
</style>


