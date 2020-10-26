<template>
  <el-card shadow="always" class="level-one-div">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="修改个人信息" name="first">
        <modify-name></modify-name>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="second">
        <modify-pswd></modify-pswd>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script>
import ModifyTeaName from './modify_tea_info/ModifyTeaName'
import ModifyTeaPassword from './modify_tea_info/ModifyTeaPassword'
export default {
  name: 'ModifyTeaInfo',
  data() {
    return {
      activeName: 'first'
    }
  },
  methods: {
    handleClick(tab, event) {}
  },
  components: {
    'modify-name': ModifyTeaName,
    'modify-pswd': ModifyTeaPassword
  }
}
</script>

<style scoped>
.level-one-div {
  width: 380px;
  margin: auto;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
</style>
