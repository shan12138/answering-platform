<template>
  <div class="college-list">
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="input" placeholder="请输入搜索房间相关信息"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit" class="button-size">搜索</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import bus from '../../assets/eventsBus.js'
export default {
  name: 'SearchInfo',
  data() {
    return {
      input: ''
    }
  },
  methods: {
    onSubmit() {
      bus.$emit('searchContent', this.input)
    }
  }
}
</script>
<style scoped>
.college-list {
  display: block-inline;
  padding: 10px 20px;
  float: right;
  right: 100px;
  width: 400px;
  height: 50px;
}
.button-size {
  padding: 10px 20px;
}
</style>