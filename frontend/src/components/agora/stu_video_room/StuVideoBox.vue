<template>
  <div>
    <div class="livepart">
      <div id="video" class="video-part" style="margin:0 auto;">
        <el-col :span="16">
          <div v-if="videoState">
            <div id="agora_local" class="camera-part"></div>
          </div>
          <div v-else>
            <div :id="agoraRemoteId" class="camera-part"></div>
          </div>
        </el-col>
      </div>
    </div>
  </div>
</template>
<script>
import AgoraRTC from 'agora-rtc-sdk'

import socketio from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

const SocketInstance = socketio('http://localhost:4115')
export default {
  name: 'Camera',
  data() {
    return {
      client: '',
      localStream: '',
      camera: '',
      microphone: '',
      appId: this.$store.state.appId,
      audioSelect: '',
      videoSelect: '',
      audioArray: [],
      videoArray: [],
      agoraRemoteId: 'agora-remote',
      channel: '406',
      videoState: false
    }
  },
  created() {
    this.client = AgoraRTC.createClient({ mode: 'live', codec: 'h264' })
    this.getChannel()
  },
  mounted() {
    this.getDevices()
    let _this = this
    SocketInstance.on('openLive', function(data) {
      _this.$alert('系统连接你的摄像和录音装置', '连接请求', {
        confirmButtonText: '确定',
        callback: action => {
          _this.videoState = true
          _this.switch()
        }
      })
    }),
      SocketInstance.on('closeLive', function(data) {
        _this.stop()
        _this.videoState = false
      })
  },
  methods: {
    getChannel: function() {
      this.channel = (parseInt(this.$store.state.room_id) * 2 + 1).toString()
    },

    switch: function() {
      this.init()
      this.join()
    },
    stop: function() {
      this.localStream.stop()
      this.client.leave()
    },
    init: function() {
      let _this = this
      _this.client.init(
        _this.appId,
        function() {},
        function(err) {
          _this.$message.error(err)
        }
      )
    },

    join: function() {
      let _this = this
      _this.client.join(
        null,
        _this.channel,
        null,
        function(uid) {
          if (true) {
            let camera = _this.videoSelect
            let microphone = _this.audioSelect
            _this.localStream = AgoraRTC.createStream({
              streamID: uid,
              audio: true,
              cameraId: camera,
              microphoneId: microphone,
              video: _this.videoState,
              screen: false
            })
            if (true) {
              _this.localStream.setVideoProfile('720p_3')
            }

            _this.localStream.on('accessAllowed', function() {})

            // The user has denied access to the camera and mic.
            _this.localStream.on('accessDenied', function() {})
            _this.localStream.init(
              function() {
                _this.localStream.play('agora_local')
                _this.client.publish(_this.localStream, function(err) {
                  _this.$message.error('Publish local stream error:' + err)
                })
                _this.client.on('stream-published', function(evt) {})
              },
              function(err) {
                _this.$message.error(err)
              }
            )
          }
        },
        function(err) {
          _this.$message.error(err)
        }
      )
      let channelKey = ''
      _this.client.on('error', function(err) {
        _this.$message.error('Got error msg: ' + err.reason)
        if (err.reason === 'DYNAMIC_KEY_TIMEOUT') {
          _this.client.renewChannelKey(
            channelKey,
            function() {},
            function(err) {
              _this.$message.error('Renew channel key failed:  ' + err)
            }
          )
        }
      })
      _this.client.on('stream-added', function(evt) {
        let stream = evt.stream
        _this.client.subscribe(stream, function(err) {
          _this.$message.error('Subscribe stream failed ' + err)
        })
      })

      _this.client.on('stream-subscribed', function(evt) {
        let stream = evt.stream
        _this.agoraRemoteId = 'agora_remote' + stream.getId()
        stream.play(_this.agoraRemoteId)
      })

      _this.client.on('stream-removed', function(evt) {
        let stream = evt.stream
        stream.stop()
      })

      _this.client.on('peer-leave', function(evt) {
        let stream = evt.stream
        if (stream) {
          stream.stop()
        }
      })
    },
    leave: function() {
      document.getElementById('leave').disabled = true
      this.client.leave(function() {})
    },
    publish: function() {
      let _this = this
      document.getElementById('publish').disabled = true
      document.getElementById('unpublish').disabled = false
      this.client.publish(this.localStream, function(err) {
        _this.$message.error('Publish local stream error:  ' + err)
      })
    },
    unpublish: function() {
      let _this = this
      document.getElementById('publish').disabled = false
      document.getElementById('unpublish').disabled = true
      this.client.unpublish(this.localStream, function(err) {
        _this.$message.error('Unpublish local stream failed ' + err)
      })
    },

    getDevices: function() {
      let _this = this
      AgoraRTC.getDevices(function(devices) {
        for (let i = 0; i !== devices.length; ++i) {
          let device = devices[i]
          let value = device.deviceId
          if (device.kind === 'audioinput') {
            let text = device.label
            _this.audioArray.push({
              label: text,
              id: value
            })
          } else if (device.kind === 'videoinput') {
            let text = device.label
            _this.videoArray.push({
              label: text,
              id: value
            })
          } else {
            _this.$message.error('Some other kind of source/device: ' + device)
          }
        }
      })
    }
  }
}
</script>
<style>
.livepart {
  height: 34vh;
  width: 300px;
  background-color: #606266;
  position: relative;
}

.panel-body {
  float: right;
}

.video-part {
  height: 34vh;
  width: 300px;
}

.camera-part {
  float: left;
  height: 34vh;
  width: 300px;
}
</style>

