<template>
  <el-main id="main-body">
    <el-upload
      class="upload-infor"
      action="/api/admin_manage/input_college/"
      :http-request="uploadFile"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      :limit="1"
      :before-upload="beforeAvatarUpload"
      :on-exceed="handleExceed"
      :file-list="fileList"
    >
      <el-button size="small" type="primary">一键导入院系信息</el-button>
      <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
    </el-upload>
    <el-table :data="searchKeyWord">
      <el-table-column type="index" :index="indexMethod"></el-table-column>
      <el-table-column label="Date" prop="date"></el-table-column>
      <el-table-column label="Department" prop="department"></el-table-column>
      <el-table-column align="right">
        <template slot="header" slot-scope="scope">
          <el-input v-model="keyWord" size="mini" placeholder="输入关键字搜索"/>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" @click="openDialogForm(scope.row.department)">Edit</el-button>
          <el-dialog title="院系信息" :visible.sync="dialogFormVisible">
            <el-form :model="dialogForm">
              <el-form-item label="院系名" :label-width="formLabelWidth">
                <el-input v-model="dialogForm.name" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="{dialogFormVisible = false}">取 消</el-button>
              <el-button type="primary" @click="handleEdit(scope.$index)">确 定</el-button>
            </div>
          </el-dialog>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  name: 'departmentsInforMng',
  data() {
    return {
      tableData: [],
      fileList: [],
      keyWord: '',
      dialogFormVisible: false,
      dialogForm: {
        name: '',
        delivery: false,
        type: []
      },
      formLabelWidth: '120px'
    }
  },
  methods: {
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    handleRemove(file, fileList) {
      // 删除被上传的文件请求
      this.fileList = []
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      )
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
    },
    uploadFile(param) {
      let fileObj = param.file
      let URL = '/admin_manage/input_college'
      let form = new FormData()
      form.append('file', fileObj)
      form.append('csrf_token', sessionStorage.getItem('csrftoken'))
      this.$axios.post(URL, form).then(response => {
        let data = response.data
        const code = data.code
        if (code !== '0000') {
          this.$message.error(data.msg)
        } else {
          this.$message({
            message: data.msg,
            type: 'success'
          })
        }
      })
    },

    indexMethod(index) {
      return index + 1
    },
    openDialogForm(department) {
      this.dialogFormVisible = true
      this.dialogForm.name = department
    },
    handleEdit(index) {
      let name = this.dialogForm.name
      // 执行修该数据的操作
      this.tableData[index].department = name
      this.dialogFormVisible = false
    },
    handleDelete(index, row) {
      this.$confirm('此操作将永久删除该条信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          //执行删除操作

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
    }
  },
  computed: {
    searchKeyWord: function() {
      let _this = this
      let visibleTableData = _this.tableData.filter(data => {
        let department = data.department.toLowerCase()
        return (
          !_this.keyWord || department.includes(_this.keyWord.toLowerCase())
        )
      })
      return visibleTableData
    }
  }
}
</script>

