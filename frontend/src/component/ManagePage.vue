<template>

  <body id="body">
    <div class="background">
      <div class="header">
        <h1>全部项目</h1>
        {{ projects.length }}个项目
        <el-button type="primary" @click="show" class="create_btn">New Project</el-button>
        <div class="project_list">
          <ul v-for="(project,idx) in projects" :key="idx">
            <li>
              <span class="task_name">{{ project.taskname }}</span>
              <span class="founder_name">{{ project.foundername }}</span>
              <span class="time">{{ project.time }}</span>
              <span class="acts">
                <el-button type="success" class="open" @click="open(project.id)">打开项目</el-button>
                <el-button type="primary" class="rename" @click="rename(project.id, project.taskname)">重命名</el-button>
                <el-button type="danger" class="delete" @click="delete_project(project.id, project.taskname)">删除项目
                </el-button>
              </span>
              <hr class="hr" />
            </li>
          </ul>
        </div>
      </div>
      <!-- 弹出窗口 -->
      <el-form ref="form" label-width="80px" id="popup" :model="form" class="popup">
        <h2>新项目设置</h2>
        <h3>项目名称</h3>
        <el-form-item label="项目名称">
          <el-input v-model="form.taskname"></el-input>
        </el-form-item>
        <h3>项目作者</h3>
        <el-form-item label="项目作者">
          <el-input v-model="form.foundername"></el-input>
        </el-form-item>
<!--                <el-form-label label="项目名称">-->
<!--          <el-input v-model="taskname"></el-input>-->
<!--        </el-form-label>-->
<!--        <h3>项目作者</h3>-->
<!--        <el-form-label label="项目作者">-->
<!--          <el-input v-model="foundername"></el-input>-->
<!--        </el-form-label>-->
        <h3>请选择语言</h3>
        <el-form-item>
          <el-radio-group v-model="form.language">
            <el-radio label="python" class="language-label"></el-radio>
            <el-radio label="java" class="language-label"></el-radio>
            <el-radio label="c" class="language-label"></el-radio>
            <el-radio label="c++" class="language-label"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-button type="success" id="submit-new-proj" @click="submit">提交</el-button>
      </el-form>
    </div>
  </body>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'

axios.defaults.baseURL = 'http://127.0.0.1:5001'

export default {
  name: "ManagePage",
  data() {
    return {
      projects: [{ taskname: 'test1', foundername: 'user1', time: '1111/11/11 11:11:11' }, { taskname: '1', foundername: '1', time: '1' }],
      form:{
        taskname: "",
        foundername: "",
        language: "",
      }
    };
  },
  created() {
    this.get_project_list()
  },
  mounted() {
    this.get_project_list()
  },
  methods: {
    get_project_list: function () {
      //此处编写初始化拉取代码
      // todo:之后如果要做用户管理，取消下面的注释，把GET方法改为POST
      // var user = Qs.stringify({user : this.user});
      axios.get('/getprojects').then(res => {
        console.log(res.data)
        console.log(this.projects)
        this.projects = res.data;
        console.log(this.projects)
      })
    },
    open: function (id) {
      // 此处编写打开项目代码
      var data = Qs.stringify({ id: id });
      axios.post('/open-project', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(res => {
        if (res.data !== 'error') {
          let path_ = res.data['path']
          console.log('open' + path_ + 'success');
          this.$router.push({
            name: 'edit',
            params: {
              path: `${path_}`,
            }
          });
        } else {
          console.log('qaq');
          this.$message({
            type: 'info',
            message: '打开失败'
          });
        }
      })
    },
    rename: function (id, oldname) {
      // 此处编写重命名代码
      this.$prompt('请输入新的项目名称', '提示', {   // 弹出框用于输入文件名
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        /* inputPattern: /^\S{1,10}$/,
        inputErrorMessage: '文件名长度在1到10之间' */
      }).then(({
        value
      }) => {
        var data = Qs.stringify({ id: id, oldName: oldname, newName: value });
        axios.post('/rename-project', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(res => {
          if (res.data == '1') {
            console.log('success');
            this.get_project_list()
            this.$message({
              type: 'success',
              message: '重命名成功！'
            });
          } else {
            console.log('qaq');
            this.$message({
              type: 'info',
              message: '取消输入'
            });
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
    },
    delete_project: function (id, name) {
      // 此处编写删除项目代码
      this.$confirm('此操作将永久删除' + name + ', 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        var data = Qs.stringify({ id: id })
        axios.post('/delete-project', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(res => {
          if (res.data == '1') {
            this.get_project_list()
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
          } else {
            this.$message({
              type: 'error',
              message: '删除失败!'
            });
          }
        })
      }).catch(() => {
      });
    },
    show: function () {
      var popup = document.getElementById("popup")
      popup.style.display = "block";
    },
    submit: function () {
      var popup = document.getElementById("popup")
      popup.style.display = "none";
      let param = new FormData(); // 创建form对象
      param.append('taskname', this.form.taskname); // 通过append向form对象添加数据
      param.append('foundername', this.form.foundername)
      param.append('language', this.form.language)

      axios.post('/newproject', param, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(res => {
        if (res.data === 'create succeed') {
          console.log('create succeed');
          this.get_project_list()
          this.$message({
            type: 'success',
            message: '文件新建成功！'
          });

        } else {
          console.log("failed");
          this.$message({
            type: 'info',
            message: '新建失败'
          });
        }
      }).catch(() => {
        console.log("fail");
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
      // 此处编写提交新建项目申请代码
    },
  }
}
</script>

<style src="../style/managepage.css">
</style>
