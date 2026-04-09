<template>
    <div>
      <iframe :src="baseUrl" width="100%" height="1000px" frameborder="0"></iframe>
    </div>
</template>

<script>
export default {
  created(){
    
  },
  data(){
    return{
      baseUrl:'http://127.0.0.1:9070/runqian5/reportJsp/showReport.jsp?rpx=/111/test1.rpx&start=2024-04-05&end=2024-04-06'
    }
  },
  methods:{
    
  }
}
</script>

<style>

</style>