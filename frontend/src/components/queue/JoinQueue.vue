<template>
  <el-row>
    <el-button type="primary" id="queue-button" :disabled="isDisable">主要按钮</el-button>
  </el-row>
</template>

<script>
export default {
  name: 'JoinQueue',
  data() {
    return {
      isDisable: true
    }
  }
}
</script>

