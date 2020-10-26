<template>
  <el-card shadow='always'>
    <el-form :label-position='labelPosition' label-width='80px'>
      <el-form-item label='邮箱'>
        <el-input v-model='email' :disabled='true'></el-input>
      </el-form-item>
      <el-form-item label='姓名'>
        <el-input v-model='newName' placeholder='请输入您的姓名' clearable></el-input>
      </el-form-item>
      <el-form-item size='large'>
        <el-button type='primary' @click='modify'>修改</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: 'ModifyTeaName',
  data () {
    return {
      labelPosition: 'right',
      email: 'loding',
      oldName: 'loding',
      newName: 'loding'
    }
  },
  beforeCreate() {
    this.$axios
        .post(
          '/teachers/get_email',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id
          })
        )
        .then(response => {
          this.email = response.data.email
        })
        .catch(err => {
          alert(err)
        })
    this.$axios
        .post(
        '/teachers/get_name',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id
          })
        )
        .then(response => {
        this.oldName = this.newName = response.data.data
        })
        .catch(err => {
          this.$message.error(err)
        })
  },
  methods: {
    modify: function () {
      if (this.oldName === this.newName) {
        this.$message('新名字与旧名字一样!!!')
      }
      else {
        this.$axios.post(
          '/teachers/change_name',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id,
            name: this.newName
          })
        )
        .then(response => {
          this.$message(response.data.msg)
        })
        .catch(err => {
          this.$message.error(err.data)
        })
      }
    }
  }
}
</script>
