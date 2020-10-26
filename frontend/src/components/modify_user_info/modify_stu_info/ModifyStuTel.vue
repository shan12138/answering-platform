<template>
  <el-card shadow='always'>
    <el-form :label-position='labelPosition' label-width='80px'>
      <el-form-item label='学号'>
        <el-input v-model='stuId' disabled></el-input>
      </el-form-item>
      <el-form-item label='手机号码'>
        <el-input v-model='telephone' placeholder='请输入您的手机号码' clearable></el-input>
      </el-form-item>
      <el-form-item label='验证码'>
        <el-input v-model='checkNumber' placeholder='点击下方按钮获取验证码' clearable></el-input>
      </el-form-item>
      <el-form-item size='large'>
        <el-button type='primary' @click='getVerificationCode'>{{verificationText}}</el-button>
        <el-button type='primary' @click='modify'>修改</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: 'ModifyStuTel',
  data() {
    return {
      labelPosition: 'right',
      stuId: '',
      telephone: '',
      checkNumber: '',
      verificationText: '获取验证码'
    }
  },
  mounted() {
    this.mountStuId()
  },
  methods: {
    mountStuId: function() {
      this.$axios
        .post(
          '/students/get_student_id',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id
          })
        )
        .then(response => {
          this.stuId = response.data.stuId
        })
        .catch(err => {
          alert(err)
        })
    },
    getVerificationCode: function() {
      if (this.username === '') {
        return alert('请输入学号')
      }
      if (this.telephone === '') {
        return alert('请输入电话')
      }
      if (this.password === '') {
        return alert('请输入密码')
      }
      this.$axios
        .post(
          '/students/send_code',
          this.$Qs.stringify({
            telephone: this.telephone
          })
        )
        .then(response => {
          alert(response.data.msg)
        })
        .catch(err => {
          alert(err)
        })
    },
    modify: function() {
      if (this.telephone === '') {
        alert('请输入要改的手机号')
      } else if (this.checkNumber === '') {
        alert('请输入验证码')
      } else {
        this.changeTel()
      }
    },
    changeTel: function() {
      this.$axios
        .post(
          '/students/change_tele',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id,
            telephone: this.telephone,
            code: this.checkNumber
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
