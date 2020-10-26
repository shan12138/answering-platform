<template>
  <el-row :gutter="8" id="livingroom">
    <el-col :span="18" id="display-video-editor-control">
      <el-row  id="display-video-editor" :gutter="10">
        <el-col :span="6" id="video">
          <tea-video/>
        </el-col>
        <el-col :span="18">
          <el-card shadow="always" id="editor" :body-style="{ padding: '10px' }">
            <editor-area/>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="24">
          <el-card shadow="always" id="control" :body-style="{ padding: '0px' }">
            <teacher-control-area/>
          </el-card>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="6">
      <el-card id="lists" :body-style="{ padding: '10px' }">
        <teacher-list-area/>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import TeacherListArea from '../room/TeacherListArea'
import EditorArea from '../room/EditorArea'
import TeacherControlArea from '../room/TeacherControlArea'
import TeaVideo from '../agora/TeaVideo'

export default {
  components: {
    TeacherListArea,
    EditorArea,
    TeacherControlArea,
    TeaVideo
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 10px;
}

.el-col {
  border-radius: 4px;
}

#livingroom {
  background-color: darkgrey;
}

#editor {
  background-color: white;
}
#video {
  background-color: white;
}
#control {
  background-color: white;
}
#lists {
  background-color: white;
}
</style>


