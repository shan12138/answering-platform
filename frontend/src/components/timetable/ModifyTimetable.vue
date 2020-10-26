<template>
  <el-table :data="timetableList" id="modify-timetable">
    <el-table-column label="教学周" class="table-column">
      <template slot-scope="scope">
        <i class="el-icon-time"></i>
        <span class="span-position">第{{ scope.row.week }}周</span>
      </template>
    </el-table-column>
    <el-table-column label="上课星期" class="table-column">
      <template slot-scope="scope">
        <span class="span-position">{{ week[scope.row.day] }}</span>
      </template>
    </el-table-column>
    <el-table-column label="开始时间" class="table-column">
      <template slot-scope="scope">
        <span>{{ scope.row.open_time }}</span>
      </template>
    </el-table-column>
    <el-table-column label="结束时间" class="table-column">
      <template slot-scope="scope">
        <span class="span-position">{{ scope.row.end_time }}</span>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button size="mini" @click="modifyItem(scope.$index, scope.row)">编辑</el-button>
        <el-dialog title="时间表信息" :visible.sync="isShow">
          <el-form :model="editorForm">
            <el-form-item label="教学周" :label-width="formLabelWidth">
              <el-select v-model="editorForm.week" placeholder="请选择上课直播周">
                <el-option
                  :label="teachingWeek"
                  :value="teachingWeek"
                  v-for="teachingWeek in teachingWeeks"
                  :key="teachingWeek"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="上课周" :label-width="formLabelWidth">
              <el-select v-model="editorForm.day" autocomplete="off" placeholder="请选择本周内上课日期">
                <el-option label="周一" value="1"></el-option>
                <el-option label="周二" value="2"></el-option>
                <el-option label="周三" value="3"></el-option>
                <el-option label="周四" value="4"></el-option>
                <el-option label="周五" value="5"></el-option>
                <el-option label="周六" value="6"></el-option>
                <el-option label="周日" value="7"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="上课时间" :label-width="formLabelWidth">
              <el-time-picker
                is-range
                v-model="date"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                placeholder="选择时间范围"
              ></el-time-picker>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="{isShow = false}">取 消</el-button>
            <el-button type="primary" @click="handleEdit(scope.$index)">确 定</el-button>
          </div>
        </el-dialog>
        <el-button size="mini" type="danger" @click="deleteItem(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: 'modifyTimetable',
  data() {
    return {
      week: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      date: [new Date(), new Date()],
      room_id: this.$store.state.room_id,
      formLabelWidth: '120px',
      timetableList: [],
      isShow: false,
      teachingWeeks: [],
      editorForm: {
        week: Number,
        day: Number,
        open_time: '',
        end_time: '',
        pk: ''
      }
    }
  },
  methods: {
    modifyItem(index, row) {
      this.editorForm.day = row.day
      this.editorForm.week = row.week
      this.editorForm.pk = row.pk
      this.isShow = true
    },
    handleEdit(index) {
      let convertTime = date => date.toTimeString().split(' ')[0]
      this.editorForm.open_time = convertTime(this.date[0])
      this.editorForm.end_time = convertTime(this.date[1])
      let editorInfo = this.editorForm
      editorInfo['room_id'] = this.room_id
      let _this = this
      this.$axios
        .post('/teachers/alter_room_calendar', this.$Qs.stringify(editorInfo))
        .then(response => {
          let responseData = response.data
          if (responseData.code === this.$successCode) {
            _this.$message({
              type: 'success',
              message: '修改成功!'
            })
            this.isShow = false
          } else {
            _this.$message.error(responseData.msg)
          }
        })
        .catch(error => {
          this.$message.error(error)
        })
    },
    deleteItem(index, row) {
      let _this = this
      this.$confirm('此操作将永久删除该条信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          //执行删除操作
          let requestData = {
            pk: row.pk
          }
          this.$axios
            .post('/teachers/delete_room_calendar', this.$Qs.stringify(requestData))
            .then(response => {
              let responseData = response.data
              if (responseData.code === _this.$successCode) {
                _this.timetableList.splice(index, 1)
                _this.$message({
                  type: 'success',
                  message: '删除成功!'
                })
              } else {
                _this.$message.error(responseData.msg)
              }
            })
            .catch(error => {
              _this.$message.error(error)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    initTeachingWeekss(weekNumbers) {
      this.teachingWeeks = Array.from({ length: weekNumbers }, (v, k) => k + 1)
    }
  },
  beforeCreate() {
    let requestData = {
      room_id: this.$store.state.room_id
    }
    // 获取到数据
    this.$axios
      .post('/teachers/get_all_calendars', this.$Qs.stringify(requestData))
      .then(response => {
        let responseData = response.data
        if (responseData.code === this.$successCode) {
          this.timetableList = responseData.data.timetable
          let teachingWeeksNumbers = parseInt(
            responseData.data.max_week
          )
          this.initTeachingWeekss(teachingWeeksNumbers)
        } else {
          this.$message.error(responseData.msg)
        }
      })
      .catch(error => {
        this.$message.error(error)
      })
  }
}
</script>

<style scoped>
#modify-timetable {
  width: 100vw;
}
.table-column {
  width: 180px;
}
.span-position {
  margin-left: 10px;
}
</style>
