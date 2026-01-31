const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
    devServer: {
      host: '0.0.0.0', // 使用 0.0.0.0 来允许任何 IP 地址访问  
      port: 9071,
    proxy: {
      '/api': {
        // target:process.env.VUE_APP_BASE_URL,//http://localhost:9898/api
        target: 'http://localhost:8899',//http://localhost:9898/api
        ws: true,
        changeOrigin: true,
        pathRewrite:{
          '^/api':''
        }
      },
       

      '/foo': {
        target: 'http://www.baidu.com'
      }
    }
  },
   
 
})
