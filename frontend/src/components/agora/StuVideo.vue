<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-card :body-style="{ padding: '5px' }">
          <tea-video-box/>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-card :body-style="{ padding: '5px' }">
          <stu-video-box/>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import TeaVideoBox from './stu_video_room/TeaVideoBox'
import StuVideoBox from './stu_video_room/StuVideoBox'
export default {
  data() {
    return {}
  },
  components: {
    TeaVideoBox,
    StuVideoBox
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 5px;
}
.el-col {
  border-radius: 4px;
}
</style>

