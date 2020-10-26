<template>
  <el-row :gutter="8" id="livingroom">
    <el-col :span="18" id="display-video-editor-control">
      <el-row id="display-video-editor" :gutter="10">
        <el-col :span="6" id="video">
            <stu-video/>
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
            <student-control-area :student="student"/>
          </el-card>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="6">
      <el-card id="lists" :body-style="{ padding: '10px' }">
        <student-list-area/>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import StudentListArea from '../room/StudentListArea'
import StudentControlArea from '../room/StudentControlArea'
import EditorArea from '../room/EditorArea'
import TeacherControlArea from '../room/TeacherControlArea'
import StuVideo from '../agora/StuVideo'

import socketio from 'socket.io-client'
const SocketInstance = socketio('http://localhost:4111')

export default {
  data() {
    return {
      student: {
        id: '',
        name: ''
      },
      isConnector: false
    }
  },
  mounted() {
    this.$axios
      .post(
        '/students/get_student_id',
        this.$Qs.stringify({
          user_id: this.$store.state.user_id
        })
      )
      .then(response => {
        this.student.id = response.data.stuId
      })
      .catch(err => {
        alert(err)
      })
    this.$axios
      .post(
        '/students/get_name',
        this.$Qs.stringify({
          user_id: this.$store.state.user_id
        })
      )
      .then(response => {
        this.student.name = response.data.name
      })
      .catch(err => {
        alert(err)
      })

    let _this = this
    SocketInstance.on('disable', queueList => {
      if (queueList.length !== 0) {
        if (queueList[0].id === _this.student.id) {
          _this.isConnector = true
        }
      }
    })
  },
  components: {
    StudentListArea,
    StudentControlArea,
    EditorArea,
    TeacherControlArea,
    StuVideo
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
.disable {
  pointer-events: none;
}
</style>


