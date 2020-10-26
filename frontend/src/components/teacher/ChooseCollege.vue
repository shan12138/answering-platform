<template>
  <div class="college-list">
    <el-button
      type="primary"
      round
      v-for="college in collegeList"
      :key="college.id"
      @click="sendCollegeName(college.name)"
    >{{college.name}}</el-button>
  </div>
</template>
<script>
import bus from '../../assets/eventsBus.js'
export default {
  name: 'ChooseCollege',
  data() {
    return {
      collegeList: []
    }
  },
  beforeCreate() {
    this.$axios
      .post('/teachers/list_colleges', {
        headers: {
          'Content-Type': 'multipart/form-data' //hearder 很重要，Content-Type 要写对
        }
      })
      .then(response => {
        let responseData = response.data
        let { code, msg, data } = responseData
        if (code !== '0000') {
          this.$message.error(responseData.msg)
        } else {
          this.collegeList = []
          let data = responseData.data
          for (let i = 0; i < data.length; i++) {
            this.collegeList.push({
              name: data[i].name,
              id: data[i].pk
            })
          }
        }
      })
      .catch(error => {
        this.$message({
          message: '学院得到失败',
          type: 'error'
        })
      })
  },
  methods: {
    sendCollegeName: function(collegeName) {
      bus.$emit('chooseCollege', collegeName)
    }
  }
}
</script>
<style scoped>
.college-list {
  display: inline;
}
</style>


