<template>
  <el-card shadow="always" class="level-one-div">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="修改个人信息" name="first">
        <modify-info></modify-info>
      </el-tab-pane>
      <el-tab-pane label="更改绑定手机" name="second">
        <modify-tel></modify-tel>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="third">
        <modify-pswd></modify-pswd>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script>
import ModifyStuBasicInfo from './modify_stu_info/ModifyStuBasicInfo'
import ModifyStuPswd from './modify_stu_info/ModifyStuPswd'
import ModifyStuTel from './modify_stu_info/ModifyStuTel'

export default {
  name: 'ModifyPersonalInfo',
  data() {
    return {
      activeName: 'first'
    }
  },
  methods: {
    handleClick(tab, event) {}
  },
  components: {
    'modify-info': ModifyStuBasicInfo,
    'modify-pswd': ModifyStuPswd,
    'modify-tel': ModifyStuTel
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
