<template>
  <el-card shadow='always'>
    <el-form
      :label-position='labelPosition'
      label-width='80px'
      class='demo-ruleForm'
      :model='infoForm'
      status-icon
      :rules='rules'
      ref='infoForm'
    >
      <el-form-item label='学号'>
        <el-input v-model='infoForm.stuId' disabled></el-input>
      </el-form-item>
      <el-form-item label='真实姓名' prop='name'>
        <el-input v-model='infoForm.name' placeholder='请输入您的真实姓名' clearable autocomplete='off'></el-input>
      </el-form-item>
      <el-form-item label='邮箱' prop='email'>
        <el-input v-model='infoForm.email' placeholder='请输入您的邮箱' clearable autocomplete='off'></el-input>
      </el-form-item>
      <el-form-item size='large'>
        <el-button type='primary' @click='modify'>修改</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: 'ModifyStuBasicInfo',
  data() {
    let validateName = (rule, value, callback) => {
      if (value === '') {
        return callback(new Error('请输入姓名'))
      }
      return callback()
    }
    let validateEmail = (rule, value, callback) => {
      if (value === '' || value === null) {
        return callback(new Error('请输入邮箱'))
      }

      let regExp = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/
      if (!regExp.test(value)) {
        return callback(new Error('请正确的邮箱地址'))
      }
      return callback()
    }
    return {
      labelPosition: 'right',
      infoForm: {
        stuId: 'loading',
        name: 'loading',
        email: 'loading'
      },
      oldName: 'loading',
      oldEmail: 'loading',
      rules: {
        name: [{ validator: validateName, trigger: 'blur' }],
        email: [{ validator: validateEmail, trigger: 'blur' }]
      }
    }
  },
  beforeCreate() {
    this.$axios
      .post(
        '/students/get_student_id',
        this.$Qs.stringify({
          user_id: this.$store.state.user_id
        })
      )
      .then(response => {
        this.infoForm.stuId = response.data.stuId
      })
      .catch(err => {
        alert(err)
      })
    this.$axios
      .post(
        '/students/get_name',
        this.$Qs.stringify({
          user_id: this.$store.state.user_id
        })
      )
      .then(response => {
        this.oldName = this.infoForm.name = response.data.name
      })
      .catch(err => {
        alert(err)
      })
    this.$axios
      .post(
        '/students/get_email',
        this.$Qs.stringify({
          user_id: this.$store.state.user_id
        })
      )
      .then(response => {
        this.oldEmail = this.infoForm.email = response.data.email
      })
      .catch(err => {
        alert(err)
      })
  },
  methods: {
    modify: function() {
      if (
        this.oldName === this.infoForm.name &&
        this.oldEmail === this.infoForm.email
      ) {
        alert('请修改姓名或者邮箱')
        return
      }
      this.$refs.infoForm.validate(valid => {
        if (valid) {
          alert('提交成功!!')
          if (this.oldName !== this.infoForm.name) {
            this.changeName()
          }
          if (this.oldEmail !== this.infoForm.email) {
            this.changeEmail()
          }
        } else {
          return false
        }
      })
    },
    changeName: function() {
      this.$axios
        .post(
          '/students/change_name',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id,
            name: this.infoForm.name
          })
        )
        .then(response => {
          alert(response.data.msg)
        })
        .catch(err => {
          alert(err)
        })
    },
    changeEmail: function() {
      this.$axios
        .post(
          '/students/change_email',
          this.$Qs.stringify({
            user_id: this.$store.state.user_id,
            email: this.infoForm.email
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
