<template>
  <el-container class="code-editor">
    <el-header id="select-header">
      <el-select v-model="mode" id="header-item" filterable placeholder="请选择">
        <el-option
          v-for="(language, index) in languageArray"
          :key="index"
          :label="language.label"
          :value="language.value"
        ></el-option>
      </el-select>
    </el-header>
    <textarea ref="code" id="editor" v-model="code"></textarea>
  </el-container>
</template>

<script>
import CodeMirror from 'codemirror/lib/codemirror' // CodeMirror，必要
import 'codemirror/lib/codemirror.css' // css，必要
import 'codemirror/mode/javascript/javascript' // js的语法高亮，自行替换为你需要的语言
import 'codemirror/mode/python/python'
import 'codemirror/mode/javascript/javascript'
import 'codemirror/mode/clike/clike'
import 'codemirror/mode/go/go'
import 'codemirror/mode/htmlmixed/htmlmixed'
import 'codemirror/mode/http/http'
import 'codemirror/mode/php/php'
import 'codemirror/mode/http/http'
import 'codemirror/mode/sql/sql'
import 'codemirror/mode/vue/vue'
import 'codemirror/mode/xml/xml'
import 'codemirror/theme/monokai.css'
import 'codemirror/addon/scroll/simplescrollbars.css'
import 'codemirror/addon/scroll/simplescrollbars'
import 'codemirror/mode/meta'

import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

const SocketInstance = socketio('http://localhost:4113')

export default {
  name: 'codeMirror',
  data() {
    return {
      code: '',
      mode: 'python',
      languageArray: [
        { value: 'javascript', label: 'javascript' },
        { value: 'python', label: 'python' }
      ],
      editor: null,
      username: 'Jack',
      package: { username: this.username, dataObj: null },
      tag: true
    }
  },
  methods: {
    configCodeMirror() {
      this.editor = CodeMirror.fromTextArea(this.$refs.code, {
        mode: 'python', //选择对应代码编辑器的语言
        theme: 'monokai',
        indentWithTabs: true,
        smartIndent: true,
        scrollbarStyle: 'simple',
        indentUnit: 2,
        tabSize: 4,
        lineNumbers: true,
        matchBrackets: true,
        autofocus: true,
        extraKeys: { Ctrl: 'autocomplete' }, //自定义快捷键
        tag: true
      })
      this.editor.on(
        'change',
        (codeMirror, { from, to, text, removed, origin }) => {
          if (origin !== undefined) {
            SocketInstance.emit('sendMsg', {
              from: from,
              to: to,
              text: text,
              removed: removed,
              origin: origin
            })
          }
        }
      )
    }
  },
  watch: {
    mode() {
      this.editor.setOption('mode', this.mode)
    }
  },
  created() {
    SocketInstance.emit('join', this.username)
  },
  mounted() {
    //配置codeMirror
    this.configCodeMirror()
    let _this = this
    SocketInstance.on('news', function(data) {
      let newData = data.data
      let text = newData.text.join('\t\n')
      _this.editor.replaceRange(text, newData.from, newData.to)
      _this.tag = false
    })
  }
}
</script>

<style>
.code-editor {
  border: 1px solid black;
  height: 65vh;
  width: 56vw;
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
#header-item {
  width: 20vw;
}
#select-header {
  height: 40px !important;
}
.CodeMirror {
  height: 90vh;
}
.el-select {
  float: right;
}
</style>
