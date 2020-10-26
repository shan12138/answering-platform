<template>
  <el-card class="box-card" shadow="hover">
    <div slot="header" class="clearfix">
      <span>{{room.title}}</span>
      <el-button class="modify-btn" type="text" @click="modify">修改信息</el-button>
      <br>
      <el-button class="modify-btn" type="text" @click="manageTimetable">管理课表</el-button>
    </div>
    <div class="text item">
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">所属院系：{{room.college}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">密码：{{room.password}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">房间描述：
            <p class="text-len">{{room.description}}</p>
          </div>
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'RoomCard',
  data() {
    return {
      nowRoom: {
        id: 1,
        title: '徐达摩',
        description: '达摩院老祖',
        password: 'String',
        college: '少林寺',
        host_email: 'shaolinsi@sls',
        is_white_board: true,
        is_code_editor: true
      }
    }
  },
  props: {
    room: {
      pk: Number,
      title: String,
      description: String,
      password: String,
      college: String,
      host_email: String,
      is_white_board: Number,
      is_code_editor: Number
    }
  },
  methods: {
    modify: function() {
      this.$router.push({ name: 'modifyRoomInfo', params: { room: this.room } })
    },
    manageTimetable() {
      this.$router.push('/teacher/ManageTimetable')
    }
  },
  watch: {
    room: function(newRoom, old) {
      this.nowRoom = newRoom
    }
  }
}
</script>

<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: '';
}
.clearfix:after {
  clear: both;
}
.text-len {
  text-overflow: ellipsis;
  border: none;
}
.box-card {
  width: 300px;
  margin: 10px;
}
.modify-btn {
  float: right;
  padding: 3px 0;
}

.right-margin {
  margin-right: 20px;
}
</style>