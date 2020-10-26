<template>
  <div>
    <el-tooltip class="item" effect="dark" content="添加课程" placement="right-start">
      <el-button type="primary" icon="el-icon-edit" circle @click="dialogFormVisible = true"></el-button>
    </el-tooltip>
    <el-dialog title="新添课程" :visible.sync="dialogFormVisible">
      <el-form :model="newTimetableItem">
        <el-form-item label="教学周" :label-width="formLabelWidth">
          <el-select v-model="newTimetableItem.weeks" multiple placeholder="请选择上课的教学周">
            <el-option
              :label="lable"
              :value="value"
              v-for="(lable,value) of maxWeek"
              :key="value"
              v-bind:disable="currWeek < value ? false : true"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上课日期" :label-width="formLabelWidth">
          <el-select v-model="newTimetableItem.days" multiple placeholder="请选择上课的日期">
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
            v-model="newTimetableItem.date"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            placeholder="选择时间范围"
          ></el-time-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="createNewItem">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'createTimetable',
  data() {
    return {
      maxWeek: Number,
      currWeek: Number,
      formLabelWidth: '100px',
      dialogFormVisible: false,
      newTimetableItem: {
        weeks: [],
        days: [],
        date: [new Date(), new Date()]
      }
    }
  },
  methods: {
    createNewItem() {
      let requestData = this.getRequestData()
      this.$axios
        .post('teachers/create_room_calendar', requestData, {
          headers: {
            'Content-Type': 'multipart/form-data' //hearder 很重要，Content-Type 要写对
          }
        })
        .then(response => {
          let responseData = response.data
          if (responseData.code === this.$successCode) {
            this.$message({
              message: '信息创建成功！',
              type: 'success'
            })
          } else {
            this.$message.error(responseData.msg)
          }
          this.dialogFormVisible = false
        })
        .catch(error => {
          this.$message.error(error)
          this.dialogFormVisible = false
        })
    },
    getRequestData() {
      let newTimetableItem = this.newTimetableItem
      let timeList = this.convertTime(newTimetableItem.date)
      let requestData = new FormData()
      requestData.append('room_id', this.$store.state.room_id)
      requestData.append('weeks', newTimetableItem.weeks)
      requestData.append('days', newTimetableItem.days)
      requestData.append('open_time', timeList.openTime)
      requestData.append('close_time', timeList.closeTime)
      return requestData
    },
    convertTime(date) {
      let openTimeList = date[0].toTimeString().split(' ')
      let closeTimeList = date[1].toTimeString().split(' ')
      return { openTime: openTimeList[0], closeTime: closeTimeList[0] }
    }
  },
  beforeMount() {
    this.$axios
      .post(
        '/teachers/get_curr_max_week',
        this.$Qs.stringify({ room_id: this.$store.state.room_id })
      )
      .then(response => {
        let requestData = response.data
        if (requestData.code === this.$successCode) {
          this.maxWeek = requestData.data.max_week
          this.currWeek = requestData.data.current_week
        }
      })
      .catch(error => {
        this.$message.error(error)
      })
  }
}
</script>

