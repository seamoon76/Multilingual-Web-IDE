// // 注册
// import Vue from 'vue'
// import VueRouter from 'vue-router'
// import HandleError from "@/component/HandleError";
// import ManagePage from "@/component/ManagePage";
// import WebIDE from "@/component/WebIDE";
//
// Vue.use(VueRouter)
//
// // 配置router
// const routes = [
//     {
//         // path: '/',
//         // redirect: '/ManagePage',
//         name: 'ManagePage',
//         component: ManagePage
//     },
//     {
//         path: '/ide',
//         // redirect: '/ide',
//         // // path: '/ide',
//         name: 'ide',
//         component: WebIDE
//     },
//     {
//         path: '/',
//         name: 'HandleError',
//         component: HandleError,
//     },
// ]
//
// const router = new VueRouter({
//     mode: 'history',
//     base: process.env.BASE_URL,
//     routes,
// })
//
// export default router