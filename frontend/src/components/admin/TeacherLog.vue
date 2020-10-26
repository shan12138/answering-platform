<template>
  <el-main id="main-body">
    <el-table :data="searchKeyWord" id="data-table">
      <el-table-column type="index" :index="indexMethod"></el-table-column>
      <el-table-column label="日期" prop="date"></el-table-column>
      <el-table-column label="姓名" prop="name"></el-table-column>
      <el-table-column label="操作" prop="operate"></el-table-column>
      <el-table-column label="传入参数" prop="parameter"></el-table-column>
      <el-table-column label="返回值" prop="returnValue"></el-table-column>
      <el-table-column align="right">
        <template slot="header">
          <el-input v-model="keyWord" size="mini" placeholder="输入关键字搜索"/>
        </template>
      </el-table-column>
    </el-table>
  </el-main>
</template>
<script>
export default {
  data() {
    return {
      teacherLogList: []
    }
  },
  methods: {
    indexMethod(index) {
      return index + 1
    }
  },
  computed: {
    searchKeyWord: function() {
      let _this = this
      let visibleTableData = _this.teacherLogList.filter(data => {
        const teacherLogsArray = data.name.toLowerCase()
        const date = data.date
        return (
          !_this.keyWord ||
          teacherLogsArray.includes(_this.keyWord.toLowerCase())
        )
      })
      return visibleTableData
    }
  }
}
</script>
