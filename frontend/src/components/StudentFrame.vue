<template>
  <div id="bos">
    <div id="header">
      <el-menu
        :default-active="activeIndex2"
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        id="header-in"
        router
      >
        <el-menu-item index="Home">
          <i class="el-icon-menu"></i>
        </el-menu-item>
        <el-menu-item tag="div" class="item-center" index="5">
          <span class="title">计算机在线答疑系统</span>
        </el-menu-item>

        <el-submenu index="2" class="item-right">
          <template slot="title">{{account}}</template>
          <el-menu-item index="Info">个人信息</el-menu-item>
          <el-menu-item @click="logout">退出</el-menu-item>
        </el-submenu>
        <el-menu-item index="3" class="item-right">
          <span>我的房间</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div id="main">
      <router-view/>
    </div>
  </div>
</template>
<script>
import StudentLog from '../components/admin/StudentLog'
export default {
  data() {
    return {
      activeIndex: '1',
      activeIndex2: '1',
      account: this.$store.state.account
    }
  },
  methods: {
    handleSelect(key, keyPath) {},
    logout() {
      this.$router.push('/student')
    }
  },
  components: {}
}
</script>
<style scoped>
.item-right {
  float: right;
}
.item-center {
  float: left;
  left: 30%;
  width: 400px;
  text-align: center;
  font-size: 30px;
  color: blueviolet;
}
.college-pos {
  padding: 10px 20px;
}

.title {
  color: gray;
}

#bos {
  display: flex;
  flex-direction: column;
}

#header {
  flex: 1 1 10px;
  padding: 0;
}

#header-in {
  height: 10vh;
}

#main {
  height: 90vh;
  flex: 10 10 100px;
  padding: 0;
}
</style>




