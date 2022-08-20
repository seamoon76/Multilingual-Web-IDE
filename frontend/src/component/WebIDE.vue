<template>

    <body>
        <div class="Tools">
            <div class="Left">
                <el-button type="primary" plain icon="el-icon-user" @click="toManagePage" round>回到首页</el-button>
            </div>
            <div class="debug">
                <!-- button -->
                <el-tooltip effect="dark" content="运行配置" placement="bottom">
                    <el-button plain icon="el-icon-arrow-down" id="config-button" @click="showConfigForm"
                        style="font-size: 20px" round>{{ configform.runningFileName }}</el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="运行" placement="bottom">
                    <el-button id="run" type="success" plain icon="el-icon-video-play" style="font-size: 30px"
                        size="mini" circle :disabled="debugState" @click="runProgram"></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="调试" placement="bottom">
                    <el-button v-show="debugState===false" id="debug-button" type="success" plain icon="el-icon-magic-stick" style="font-size: 30px"
                        size="mini" circle :disabled="debugState" @click="startDebug"></el-button>
                </el-tooltip>
                <!--调试模式下显示-->
                <el-tooltip effect="dark" content="继续执行(continue)" placement="bottom">
                    <el-button v-show="debugState" id="run-till-next-breakpoint" type="success" plain
                        icon="el-icon-d-arrow-right" style="font-size: 30px" size="mini" circle @click="debugContinue"></el-button>
                </el-tooltip>
              <el-tooltip effect="dark" content="单步执行(next)" placement="bottom">
                    <el-button v-show="debugState" id="run-till-next-breakpoint" type="success" plain
                        icon="el-icon-arrow-right" style="font-size: 30px" size="mini" circle @click="debugNext"></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="步入(step)" placement="bottom">
                    <el-button v-show="debugState" id="step-in" plain icon="el-icon-download" style="font-size: 30px"
                        size="mini" circle @click="debugStepIn"></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="步出(return)" placement="bottom">
                    <el-button v-show="debugState" id="step-out" plain icon="el-icon-upload2" style="font-size: 30px"
                        size="mini" circle @click="debugStepOut"></el-button>
                </el-tooltip>

                <el-tooltip effect="dark" content="终止(quit)" placement="bottom">
                    <el-button id="stop" type="danger" plain icon="el-icon-video-pause" style="font-size: 30px"
                        size="mini" circle @click="stopDebuging"></el-button>
                </el-tooltip>
                <!--form-->
                <el-form ref="form" v-model="configform" id="configForm" class="configForm" label-width="80px">
                    <h3>运行配置</h3>
                    <el-form-item label="名称">
                        <el-input v-model="configform.runningFileName"></el-input>
                    </el-form-item>
                    <el-form-item label="路径">
                        <el-input v-model="configform.runningFilePath"></el-input>
                    </el-form-item>
                    <!--<el-form-item label="编译参数">
                        <el-input v-model="configform.compileArgs"></el-input>
                    </el-form-item>-->
                    <el-form-item label="运行参数">
                        <el-input v-model="configform.runningArgs"></el-input>
                    </el-form-item>
                    <!--<el-form-item label="环境变量">
                        <el-input type="textarea" v-model="configform.environmentVariables"></el-input>
                    </el-form-item>-->
                    <el-form-item class="config-form-button">
                        <el-button @click="saveConfigForm">保存</el-button>
                        <el-button @click="closeConfigForm">取消</el-button>
<!--                        <el-button type="primary">保存并运行</el-button>-->
                    </el-form-item>
                </el-form>
            </div>
            <div class="Monitor" v-show="debugState">
              <div>变量</div>
<!--                <el-input v-model="addVariableName" style="width: 160px" size="mini" placeholder="请输入要查看的变量名">-->
<!--                </el-input>-->
<!--                <el-tooltip effect="dark" content="添加变量" placement="top">-->
<!--                    <el-button id="AddVariableButton" plain icon="el-icon-plus" size="mini" circle @click="addVariable">-->
<!--                    </el-button>-->
<!--                </el-tooltip>-->
                <div class="MonitorForm">
                    <div class="VariableFormText">{{ monitoredVariables }}</div>
