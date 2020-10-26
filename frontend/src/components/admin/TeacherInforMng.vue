<template>
  <el-main id="main-body">
    <el-upload
      class="upload-infor"
      action="/api/admin_manage/input_teacher/"
      :http-request="uploadFile"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      :limit="1"
      :before-upload="beforeAvatarUpload"
      :on-exceed="handleExceed"
      :file-list="fileList"
    >
      <el-button size="small" type="primary">一键导入教师信息</el-button>
      <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
    </el-upload>
    <el-table :data="searchKeyWord" id="data-table">
      <el-table-column type="index" :index="indexMethod"></el-table-column>
      <el-table-column label="Email" prop="email"></el-table-column>
      <el-table-column label="Password" prop="password"></el-table-column>
      <el-table-column align="right">
        <template slot="header" slot-scope="scope">
          <el-input v-model="keyWord" size="mini" placeholder="输入关键字搜索"/>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  name: 'teacherInforMng',
  data() {
    return {
      tableData: [],
      fileList: [],
      keyWord: ''
    }
  },
  methods: {
    indexMethod(index) {
      return index + 1
    },
    handleRemove(file, fileList) {
      // 可选的补充功能
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      )
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    handleDelete(index, row) {
      this.$confirm(`确定删除该条数据吗？ ${row.email}？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          //向后台发送删除数据请求
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },

    uploadFile(params) {
      let fileObj = params.file
      let form = new FormData()
      form.append('file', fileObj)
      form.append('csrf_token', sessionStorage.getItem('csrftoken'))
      this.$axios
        .post('/admin_manage/input_teacher', form, {
          headers: {
            'Content-Type': 'multipart/form-data' //hearder 很重要，Content-Type 要写对
          }
        })
        .then(response => {
          let responseData = response.data
          let code = responseData.code
          if (code !== '0000') {
            this.$message.error(responseData.msg)
          } else {
            this.$message({
              message: responseData.msg,
              type: 'success'
            })
          }
        })
    },
    beforeAvatarUpload(file) {
      const fileType = file.type
      let isExcel = false
      if (fileType === 'application/vnd.ms-excel') {
        isExcel = true
      } else if (
        fileType ===
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ) {
        isExcel = true
      }
      if (!isExcel) {
        this.$message.error('只支持上传excel格式的文件!')
        this.fileList = []
      }
      return true
    }
  },
  computed: {
    searchKeyWord() {
      let _this = this
      let visibleTableData = _this.tableData.filter(data => {
        let teacherEmail = data.email.toLowerCase()
        return (
          !_this.keyWord || teacherEmail.includes(_this.keyWord.toLowerCase())
        )
      })
      return visibleTableData
    }
  }
}
</script>

