<template>
  <div class="card-list">
    <el-row>
      <el-col
        :span="5"
        v-for="room in roomList"
        :key="room.id"
        :offset="index > 0 ? 2 : 2"
        style="margin: 10px 20px"
      >
        <el-card :body-style="{ padding: '5px' }" class="body-size">
          <div class="room-title">{{room.title}}</div>
          <hr>
          <div class="college-style">
            <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
            <span>开设学院： {{room.college}}</span>
          </div>
          <div class="college-style">
            <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
            <span>房间创建者： {{room.teacher_name}}</span>
          </div>
          <div style="height: 70px;">详情：{{room.description}}</div>
          <div class="button-pos">
            <el-button
              type="primary"
              class="button"
              style="height:30px; width:60px;"
              @click="enterRoom(room.id)"
            >进入房间</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <br>
    <div class="block">
      <el-pagination
        @current-change="handleCurrentChange"
        background
        layout="prev, pager, next"
        :total="1000"
        class="pagination"
      ></el-pagination>
    </div>
  </div>
</template>
<script>
import bus from '../../assets/eventsBus.js'
export default {
  name: 'RoomCard',
  data() {
    return {
      collegeName: '',
      searchContent: '',
      page: 0,
      roomNum: '8',
      roomList: []
    }
  },
  created: function() {
    this.getRoomList(this.searchContent, this.page)
  },
  mounted() {
    let _this = this
    bus.$on('chooseCollege', function(collegeName) {
      ;(_this.searchContent = collegeName),
        _this.getRoomList(this.searchContent, this.page, this.roomNum)
    })
    bus.$on('searchContent', function(searchContent) {
      _this.searchContent = searchContent
      _this.getRoomList(_this.searchContent, _this.page, _this.roomNum)
    })
  },
  methods: {
    enterRoom(roomId) {
      this.$store.dispatch('setRoomIdInfo', roomId)
      sessionStorage.setItem('room_id',roomId)
      this.$router.push('/student/LivingRoomInfo')
    },
    handleCurrentChange(val) {
      let currentPage = `${val}` - 1
      this.page = currentPage
      this.getRoomList(this.searchContent, this.page)
    },
    getRoomList(searchContent, page, roomNum) {
      let form = new FormData()
      form.append('query_condition', this.searchContent)
      form.append('page', this.page),
        form.append('limit', this.roomNum),
        this.$axios
          .post('/students/search_room', form, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(response => {
            let responseData = response.data
            let { code, msg, data } = responseData
            if (code !== '0000') {
              this.$message({
                message: msg,
                type: 'error'
              })
            } else {
              data = responseData.data
              this.roomList = []
              for (let i = 0; i < data.length; i++)
                this.roomList.push({
                  id: data[i].pk,
                  college: data[i].college,
                  title: data[i].title,
                  description: data[i].description,
                  teacher_name: data[i].teacher_name
                })
            }
          })
          .catch(error => {
            this.$message({
              message: 'error!!!!',
              type: 'error'
            })
          })
    }
  }
}
</script>

<style lang="less" lang="less" scoped>
@import '../../style/mixin';
.card-list {
  padding: 5px 80px;
}

.room-title {
  text-align: center;
  color: #464646;
}

.body-size {
  height: 200px;
  width: 300px;
  background-color: white;
  box-shadow: 0px 5px 20px #999;
  border: 1px solid #464646;
}

.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 350px;
  height: 150px;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: '';
}

.clearfix:after {
  clear: both;
}
.pagination {
  position: absolute;
  left: 50%;
  bottom: 50px;
  transform: translateX(-50%);
}
</style>