<template>
  <el-card shadow='always'>
    <el-form :label-position='labelPosition' label-width='80px'>
      <el-form-item label='旧密码'>
        <el-input v-model='oldPassword' placeholder='请输入原密码' clearable></el-input>
      </el-form-item>
      <el-form-item label='密码'>
        <el-input type="password" v-model='newPassword' placeholder='请输入新密码' clearable></el-input>
      </el-form-item>
      <el-form-item label='确认密码'>
        <el-input type="password" v-model='password2' placeholder='请核对新密码' clearable></el-input>
      </el-form-item>
      <el-form-item size='large'>
        <el-button type='primary' @click='modify'>修改</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: 'ModifyStuPswd',
  data() {
    return {
      labelPosition: 'right',
      oldPassword: '',
      newPassword: '',
      password2: ''
    }
  },
  methods: {
    modify: function() {
      if (this.oldPassword === '') {
        alert('请输入原密码')
      } else if (this.newPassword === '') {
        alert('请输入新密码')
      } else if (this.newPassword !== this.password2) {
        alert('请核对新密码')
      } else {
        this.changePswd()
      }
    },
    changePswd: function() {
      this.$axios
        .post(
          '/students/change_password',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id,
            old_password: this.oldPassword,
            new_password: this.newPassword
          })
        )
        .then(response => {
          alert(response.data.msg)
        })
        .catch(err => {
          alert(err)
        })
    }
  }
}
</script>
