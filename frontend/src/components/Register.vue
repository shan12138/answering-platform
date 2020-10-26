<template>
  <el-card shadow="always" class="level-one-div">
    <div slot="header" class="register-title">
      <span>注册账号</span>
    </div>
    <div>
      <el-form :label-position="labelPosition" label-width="80px">
        <el-form-item label="学号">
          <el-input v-model="username" placeholder="请输入您的学号" clearable></el-input>
        </el-form-item>
        <el-form-item label="手机号码">
          <el-input v-model="telephone" placeholder="请输入您的手机号码" clearable></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" type="password" placeholder="请输入密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="password2" type="password" placeholder="请核对密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="验证码">
          <el-input v-model="checkNumber" placeholder="点击下方按钮获取验证码" clearable></el-input>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="getVerificationCode">{{verificationText}}</el-button>
          <el-button type="primary" @click="register">注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      labelPosition: 'right',
      username: '',
      telephone: '',
      password: '',
      password2: '',
      checkNumber: '',
      verificationText: '获取验证码'
    }
  },
  computed: {},
  methods: {
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
    register: function() {
      this.$axios
        .post(
          '/students/signup',
          this.$Qs.stringify({
            username: this.username,
            password: this.password,
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

<style scoped>
.register-title {
  font-size: 34px;
  text-align: center;
  font-family: Helvetica;
}
.level-one-div {
  width: 380px;
  margin: auto;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.errorText {
  color: red;
}
</style>
