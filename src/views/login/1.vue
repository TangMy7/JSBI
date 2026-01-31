<template>
    <div class="main">
        <el-form :rules="rules" ref="loginForm" :model="loginForm" class="loginContainer">
            <h3 class="loginTitle">系统登录</h3>
            <el-form-item prop="username">
                <el-input type="text" v-model="loginForm.username" placeholder="亲，请输入用户名">
                </el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input type="password" v-model="loginForm.password" placeholder="亲，请输入密码">
                </el-input>
            </el-form-item>
            <el-checkbox v-model="checked" class="loginRemember">记住我</el-checkbox>
            <el-button type="primary" style="width: 100%" @click="submitLogin">登录</el-button>
        </el-form>
    </div>
    </template>
    
    <script>
    import {
        mapMutations
    } from 'vuex';
    export default {
        name: "Login",
        data() {
            return {
                captchaUrl: "",
                loginForm: {
                    username: "",
                    password: "",
                },
                checked: true,
                rules: {
                    username: [{
                            required: true,
                            message: "请输入用户名",
                            trigger: "blur"
                        },
                        {
                            min: 1,
                            max: 14,
                            message: "长度在 5 到 14 个字符",
                            trigger: "blur",
                        },
                    ],
                    password: [{
                            required: true,
                            message: "请输入密码",
                            trigger: "blur"
                        }, ,
                        {
                            min: 1,
                            message: "密码长度要大于1",
                            trigger: "blur"
                        },
                    ],
                },
            };
        },
        methods: {
            ...mapMutations('Login', ['setUser']),
            async submitLogin() {
                this.$refs.loginForm.validate((valid) => {
                    if (valid) {
                        this.login()
                    } else {
                        this.$message.error("登录出错请重新输入");
                        return false;
                    }
                });
            },
            
            async login() {
                console.log("登录信息", this.loginForm.username, this.loginForm.password);
                try {
                    let res = await this.$api.login({
                        user: this.loginForm.username,
                        pwd: this.loginForm.password,
                    });
    
                    if (res && res.data.status === 200) {
                        // Store login info in Vuex
                        console.log(res);
                        console.log('登录接口请求----', res.data, res.data.status);
                        console.log("登录信息", this.loginForm.username, res.data.token);
    
                        this.setUser({
                            username: this.loginForm.username,
                            token: res.data.role,
                            post: res.data.post,
                        });
    
                        // On success, navigate to the homepage  
                        // this.$router.push('/productList');
                        this.$router.push('/');
                    } else {
                        console.log("失败打印", res);
                        console.log("登录失败", res.data);
                        this.$message.error(res.data.error);
                        this.$router.push('/login');
                    }
                } catch (error) {
                    // Catch the error if the API call fails (e.g., backend not reachable)
                    console.error("网络错误或后端服务未连接", error);
                    this.$message.error("网络连接异常，请重启后端服务！");
                }
            }
    
        },
    };
    </script>
    
    <style lang="less" scoped>
    .main {
        background-image: url("@/assets/images/background.jpg");
        background-size: 100%;
        height: 100%;
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: -1;
    }
    
    .loginContainer {
        border-radius: 15px;
        background-clip: padding-box;
        margin: 180px auto;
        width: 350px;
        padding: 15px 35px 15px 35px;
        background: aliceblue;
        border: 1px solid #18181c;
        box-shadow: 0 0 25px #18181c;
    }
    
    .loginTitle {
        margin: 0px auto 48px auto;
        text-align: center;
        font-size: 40px;
    }
    
    .loginRemember {
        text-align: left;
        margin: 0px 0px 15px 0px;
    }
    </style>
    