<!--                    <div class="VariableFormText">{{ monitoredVariables[1]['name'] }}:&nbsp;{{-->
<!--                        monitoredVariables[1]['value'] }}</div>-->
<!--                    <div class="VariableFormText">{{ monitoredVariables[2]['name'] }}:&nbsp;{{-->
<!--                        monitoredVariables[2]['value'] }}</div>-->
<!--                    <div class="VariableFormText">{{ monitoredVariables[3]['name'] }}:&nbsp;{{-->
<!--                        monitoredVariables[3]['value'] }}</div>-->
<!--                    <div class="VariableFormText">{{ monitoredVariables[4]['name'] }}:&nbsp;{{-->
<!--                        monitoredVariables[4]['value'] }}</div>-->
                </div>
            </div>
        </div>
        <div class="Center">
            <div class="DocTree">
                <div class="custom-tree-container">
                    <h3>全部文件</h3>
                    <div class="block">
                        <!-- 使用 scoped slot -->
                        <el-tree 
                            :data="data"
                            node-key="id" 
                            default-expand-all
                            @node-click="handleNodeClick"
                            @node-contextmenu="rightMenu" 
                            :expand-on-click-node="false">
                            <span class="custom-tree-node" slot-scope="{ node, data }">                                
                                <span  :data-obj="JSON.stringify(data)">
                                <i  :class="{
                                    'el-icon-document': data.isdir == 'false',
                                    'el-icon-folder': data.isdir == 'true' && !node.expanded,
                                    'el-icon-folder-opened': data.isdir == 'true' && node.expanded
                                    }"></i>
                                {{ node.label }}</span>
                            </span>
                        </el-tree>
                    </div>
                    <div id="filemenu" v-show="fileMenuVisible" @mouseleave="fileMenuVisible=!fileMenuVisible">
                        <el-card class="box-card">
                            <div class="text item">
                                <el-link icon="el-icon-refresh-right" :underline="false" @click="rename">重命名</el-link>
                            </div>
                            <div class="text item">
                                <el-link icon="el-icon-remove-outline" :underline="false" @click="remove">删除</el-link>
                            </div>
                            <div class="text item">
                                <el-link icon="el-icon-download" :underline="false" @click="download">下载</el-link>
                            </div>
                        </el-card>
                    </div>
                    <div id="foldermenu" v-show="folderMenuVisible" @mouseleave="folderMenuVisible=!folderMenuVisible">
                        <el-card class="box-card">
                            <div class="text item">
                                <el-link icon="el-icon-refresh-right" :underline="false" @click="rename">重命名</el-link>
                            </div>
                            <div class="text item">
                                <el-link icon="el-icon-circle-plus" :underline="false" @click="append_folder">新建目录</el-link>
                            </div>
                            <div class="text item">
                                <el-link icon="el-icon-circle-plus-outline" :underline="false" @click="append_file">新建文件</el-link>
                            </div>
                            <div class="text item">
                                <el-link icon="el-icon-upload2" :underline="false">
                                    上传文件
                                    <input type="file" @change="update" class="hide-btn"/>
                                </el-link>
                            </div>
                            <div class="text item">
                                <el-link icon="el-icon-remove-outline" :underline="false" @click="remove">删除</el-link>
                            </div>
                        </el-card>
                    </div>
                </div>
            </div>
            <div class="IDEAndTerminal">
                <DebugConfig ref="debugger"></DebugConfig>
                <div class="IDE">
                     <editor ref="child"></editor>
                </div>
                <div class="Terminal">
                    <div class="TerminalTop">
                        <div class="TerminalHead" v-for="(terminal,index) in terminals" v-show="index !== 0 && validIndex.includes(index)">
                            <button class="TerminalHeadText" @click="changeCurrentTerminal(index)">Terminal</button>
                            <button class="CloseTerminal" @click="closeTerminal(index)">&#10005;</button>
                        </div>
                        <div class="ConsoleHead" v-show="this.console_num != 0">
                            <button class="TerminalHeadText" @click="changeToConsole">Debug</button>
                            <button class="CloseTerminal" @click="closeConsole">&#10005;</button>
                        </div>
                        <div class="ConsoleHead" v-show="this.output_console_num != 0">
                            <button class="TerminalHeadText" @click="changeToOutputConsole">OutPut</button>
                            <button class="CloseTerminal" @click="closeOutputConsole">&#10005;</button>
                        </div>
                        <button class="add" @click="addTerminal()" v-show="validIndex.length !== 0">+</button>
                    </div>
                    <div class="TerminalBody" ref="terminal" v-for="(terminal, index) in terminals" v-show="index === currentIndex"></div>
                    <div class="TerminalBody" ref="console" v-show="currentIndex == -1"></div>
                    <div class="TerminalBody" ref="output-console" v-show="currentIndex == -2"></div>
                    <div class="TerminalBottom" ref="TerminalBottom">
                        <button class="TerminalButton" @click="createTerminal()">终端</button>
                        <button class="TerminalButton" @click="createOutputConsole()">输出</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="Bottom"></div>
    </body>
