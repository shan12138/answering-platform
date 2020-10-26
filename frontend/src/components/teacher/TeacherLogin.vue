<template>
  <div class="login-page">
    <transition name="form-fade" mode="in-out">
      <section class="form_contianer" v-show="showLogin">
        <div class="manage-tip">教师登录</div>
        <el-form
          ref="AccountFrom"
          :model="account"
          :rules="rules"
          label-position="left"
          label-width="0px"
          class="demo-ruleForm"
        >
          <el-form-item prop="username">
            <el-input type="text" v-model="account.username" auto-complete="off" placeholder="账号"></el-input>
          </el-form-item>
          <el-form-item prop="pwd">
            <el-input type="password" v-model="account.pwd" auto-complete="off" placeholder="密码"></el-input>
          </el-form-item>
          <el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>
          <el-form-item style="width:100%;">
            <el-button
              type="primary"
              style="width:100%;"
              @click.native.prevent="handleLogin"
              :loading="logining"
            >登录</el-button>
          </el-form-item>
        </el-form>
      </section>
    </transition>
  </div>
</template>
<script>
export default {
  name: 'TeacherLogin',
  data() {
    return {
      logining: false,
      account: {
        username: '',
        pwd: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 5, max: 30, message: '长度在5到30个字符之间', trigger: 'blur' }
        ],
        pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 30, message: '长度在5到30个字符之间', trigger: 'blur' }
        ]
      },
      checked: true,
      showLogin: false
    }
  },
  mounted() {
    this.showLogin = true
  },
  methods: {
    handleLogin() {
      this.$refs.AccountFrom.validate(valid => {
        if (valid) {
          this.logining = true
          let form = new FormData()
          form.append('username', this.account.username)
          form.append('password', this.account.pwd)
          this.$axios
            .post('/teachers/', form, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
            .then(response => {
              let responseData = response.data
              let { token, user_id, username, code } = responseData
              if (code === '0000') {
                this.$store.dispatch('serUserIdInfo', user_id)
                this.$store.dispatch('setUserAccountInfo', username)
                sessionStorage.setItem('user_id', user_id)
                sessionStorage.setItem('username', username)
                this.$router.push({ path: './teacher/home' })
              } else {
                this.$message({
                  message: msg,
                  type: 'error'
                })
              }
            })
            .catch(error => {
              this.$message.error('用户名或密码错误')
              this.logining = false
              this.$router.replace({ path: './teacher' })
            })
        } else {
          return false
        }
      })
    }
  }
}
</script>
<style lang="less" lang="less" scoped>
@import '../../style/mixin';
html,
body,
#app {
  width: 100%;
  height: 100%;
}
.login-page {
  width: 100%;
  height: 100%;
  background-color: #324057;
}

.form_contianer {
  .wh(320px, 240px);
  .ctp(320px, 240px);
  padding: 25px;
  border-radius: 5px;
  text-align: center;
  background-color: #fff;
  .submit_btn {
    width: 100%;
    font-size: 16px;
  }
}

.manage-tip {
  position: absolute;
  width: 100%;
  top: -100px;
  left: 0;

  font-size: 34px;
  color: #fff;
}

.login-container {
  margin-top: 15em;
  width: 350px;
  margin-left: 35%;
}

.form-fade-enter-active,
.form-fade-leave-active {
  transition: all 1s;
}

.form-fade-enter,
.form-fade-leave-active {
  transform: translate3d(0, -50px, 0);
  opacity: 0;
}
</style>
