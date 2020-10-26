<template>
  <el-card shadow="always" class="level-one-div">
    <div slot="header" class="register-title">
      <span>修改房间信息</span>
    </div>
    <div>
      <el-form
        :label-position="labelPosition"
        :model="roomForm"
        status-icon
        :rules="rules"
        ref="roomForm"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="roomForm.title" placeholder="请输入标题" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="院系" prop="selected">
          <el-select v-model="roomForm.selected" placeholder="请选择所属院系" autocomplete="off">
            <el-option
              v-for='college in collegeList'
              :key='college.pk'
              :label='college.name'
              :value='college.pk'
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="roomForm.password" placeholder="请输入密码" clearable></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            type="textarea"
            v-model="roomForm.description"
            placeholder="请输入描述（100字以内）"
            maxlength="100"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="白板:">
          <el-switch v-model="roomForm.is_white_board"></el-switch>
          <span class="left-margin">代码编辑器:
            <el-switch v-model="roomForm.is_code_editor"></el-switch>
          </span>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="create('roomForm')">修改</el-button>
          <el-button @click="resetForm('roomForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'ModifyRoomInfo',
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
      roomForm: {
        id: 1,
        title: 'String',
        description: 'String',
        password: 'String',
        selected: 'String',
        is_white_board: true,
        is_code_editor: true,
        collegeList: [],
        host_email: 'String'
      },
      rules: {
        title: [{ validator: checkTitle, trigger: 'blur' }],
        description: [{ validator: checkDescribtion, trigger: 'blur' }],
        selected: [{ validator: checkSelected, trigger: 'blur' }]
      }
    }
  },
   beforeCreate() {
    this.$axios({
      methods: 'post',
      url: '/teachers/list_colleges',
    })
      .then(response => {
        this.collegeList = response.data.data
      })
      .catch(err => {
        alert(err)
      })
  },
  computed: {
    collegeList: {
      get: function() {
        return this.roomForm.collegeList
      },
      set: function(list) {
        this.roomForm.collegeList = list
      }
    }
  },

  methods: {
    getCollegeId: function() {
      for (let college of this.collegeList) {
        if (college.pk == this.roomForm.selected) {
          return college.pk
        }
      }
    },
    create: function(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('提交成功!!')
          this.$axios
            .post(
              '/teachers/alter_room',
              this.$Qs.stringify({
                room_id: this.roomForm.id,
                title: this.roomForm.title,
                description: this.roomForm.description,
                college: this.getCollegeId(),
                password: this.roomForm.password,
                is_white_board: this.roomForm.is_white_board,
                is_code_editor: this.roomForm.is_code_editor
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
      this.roomForm.title = ''
      this.roomForm.description = ''
      this.roomForm.password = ''
      this.roomForm.selected = ''
    }
  },
  mounted() {
    this.roomForm.id = this.$route.params.room.pk
    this.roomForm.title = this.$route.params.room.title
    this.roomForm.description = this.$route.params.room.description
    this.roomForm.password = this.$route.params.room.password
    this.roomForm.selected = this.$route.params.room.college
    this.roomForm.is_white_board = this.$route.params.room.is_white_board
    this.roomForm.is_code_editor = this.$route.params.room.is_code_editor
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
.box-card {
  width: 300px;
  margin: 10px;
}
</style>