</template>

<script>
//*************************doctree*************************/    
import axios from 'axios'
import Qs from 'qs'

let id = 1000;
axios.defaults.baseURL = 'http://127.0.0.1:5001'
//*************************terminal*************************/
import { Terminal } from "xterm"
import { FitAddon } from 'xterm-addon-fit'
import "xterm/css/xterm.css"
import io from 'socket.io-client';
import editor from "@/component/editor";
import DebugConfig from "@/component/DebugConfig";


export default {
  data() {
    return {
      // doctree
      data: [],
      path: '',
      fileList: [],
      nodeData: null,
      optionData: [],
      folderMenuVisible: false,
      fileMenuVisible: false,
      language:'',

      // terminal
      terminals: [""], //最开始长度是1，每次initXterm执行完之后最后一个是不用的
      currentTerminal: '', //current terminal
      currentIndex: 0, //terminals里的index
      validIndex: [1],
      count: 1, //自始至终一共创建了几个终端
      rows: 8,
      cols: 500, //问题：换行也能出现吞行的现象，备用解决方法,把cols设置成无限长
      socket: undefined,
      console_num: 0, //现有调试控制台个数
      debug_console: "", //当前调试控制台
      output_console_num: 0, // 现在的输出窗口的个数
      output_console: "", //当前的输出窗口

      // tools
      configMenuVisible: false,
      debugState: false,
      configform: {
        runningFileName: '',
        runningFilePath: '',
        compileArgs: '',
        runningArgs: '',
        environmentVariables: ''
      },
      addVariableName: '',
      monitoredVariables: ""
    };
  },
  mounted() {
    this.initXterm(0);
  },
  created: function () {
    this.path = this.$route.params.path;
    this.language = this.path.split('_')[1]
    // 获取文件树
    this.getData();
  },
  methods: {
    //*************************doctree*************************/
    // 获取文件路径
    getPath() {
      var path = '';
      var tmpNode = this.nodeData;
      while (tmpNode.parent.label) {
        path = String(tmpNode.parent.label) + '/' + path;
        tmpNode = tmpNode.parent;
      }
      return path;
    },

    // 新建文件
    append_file() {
      this.$prompt('请输入文件名', '提示', {   // 弹出框用于输入文件名
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        /* inputPattern: /^\S{1,10}$/,
                inputErrorMessage: '文件名长度在1到10之间' */
      }).then(({
                 value
               }) => {
        var data = Qs.stringify({path: this.getPath() + this.optionData.label, fileName: value});
        axios.post('/newfile', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
          if (res.data == '1') {
            console.log("1");
            const newChild = {   // 新建一个子节点
              id: id++,
              label: value,
              children: [],
              isdir: 'false'
            };
            if (!this.optionData.children) {   // 如果当前节点没有子节点，就新建一个空的子节点数组，用来存放新建子文件夹
              this.$set(this.optionData, 'children', []);
            }
            this.optionData.children.push(newChild);  // 插入
            //同时展开节点
            if (!this.nodeData.expanded) {
              this.nodeData.expanded = true
            }
            this.$message({
              type: 'success',
              message: '文件新建成功！'
            });
          } else {
            console.log("0");
            this.$message({
              type: 'info',
              message: '新建失败'
            });
          }
        })
      }).catch(() => {
        console.log("fail");
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
    },

    // 新建文件夹
    append_folder() {
      //this.folderMenuVisible = false;
      this.$prompt('请输入文件夹名', '提示', {   // 弹出框用于输入文件名
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        /* inputPattern: /^\S{1,10}$/,
                inputErrorMessage: '文件名长度在1到10之间' */
      }).then(({
                 value
               }) => {
        var data = Qs.stringify({path: this.getPath() + this.optionData.label, dirName: value});
        axios.post('/newdir', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
          if (res.data == '1') {
            console.log('success');
            const newChild = {   // 新建一个子节点
              id: id++,
              label: value,
              children: [],
              isdir: 'true'
            };
            if (!this.optionData.children) {   // 如果当前节点没有子节点，就新建一个空的子节点数组，用来存放新建子文件夹
              this.$set(this.optionData, 'children', []);
            }
            this.optionData.children.push(newChild);  // 插入
            //同时展开节点
            if (!this.nodeData.expanded) {
              this.nodeData.expanded = true
            }
            console.log("here3");
            this.$message({
              type: 'success',
              message: '文件夹新建成功！'
            });
          } else {
            this.$message({
              type: 'info',
              message: '新建失败'
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

    // 删除文件
    remove() {
      this.$confirm('此操作将永久删除' + this.optionData.label + ', 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        var data = Qs.stringify({path: this.getPath(), file: this.optionData.label})
        axios.post('/delete', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
          if (res.data == '1') {
            const parent = this.nodeData.parent;
            const children = parent.data.children || parent.data;
            const index = children.findIndex(d => d.id === this.data.id);
            children.splice(index, 1);
            this.getData()
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

    // 重命名
    rename() {
      this.$prompt('请输入新名称', '提示', {   // 弹出框用于输入文件名
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        /* inputPattern: /^\S{1,10}$/,
                inputErrorMessage: '文件名长度在1到10之间' */
      }).then(({
                 value
               }) => {
        var data = Qs.stringify({path: this.getPath(), oldFileName: this.optionData.label, newFileName: value});
        axios.post('/rename', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
          if (res.data == '1') {
            console.log('rename success');
            this.getData()
            this.optionData.label = value
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

    // 下载文件入口
    download() {
      var data = Qs.stringify({path: this.getPath(), file: this.optionData.label})
      axios.post('/download', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}, {responseType: 'blob'}).then(res => {
        //console.log(res.data)
        this.saveFile(res.data, this.optionData.label)
      })
    },

    // 下载文件到本地
    saveFile(data, fileName) {
      try {
        const blobUrl = window.URL.createObjectURL(new Blob([data]))
        const link = document.createElement('a')
        link.style.display = 'none'
        link.href = blobUrl
        link.setAttribute('download', fileName)
        document.body.appendChild(link);
        link.click()
        document.body.removeChild(link); // 下载完成移除元素
        window.URL.revokeObjectURL(link.href); // 释放掉blob对象
      } catch (e) {
        alert('保存文件出错')
      }
    },

    // 上传文件
    update(e) {
      let file = e.target.files[0];
      let param = new FormData(); // 创建form对象
      param.append('file', file); // 通过append向form对象添加数据
      param.append('path', this.getPath() + this.optionData.label)
      console.log(param.get('file')); // FormData私有类对象，访问不到，可以通过get判断值是否传进去
      axios.post('/upload', param, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}},) // 请求头要为表单
          .then(response => {
            console.log(response.data);
            if (response.data == '1') {
              this.getData()
              this.$message({
                type: 'success',
                message: '文件保存成功！'
              });
            } else {
              this.$message({
                type: 'info',
                message: '文件保存失败，请稍后重试'
              });
            }
          })
          .catch(function (error) {
            console.log(error);
          })
      /* 文件树部分更新 */
      this.getData();
    },

    // 右键菜单
    rightMenu(MouseEvent, object, Node, element) {
      this.optionData = object
      this.nodeData = Node
      console.log(object.isdir)
      debugger
      if (object.isdir == 'false') { // 是文件节点
        this.fileMenuVisible = true;
        console.log("file", this.nodeData.id)
        let menu = document.querySelector("#filemenu");
        menu.style.cssText = "position: fixed; left: " + (MouseEvent.clientX - 10) + 'px' + "; top: " + (MouseEvent.clientY - 25) + 'px; z-index: 999; cursor:pointer;';
      } else { // 是文件夹节点
        this.folderMenuVisible = true;
        console.log("folder", this.nodeData.id)
        let menu = document.querySelector("#foldermenu");
        menu.style.cssText = "position: fixed; left: " + (MouseEvent.clientX - 10) + 'px' + "; top: " + (MouseEvent.clientY - 25) + 'px; z-index: 999; cursor:pointer;';
      }
    },

    getData: function () {
      var data = Qs.stringify({path: this.path});
      axios.post('/', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
        this.data = res.data;
      })
    },

    handleNodeClick(MouseEvent, object, Node, element) {
      this.optionData = object
      this.nodeData = Node
      var path = '';
      var tmpNode = this.optionData;
      while (tmpNode.parent && tmpNode.parent.label) {
        path = String(tmpNode.parent.label) + '/' + path;
        tmpNode = tmpNode.parent;
      }
      if (object.data.isdir == 'false') {
        this.configform.runningFileName = this.optionData.label
        console.log(this.configform.runningFileName)
        this.configform.runningFilePath = path + this.configform.runningFileName
        console.log(this.configform.runningFilePath)
        this.$refs.child.uploadCode(path, this.optionData.label)
        var data = Qs.stringify({
          name: this.configform.runningFileName,
          path: this.configform.runningFilePath,
          runningArgs: this.configform.runningArgs
        })
        axios.post('/saveConfig', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
          console.log(res.data)
          if (res.data == '1') {
            this.$message({
              type: 'success',
              message: '自动加载运行配置'
            })
            this.closeConfigForm()
          } else {
            this.$message({
              type: 'info',
              message: '自动加载运行配置失败'
            })
          }
        })
      }

    },
    //*************************terminal & Debug Console*************************//

    //初始化终端
    initXterm(index) {

      //定义terminal类型
      let term = new Terminal({
        rendererType: "canvas",
        rows: this.rows,
        cols: this.cols,
        convertEol: true,
        disableStdin: false,
        cursorBlink: true,
        windowsMode: true,
        theme: {
          foreground: "#ECECEC",
          background: "black",
          cursor: "help",
          lineHeight: 20
        }
      });

      // 打开terminal实例
      term.open(this.$refs.terminal[index]); //open是用从顶开始打开的，但是terminal是"",terminal1，terminal2,...

      // canvas背景全屏
      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      fitAddon.fit();


      // 窗口大小改变时，触发xterm的resize方法使自适应
      window.addEventListener("resize", resizeScreen);

      function resizeScreen() {
        try {
          fitAddon.fit();
        } catch (e) {
          console.log("e", e.message);
        }
      }

      //前后端通信
      term.onData((data) => {
        socket.emit("pty-input", {input: data});
      });

      let socket = io.connect("http://127.0.0.1:5002/pty");

      socket.on("pty-output", function (data) {

        console.log("new output received from server:", data.output);
        term.write(data.output);
      });

      socket.on("connect", (response) => {

      });

      socket.on("disconnect", (response) => {

      });

      this.socket = socket;
      //保存terminal实例
      this.terminal = term;
      this.terminals.push(term)

      //运行terminal
      this.runFakeTerminal();

    },
    runFakeTerminal() {
      let term = this.terminal;

      if (term._initialized)
        return;
      // 初始化
      term._initialized = true;

    },

    //没有终端时新建终端
    createTerminal() {
      if (this.validIndex.length == 0) {
        this.count += 1
        this.validIndex.push(this.count)
        this.currentIndex = this.count - 1
        this.initXterm(this.count - 1)
      }
      this.count = 1
    },

    //关闭终端
    closeTerminal(index) {
      this.terminals[index].dispose()
      this.validIndex.splice(this.validIndex.indexOf(index), 1)

      //若正好把当前显示的终端删除了，则变成valid中最大的那个
      if (index - 1 == this.currentIndex) {
        this.currentIndex = Math.max.apply(null, this.validIndex) - 1
        this.currentTerminal = this.terminals[this.currentIndex + 1]
      }
      if (this.socket) {
        this.socket.disconnect();
        this.socket = undefined
      }

    },

    //新建终端（点击+号新建）
    addTerminal() {
      this.count += 1
      this.currentIndex = this.count - 1
      this.validIndex.push(this.count)
      this.initXterm(this.count - 1)
    },

    //切换当前显示终端
    changeCurrentTerminal(index) {
      this.currentIndex = index - 1
    },

    createDebugConsole() {
      let that=this
      if(that.currentIndex===-2||that.output_console_num!==0)
      {
        // 输出控制台还开着，关闭
              //console.log(810)
        that.closeOutputConsole()
      }
      if (this.console_num > 0) {
              //console.log(818)
        this.changeToConsole()
        return
      }

      //定义console类型（terminal改动一下）
      let debug_console = new Terminal({
        rendererType: "canvas",
        rows: this.rows,
        cols: this.cols,
        convertEol: true,
        disableStdin: false,
        cursorBlink: true,
        windowsMode: true,
        theme: {
          foreground: "#ECECEC",
          background: "black",
          cursor: "help",
          lineHeight: 20
        }
      });

      // 打开terminal实例
      debug_console.open(this.$refs["console"]);

      // canvas背景全屏
      const fitAddon = new FitAddon();
      debug_console.loadAddon(fitAddon);
      fitAddon.fit();


      // 窗口大小改变时，触发xterm的resize方法使自适应
      window.addEventListener("resize", resizeScreen);

      function resizeScreen() {
        try {
          fitAddon.fit();
        } catch (e) {
          console.log("e", e.message);
        }
      }

      //前后端通信
      debug_console.onData((data) => {
        socket.emit("pty-input", {input: data});
      });

      let socket = io.connect("http://127.0.0.1:5003/pty");

      socket.on("pty-output", function (data) {
        let output=data.output
        //let output=that.$refs.debugger.utf8To16(data.output)
            // console.log(u16)
        console.log("new output received from server:", output);
        console.log('lang:'+that.language)
        that.$refs.debugger.handleOutput(output,that,that.language)
        // //捕获后端发来的串，并处理
        // var output = data.output
        // var last_character = data.output[data.output.length - 2]
        // var tmp = data.output.lastIndexOf("\n")
        // if (last_character == '$') {
        //   if (tmp != -1) {
        //     output = data.output.slice(0, data.output.lastIndexOf("\n") + 1) + "$ "
        //   } else {
        //     output = data.output.substring(data.output.length - 2)
        //   }
        // }
        // let tmp_idx_begin=data.output.lastIndexOf("[my-pdb]")
        //
        //
        //   let tmp_idx = data.output.lastIndexOf("lineno:")
        //   let tmp_idx_num_end = data.output.lastIndexOf(".end")
        //   let left_idx_locals = data.output.lastIndexOf("{")
        //   let right_idx_locals = data.output.lastIndexOf("}")
        //   if (tmp_idx !== -1 && tmp_idx_num_end !== -1) {
        //     try {
        //       let line_no = parseInt(data.output.substring(tmp_idx + 7, tmp_idx_num_end));
        //       that.$refs.child.changeline(line_no);
        //       console.log('change line to ' + line_no)
        //     } catch (e) {
        //       console.error(e)
        //     }
        //     if (left_idx_locals !== -1 && right_idx_locals !== -1) {
        //       let local_variables = data.output.substring(left_idx_locals, right_idx_locals + 1);
        //       if(local_variables.lastIndexOf('{k:v for )')===-1) {
        //         that.monitoredVariables = local_variables;
        //       }
        //
        //     }
        //   }
        //   else if (left_idx_locals !== -1 && right_idx_locals !== -1) {
        //       let local_variables = data.output.substring(left_idx_locals, right_idx_locals + 1);
        //       if(local_variables.lastIndexOf('{k:v for )')===-1) {
        //         that.monitoredVariables = local_variables;
        //       }
        //
        //     }
        //   else {
        //     debug_console.write(output);
        //   }
        //
        //


      });

      socket.on("connect", (response) => {

      });

      socket.on("disconnect", (response) => {

      });

      this.socket = socket;
      //保存console实例
      this.debug_console = debug_console;


      //计数器加1
      this.console_num += 1
      this.currentIndex = -1

      //运行console
      if (debug_console._initialized)
        return;
      // 初始化
      debug_console._initialized = true;
      socket.emit("pty-input", {input: 'PS1="$"\n'});
    },

    createOutputConsole() {
      let that = this
      if(that.currentIndex===-1||that.console_num!==0)
      {
        // 调试控制台还开着，关闭
              //console.log(810)
        if(that.debugState===true)
        {
          that.stopDebuging()
        }
        that.closeConsole()
      }
      if (this.output_console_num > 0) {
              //console.log(818)
        this.changeToOutputConsole()
        return
      }




      //定义console类型（terminal改动一下）
      let output_console = new Terminal({
        rendererType: "canvas",
        rows: this.rows,
        cols: this.cols,
        convertEol: true,
        disableStdin: false,
        cursorBlink: true,
        windowsMode: true,
        theme: {
          foreground: "#ECECEC",
          background: "black",
          cursor: "help",
          lineHeight: 20
        }
      });

      // 打开terminal实例
      output_console.open(this.$refs["output-console"]);

      // canvas背景全屏
      const fitAddon = new FitAddon();
      output_console.loadAddon(fitAddon);
      fitAddon.fit();


      // 窗口大小改变时，触发xterm的resize方法使自适应
      window.addEventListener("resize", resizeScreen);

      function resizeScreen() {
        try {
          fitAddon.fit();
        } catch (e) {
          console.log("e", e.message);
        }
      }

      //前后端通信
      output_console.onData((data) => {
        socket.emit("pty-input", {input: data});
      });

      let socket = io.connect("http://127.0.0.1:5002/pty");

      socket.on("pty-output", function (data) {
        var output = data.output
        console.log("new output received from server:", output);
        //捕获后端发来的串，并处理

        if(output.lastIndexOf('PS1="$"')===-1)
        {
          output_console.write(output);
        }

        // var last_character = data.output[data.output.length - 2]
        // var tmp = data.output.lastIndexOf("\n")
        // if (last_character == '$') {
        //   if (tmp != -1) {
        //     output = data.output.slice(0, data.output.lastIndexOf("\n") + 1) + "$ "
        //   } else {
        //     output = data.output.substring(data.output.length - 2)
        //   }
        // }

      });

      socket.on("connect", (response) => {

      });

      socket.on("disconnect", (response) => {

      });

      this.socket = socket;
      //保存console实例
      this.output_console = output_console;

      //计数器加1
      this.output_console_num += 1
      this.currentIndex = -2

      //运行console
      if (output_console._initialized)
        return;
      // 初始化
      output_console._initialized = true;
      socket.emit("pty-input", {input: 'PS1="$"\n'});
    },

    //将当前页面切换为输出控制台页面
    changeToOutputConsole() {
      this.currentIndex = -2
    },

    //关闭输出控制台
    closeOutputConsole() {
      this.output_console.dispose()
      this.output_console = ""
      this.output_console_num = 0

      this.currentIndex = Math.max.apply(null, this.validIndex) - 1
      this.currentTerminal = this.terminals[this.currentIndex + 1]

      if (this.socket) {
        this.socket.disconnect();
        this.socket = undefined
      }

    },

    //将当前页面切换为调试控制台页面
    changeToConsole() {
      this.currentIndex = -1
    },

    //关闭调试控制台
    closeConsole() {
      this.debug_console.dispose()
      this.debug_console = ""
      this.console_num = 0

      this.currentIndex = Math.max.apply(null, this.validIndex) - 1
      console.log('this.currentIndex'+this.currentIndex)
      this.currentTerminal = this.terminals[this.currentIndex + 1]

      if (this.socket) {
        this.socket.disconnect();
        this.socket = undefined
      }

    },


    //*************************tools*************************/
    toManagePage() {
      // 可以添加提示保存
      this.$router.push('/')
    },


    startDebug() {
      this.$refs.child.downloadCode()
      this.debugState = true;
      var data = Qs.stringify({language: this.language})

      axios.post('/debug-order',data,{headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then((res) => {
        console.log(res.data)
        //this.createDebugConsole();
        if (this.currentIndex == -1) {
          let breakpoints = this.$refs.child.getBreakPoints();
          console.log(breakpoints);
          this.socket.emit("pty-input", {input: res.data.cmd + this.$refs.debugger.get_set_breakpoints_order(breakpoints,this.language)+this.$refs.debugger.start(this.language)});

        } else {
          this.createDebugConsole();
          let breakpoints = this.$refs.child.getBreakPoints();
          console.log(breakpoints)
          this.socket.emit("pty-input", {input: res.data.cmd + this.$refs.debugger.get_set_breakpoints_order(breakpoints,this.language)+this.$refs.debugger.start(this.language)});
        }
      }).catch(() => {
        console.log("fail");
        this.$message({
          type: 'info',
          message: '缺少调试指令'
        });
      });

    },

    debugContinue() {
      if (this.debugState === false) {
        return
      }
      this.socket.emit("pty-input", {input: this.$refs.debugger.get_continue_order(this.language)});
      //this.socket.emit("pty-input", {input: this.$refs.debugger.get_line_order(this.language)});
    },

    debugNext() {
      if (this.debugState === false) {
        return
      }
      this.socket.emit("pty-input", {input: this.$refs.debugger.get_next_order(this.language)});
      //this.socket.emit("pty-input", {input: this.$refs.debugger.get_line_order(this.language)});
    },

    debugStepIn() {
      if (this.debugState === false) {
        return
      }
      ;
      this.socket.emit("pty-input", {input: this.$refs.debugger.get_step_in_order(this.language)});
      //this.socket.emit("pty-input", {input: this.$refs.debugger.get_line_order(this.language)});

    },

    debugStepOut() {
      if (this.debugState === false) {
        return
      }
      ;
      this.socket.emit("pty-input", {input: this.$refs.debugger.get_step_out_order(this.language)});
      //this.socket.emit("pty-input", {input: this.$refs.debugger.get_line_order(this.language)});

    },

    stopDebuging() {
      if (this.debugState === false) {
        return
      }

      this.socket.emit("pty-input", {input: this.$refs.debugger.get_stop_order(this.language)});
      this.debugState = false

    },

    showConfigForm() {
      var configForm = document.getElementById("configForm")
      configForm.style.display = "block";
    },
    closeConfigForm() {
      var configForm = document.getElementById("configForm")
      configForm.style.display = "none";
    },
    saveConfigForm() {
      /* var data = Qs.stringify({ name: this.configform.runningFileName,
            path: this.configform.runningFilePath, compileArgs: this.configform.compileArgs,
            runningArgs: this.configform.runningArgs, environmentVariables: this.configform.environmentVariables}) */
      var data = Qs.stringify({
        name: this.configform.runningFileName,
        path: this.configform.runningFilePath,
        runningArgs: this.configform.runningArgs
      })
      axios.post('/saveConfig', data, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
        console.log(res.data)
        if (res.data == '1') {
          this.$message({
            type: 'success',
            message: '运行配置成功'
          })
          this.closeConfigForm()
        } else {
          this.$message({
            type: 'info',
            message: '保存失败'
          })
        }
      })
    },
    runProgram() {
      this.$refs.child.downloadCode()
      var data = Qs.stringify({language: this.language})

      axios.post('/run',data,{headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then((res) => {
        console.log(res.data)
        //this.createDebugConsole();
        if (this.currentIndex == -2) {
          //console.log(1083)
          this.socket.emit("pty-input", {input: res.data.cmd});
        } else {
          this.createOutputConsole();
          this.socket.emit("pty-input", {input: res.data.cmd});
        }
      }).catch(() => {
        console.log("fail");
        this.$message({
          type: 'info',
          message: '缺少运行指令'
        });
      });
    },

    addVariable() {
      // 提交要查看的变量名,更新monitoredVariables
      this.addVariableName = ''
    },


  },
    components: {Terminal, editor,DebugConfig}
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped src="../style/style.css">
</style>
<style scoped src="../style/doctree.css">
</style>
<style scoped src="../style/terminal.css">
</style>
<style scoped src="../style/tools.css">
</style>
