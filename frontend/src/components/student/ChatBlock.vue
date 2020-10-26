<template>
  <div :class="chatMsg.pos ? 'self' : ''">
    <div class="image">
      <el-popover placement="top-start" width="50px" trigger="hover">
        {{chatMsg.username}}
        <i class="el-icon-info" slot="reference">{{chatMsg.username}}</i>
      </el-popover>
    </div>
    <div class="chat-block chat-msg">
      <span>{{chatMsg.content}}</span>
      <div :class="chatMsg.pos ? 'arrow-right': 'arrow-left'"></div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      name: '真实'
    }
  },

  props: ['chatMsg'],
  methods: {},
  components: {}
}
</script>

<style scoped>
.image {
  height: 30px;
}

.image-right {
  text-align: right;
}

.self {
  text-align: right;
}

.text {
  background-color: #9eea6a;
  border: 3px solid transparent;
  border-right-color: #fff;
}

.text:before {
  content: ' ';
  position: absolute;
  top: 9px;
  right: 100%;
  border: 6px solid transparent;
  border-right-color: #fff;
}

.chat-msg {
  position: relative;
  /* height: 30px; */
  background-color: yellowgreen;
  line-height: 30px;
  padding: 0 10px;
  border-radius: 8px;
  display: inline-block;
}

.arrow-left {
  position: absolute;
  top: 5px;
  left: -18px;
  width: 0;
  height: 0;
  border: 10px solid;
  border-color: transparent;
  border-right-color: yellowgreen !important;
  display: inline-block;
}

.arrow-right {
  position: absolute;
  top: 5px;
  right: -18px;
  width: 0;
  height: 0;
  border: 10px solid;
  border-color: transparent;
  border-left-color: yellowgreen !important;
  display: inline-block;
}
</style>