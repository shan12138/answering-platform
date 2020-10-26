<template>
  <el-card shadow="always" class="level-one-div">
    <div slot="header" class="register-title">
      <span>创建直播间</span>
    </div>
    <div>
      <el-form
        :label-position="labelPosition"
        :model="addRoomForm"
        status-icon
        :rules="rules"
        ref="addRoomForm"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="addRoomForm.title" placeholder="请输入标题" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="院系" prop="selected">
          <el-select v-model="addRoomForm.selected" placeholder="请选择所属院系" autocomplete="off">
            <el-option
              v-for="college in collegeList"
              :key="college.pk"
              :label="college.name"
              :value="college.pk"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="addRoomForm.password" placeholder="请输入密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            type="textarea"
            v-model="addRoomForm.description"
            placeholder="请输入描述（100字以内）"
            maxlength="100"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="白板:">
          <el-switch v-model="addRoomForm.is_white_board"></el-switch>
          <span class="left-margin">代码编辑器:
            <el-switch v-model="addRoomForm.is_code_editor"></el-switch>
          </span>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="createRooms('addRoomForm')">创建</el-button>
          <el-button @click="resetForm('addRoomForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'CreateRoom',
  data() {
    let checkTitle = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('标题不能为空'))
      }
      setTimeout(() => {
        if (value.length > 20) {
          callback(new Error('标题过长'))
        } else {
          callback()
        }
      }, 1000)
    }
    let checkDescribtion = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('请描述一下您的直播间吧'))
      }
      setTimeout(() => {
        if (value.length > 100) {
          callback(new Error('标题过长'))
        } else {
          callback()
        }
      }, 1000)
    }
    let checkSelected = (rule, value, callback) => {
      if (value === '' || value === null) {
        return callback(new Error('请选择学院'))
      } else {
        return callback()
      }
    }
    return {
      labelPosition: 'right',
      addRoomForm: {
        title: '',
        description: '',
        password: '',
        selected: '',
        is_white_board: false,
        is_code_editor: false,
        collegeList: []
      },
      rules: {
        title: [{ validator: checkTitle, trigger: 'blur' }],
        description: [{ validator: checkDescribtion, trigger: 'blur' }],
        selected: [{ validator: checkSelected, trigger: 'blur' }]
      }
    }
  },
  computed: {
    collegeList: {
      get: function() {
        return this.addRoomForm.collegeList
      },
      set: function(list) {
        this.addRoomForm.collegeList = list
      }
    }
  },
  beforeCreate() {
    this.$axios({
      methods: 'post',
      url: '/teachers/list_colleges'
    })
      .then(response => {
        this.collegeList = response.data.data
      })
      .catch(err => {
        alert(err)
      })
  },
  methods: {
    createRooms: function(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('提交成功!!')
          this.$axios
            .post(
              '/teachers/create_room',
              this.$Qs.stringify({
                user_id: this.$store.state.user_id,
                title: this.addRoomForm.title,
                description: this.addRoomForm.description,
                college: this.addRoomForm.selected,
                password: this.addRoomForm.password,
                is_code_editor: this.addRoomForm.is_code_editor,
                is_white_board: this.addRoomForm.is_white_board
              })
            )
            .then(response => {
              alert(response.data.msg)
            })
            .catch(err => {
              alert(err)
            })
        } else {
          return false
        }
      })
    },
    resetForm: function(formName) {
      this.addRoomForm.title = ''
      this.addRoomForm.description = ''
      this.addRoomForm.password = ''
      this.addRoomForm.selected = ''
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
.left-margin {
  margin-left: 40px;
}
</style>
