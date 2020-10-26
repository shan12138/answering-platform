<template>
  <div class="one-div">
    <canvas class="whiteboard"></canvas>

    <div class="colors">
      <el-color-picker v-model="color"></el-color-picker>
      <div
        :class="{tool:true, delete:true, 'black-background': isBlack, 'white-background': !isBlack}"
      ></div>
      <div
        :class="{tool:true, rectanger:true, 'blue-background': drawRec, 'white-background': !drawRec}"
      ></div>
    </div>
  </div>
</template>

<script>
import socketio from 'socket.io-client'
const SocketInstance = socketio('http://localhost:4110')
export default {
  name: 'Whiteboard',
  data() {
    return {
      isBlack: false,
      drawRec: false,
      CRASHCAN_NUM: 0,
      DRAW_REC: 1,
      color: '#111111',
      canvas: null,
      context: null,
      current: { color: 'black' },
      drawing: false
    }
  },
  mounted() {
    this.canvas = document.getElementsByClassName('whiteboard')[0]
    this.context = this.canvas.getContext('2d')

    // 鼠标点击画布的事件
    this.canvas.addEventListener('mousedown', this.onMouseDown, false)
    this.canvas.addEventListener('mouseup', this.onMouseUp, false)
    this.canvas.addEventListener('mouseout', this.onMouseUp, false)
    this.canvas.addEventListener(
      'mousemove',
      this.throttle(this.onMouseMove, 10),
      false
    )

    // 监听清除点击clear垃圾桶的事件
    let crashCan = document.getElementsByClassName('tool')[this.CRASHCAN_NUM]
    crashCan.addEventListener('mousedown', this.onReadyClear, false)
    crashCan.addEventListener('mouseup', this.onClear, false)

    // 监听是否画矩形的事件
    let drawRec = document.getElementsByClassName('tool')[this.DRAW_REC]
    drawRec.addEventListener('mouseup', this.onChangeDrawRec, false)

    // 同步其他client的drawing事件
    SocketInstance.on('drawing', this.onDrawingEvent)

    // 同步clear屏幕事件
    SocketInstance.on('clear', this.onClearEvent)

    // 同步绘制矩形的事件
    SocketInstance.on('drawRec', this.onDrawRecEvent)

    // 监听窗口大小改变事件
    window.addEventListener('resize', this.onResize, false)
    this.onResize()
  },
  methods: {
    onChangeDrawRec: function() {
      this.drawRec = !this.drawRec
    },

    onResize: function() {
      this.canvas.width = window.innerWidth * 0.7
      this.canvas.height = window.innerHeight * 0.6
    },

    onReadyClear: function() {
      this.isBlack = true
    },

    onClear: function() {
      this.isBlack = false
      this.onResize()
      SocketInstance.emit('clear', false)
    },

    onClearEvent: function() {
      this.onResize()
    },

    // 绘制直线
    drawLine: function(x0, y0, x1, y1, color, needEmit) {
      this.context.beginPath()
      this.context.moveTo(x0-100, y0-150)
      this.context.lineTo(x1-100, y1-150)
      this.context.strokeStyle = color
      this.context.lineWidth = 2
      this.context.stroke()
      this.context.closePath()

      if (!needEmit) {
        return
      }
      let w = this.canvas.width
      let h = this.canvas.height

      // 发布drawing事件
      SocketInstance.emit('drawing', {
        x0: x0 / w,
        y0: y0 / h,
        x1: x1 / w,
        y1: y1 / h,
        color: color
      })
    },

    // 绘制矩形
    drawRectang: function(x0, y0, x1, y1, color, needEmit) {
      this.context.fillStyle = color
      this.context.fillRect(x0-100, y0-150, x1 - x0, y1 - y0)
      if (!needEmit) {
        return
      }
      let w = this.canvas.width
      let h = this.canvas.height

      // 发布drawRec事件
      SocketInstance.emit('drawRec', {
        x0: x0 / w,
        y0: y0 / h,
        x1: x1 / w,
        y1: y1 / h,
        color: color
      })
    },

    onMouseDown: function(e) {
      if (this.drawRec && this.drawing) {
        return
      }
      this.current.x = e.clientX
      this.current.y = e.clientY
      this.drawing = true
    },

    onMouseUp: function(e) {
      if (!this.drawing) {
        return
      }
      this.drawing = false

      // 如果是需要绘制矩形
      if (this.drawRec) {
        this.drawRectang(
          this.current.x,
          this.current.y,
          e.clientX,
          e.clientY,
          this.color,
          true
        )
        return
      }

      this.drawLine(
        this.current.x,
        this.current.y,
        e.clientX,
        e.clientY,
        this.color,
        true
      )
    },

    onMouseMove: function(e) {
      if (!this.drawing) {
        return
      }
      if (this.drawRec) {
        this.drawRectang(
          this.current.x,
          this.current.y,
          e.clientX,
          e.clientY,
          this.color,
          true
        )
        return
      }
      this.drawLine(
        this.current.x,
        this.current.y,
        e.clientX,
        e.clientY,
        this.color,
        true
      )
      this.current.x = e.clientX
      this.current.y = e.clientY
    },

    onColorUpdate: function(e) {
      this.current.color = this.color
    },

    // limit the number of events per second
    throttle: function(callback, delay) {
      let previousCall = new Date().getTime()
      return function() {
        let time = new Date().getTime()

        if (time - previousCall >= delay) {
          previousCall = time
          callback.apply(null, arguments)
        }
      }
    },

    onDrawingEvent: function(data) {
      let w = this.canvas.width
      let h = this.canvas.height
      this.drawLine(
        data.x0 * w,
        data.y0 * h,
        data.x1 * w,
        data.y1 * h,
        data.color
      )
    },

    onDrawRecEvent: function(data) {
      let w = this.canvas.width
      let h = this.canvas.height
      this.drawRectang(
        data.x0 * w,
        data.y0 * h,
        data.x1 * w,
        data.y1 * h,
        data.color
      )
    }
  },
  watch: {}
}
</script>

<style scoped>
.one-div {
  height: 70vh;
  width: 56vw;
  margin: 0 auto;
  padding: 0;
}

.whiteboard {
  height: 70vh;
  width: 56vw;
  position: absolute;
  margin: 0 auto;
}

.colors {
  position: fixed;
}

.tool {
  display: inline-block;
  height: 48px;
  width: 48px;
}

.tool.delete {
  background-image: url(../../assets/trash-can.png);
  background-repeat: no-repeat;
  background-position: center;
}

.tool.rectanger {
  background-image: url(../../assets/rectanger.png);
  background-repeat: no-repeat;
  background-position: center;
}

.black-background {
  background-color: #555555;
}

.white-background {
  background-color: #ffffff;
}

.blue-background {
  background-color: #0ff8f0;
}

.color {
  display: inline-block;
  height: 48px;
  width: 48px;
}
</style>


