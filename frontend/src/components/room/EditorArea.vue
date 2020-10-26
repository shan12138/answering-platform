<template>
  <el-tabs id="editor-area" v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="代码编辑器" name="codeeditor">
      <code-editor/>
    </el-tab-pane>
    <el-tab-pane label="白板" name="whiteboard">
      <whiteboard/>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import CodeEditor from '../code_editor/CodeEditor'
import Whiteboard from '../whiteboard/Whiteboard'
import socketio from 'socket.io-client'
const SocketInstance = socketio('http://localhost:4110')
export default {
  name: 'editorArea',
  components: {
    CodeEditor,
    Whiteboard
  },
  data() {
    return {
      activeName: 'codeeditor'
    }
  },
  mounted() {
    let _this = this
    SocketInstance.on('select', (data) => {
      _this.activeName = data
    })
  },
  methods: {
    handleClick(tab, event) {
      SocketInstance.emit('select', tab.name)
    },
  }
}
</script>

<style scoped>
#editor-area {
  height: 70vh;
  width: 56vw;
}
</style>

