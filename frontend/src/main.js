import Vue from 'vue'
import App from './App.vue'
//导入elementUI
import ElementUI from "element-ui"
//导入element css
import 'element-ui/lib/theme-chalk/index.css'
import VueRouter from 'vue-router';
import ManagePage from "@/component/ManagePage";
import WebIDE from "@/component/WebIDE";
import HandleError from "@/component/HandleError";
import editor from "@/component/editor";

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.config.productionTip = false

const routes = [
    { path: 'index', component: ManagePage},
    { path: '/', redirect: '/ManagePage'},
    { path: '/ManagePage', component: ManagePage },
    { path: '/edit/:path', name:'edit',component: WebIDE},
    { path: '404', component: HandleError},
    {path: '/editor',component: editor}
]
const router = new VueRouter({
        routes
    })
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')



