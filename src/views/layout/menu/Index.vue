<template>
  <div>
    <el-menu 
      class="el-menu-vertical-demo" 
      background-color="#112f50" 
      text-color="#fff" 
      active-text-color="#ffd04b" 
      router 
      :collapse="true" 
    >
      <el-menu-item index="#">
        <span slot="title">原料盐车间管理系统</span>
      </el-menu-item>
      <MenuList :dyMenuList="dyMenuList"></MenuList>
    </el-menu>
  </div>
</template>

<script>
import MenuList from './MenuList.vue';
import { mapState } from 'vuex';

export default {
  components: {
    MenuList
  },
  computed: {
    ...mapState('Menu', ['dyMenuList'])
  },
  methods: {
    activeMenu() {
      let route = this.$route;
      let { name, meta } = route;
      if (meta.activeMenu) {
        return meta.activeMenu;
      } else {
        return name;
      }
    }
  }
};
//////////////////////////////这是通过下面css none把侧边栏隐藏，但直接这个页面没代码，我看也是一样的效果
</script>

<style lang="less" scoped>
.el-menu {
  display: none; /* 隐藏侧边栏 */
}
</style>