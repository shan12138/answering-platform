<template>
  <el-container id="admin-view" style="border: 1px solid #eee;">
    <el-aside class="color" width="200px" style>
      <h2 class="menu-title">管理员系统</h2>
      <el-menu :default-openeds="['3']" router class="color">
        <el-menu-item index="teacherInforMng">
          <i class="el-icon-menu"></i>
          <span slot="title">教师信息管理</span>
        </el-menu-item>
        <el-menu-item index="departmentsInforMng">
          <i class="el-icon-menu"></i>
          <span slot="title">院系信息管理</span>
        </el-menu-item>
        <el-submenu index="teacherLog">
          <template slot="title">
            <i class="el-icon-document"></i>日志管理
          </template>
          <el-menu-item index="teacherLog">教师操作日志</el-menu-item>
          <el-menu-item index="studentLog">学生操作日志</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="color header">
        <el-dropdown @command="handleCommand">
          <i class="el-icon-setting" style="margin-right: 15px;"></i>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="logout">退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <span>{{admin}}</span>
      </el-header>
      <router-view></router-view>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'adminFrame',
  data() {
    return {
      admin: '未登录'
    }
  },
  methods: {
    handleCommand(command) {
      if (command === 'logout') {
        sessionStorage.removeItem('user_id')
        sessionStorage.removeItem('username')
        this.$router.push('/admin')
      }
    }
  }
}
</script>

<style scoped>
#admin-view {
  height: 100vh;
  padding: 0;
  margin: 0;
  border: 0;
}

.color {
  background-color: rgb(238, 241, 246);
}

.header {
  padding-top: 15px;
  font-size: 18px;
  text-align: right;
}

#main-body {
  margin: 2px 30px;
}

#data-table {
  margin: 30px 0;
}

.menu-title {
  font-size: 20px;
  text-align: center;
}
</style>
