<template>
  <el-container id="room-introduce">
    <el-header>
      <h4 id="text-center">房间信息介绍</h4>
    </el-header>
    <el-main>
      <el-row>
        <el-form>
          <el-form-item label="课程标题: ">
            <div name="title">{{roomInfo.title}}</div>
          </el-form-item>
          <el-form-item label="开课人名称: ">
            <div name="teacher-name">{{roomInfo.teacher_name}}</div>
          </el-form-item>
          <el-form-item label="开课学院: ">
            <div name="college">{{roomInfo.college}}</div>
          </el-form-item>
          <el-form-item label="课程描述: ">
            <div name="description">{{roomInfo.description}}</div>
          </el-form-item>
        </el-form>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  props: {
    roomInfo: {
      title: String,
      teacherName: String,
      college: String,
      description: String
    }
  },
  name: 'roomIntroduction'
}
</script>

<style scoped>
.el-form-item__label {
  /* 字体加粗 */
  font-weight: bold !important;
}
#text-center {
  text-align: center;
}
#room-introduce {
  border: 1px solid black;
  margin: 40px auto;
}
</style>


