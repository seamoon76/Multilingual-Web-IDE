<template>
  <div class="in-coder-panel"  >
    <div class="code_top">
      <button class="filename" @click="openCode(tab.id)" v-for="tab in tabs" v-show="tab.show===1" :style="{backgroundColor: changeColor(tab.read)}">
        {{tab.openedFileName}}
        <button class="close" @click="closeCode(tab.id)" :style="{backgroundColor: changeColor(tab.read)}"><a>&#10005;</a></button>
      </button>
      <el-select  class="code-theme-select" v-model="theme" @change="changetheme">
        <el-option v-for="theme in themes" :key="theme.value" :label="theme.label" :value="theme.value">
        </el-option>
      </el-select>
      <el-input  class="code-font-size" v-model.number="myfontSize" @input="myfontSize = limitValue(myfontSize)" placeholder="14"></el-input>
      <button class="code-font-size-minus" @click="valueMinus"><a class="minus-text">-</a></button>
      <button class="code-font-size-add" @click="valueAdd"><a class="minus-text">+</a></button>
      <button @click="downloadCode" style="position:absolute; height: 23px;right: 20px;">保存</button>
    </div>
    <div class="place-holder" v-show="tabs[0].show===0">
      <div class="text-box" >
        <ul class="user-hint">
          <li>右键点击文件树创建新文件</li>
          <li>&emsp;</li>
          <li>Ctrl+C &nbsp; 复制 &emsp;Ctrl+V &nbsp; 粘贴</li>
          <li>Ctrl+Z &nbsp; 撤回 &emsp;Ctrl+S &nbsp; 保存</li>
          <li></li>
        </ul>
        </div>
    </div>
    <div class="coder-area" :style="{fontSize: myfontSize+'px', lineHeight: lineHighValue}"><textarea ref="text"></textarea></div>

  </div>
</template>

<script type="text/ecmascript-6">


// 引入全局实例
import _CodeMirror from 'codemirror'

// 核心样式
import 'codemirror/lib/codemirror.css'
// 引入主题
import 'codemirror/theme/elegant.css'
import 'codemirror/theme/3024-night.css'
import 'codemirror/theme/idea.css'
import 'codemirror/theme/panda-syntax.css'
import 'codemirror/theme/zenburn.css'
import 'codemirror/theme/paraiso-light.css'
import 'codemirror/theme/rubyblue.css'

//jump-to-line
import 'codemirror/addon/search/jump-to-line.js'
// active-line
import 'codemirror/addon/selection/active-line.js'
// styleSelectedText
import 'codemirror/addon/selection/mark-selection.js'
// 引入具体的语法高亮库
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/mode/css/css.js'
import 'codemirror/mode/python/python.js'
import 'codemirror/mode/xml/xml.js';
import 'codemirror/mode/clike/clike.js';
import 'codemirror/mode/markdown/markdown.js';
import 'codemirror/mode/r/r.js';
import 'codemirror/mode/shell/shell.js';
import 'codemirror/mode/sql/sql.js';
import 'codemirror/mode/swift/swift.js';
import 'codemirror/mode/vue/vue.js';
import 'codemirror/keymap/sublime.js';
//选择行 高亮
import "codemirror/addon/selection/active-line.js";
//代码补全提示
import 'codemirror/addon/hint/anyword-hint.js';
import '../hint/javascript-hint.js';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/hint/xml-hint.js';
import 'codemirror/addon/hint/sql-hint.js';
import 'codemirror/addon/hint/html-hint.js';
import 'codemirror/addon/hint/css-hint.js';
import '../hint/show-hint.js';
//自动补全括号，且光标在括号左右侧时，自动突出匹配的括号
import 'codemirror/addon/edit/matchbrackets'
import 'codemirror/addon/edit/closebrackets'
//代码折叠
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/foldcode'
import 'codemirror/addon/fold/foldgutter'
import 'codemirror/addon/fold/brace-fold'
import 'codemirror/addon/fold/comment-fold'
import 'codemirror/addon/fold/xml-fold'
import 'codemirror/addon/fold/indent-fold'
//选中单词时，其他单词时也高亮
import 'codemirror/addon/scroll/annotatescrollbar.js'
import 'codemirror/addon/search/matchesonscrollbar.js'
import 'codemirror/addon/search/match-highlighter.js'
import axios from "axios";
//import {Pos} from "codemirror/src/line/pos";



// 获取全局实例
const CodeMirror = window.CodeMirror || _CodeMirror
CodeMirror.ukeys = []

export default {
  props: {
    // 外部传入的内容，用于实现双向绑定
    value: String,
    // 外部传入的语法类型
    data: {
      type: String,
      default: '',
    }
  },
  data () {
    return {
      rootPath:'',//从后端获取文件根目录
      filelist : [], //存储曾打开过的文件路径对应的断点光标位置
      fileStack: [], //存储最近点击文件
      closetab: 7,  //刚刚关闭的文件标签
      breakpoints : [],   // 断点
      myfontSize: 14,//字体大小
      filename:'',   // 文件名
      extname:'',   // 文件后缀
      path:'',  //路径
      lineCurrent: 0, //当前行,行号从1开始
      runLineCurrent:0,
      code: '',   // 内部真实的内容
      mode: '',   // 默认的语法类型
      theme: 'elegant',   // 默认的主题
      coder: null,  // 编辑器实例
      options: {
        tabSize: 6,   // 缩进格式
        theme: 'elegant',   // 主题
        lineNumbers: true,   // 显示行号
        line: true,
        readOnly: false,
        autoRefresh: true,
        autofocus: true,
        indentUnit: 4,  // 一个块(编辑语言中的含义)应缩进多少个空格(设置为4)
        viewportMargin: 1000, //指定当前滚动到视图中内容上⽅和下⽅要渲染的⾏数
        // 代码折叠
        autoCloseTags: true,
        matchTags: { bothTags: true },
        styleSelectedText: true,
        //styleActiveLine: true, //高亮选中行
        lineWrapping: true, // 是否应滚动或换行以显示长行
        autoCloseBrackets: true, // 自动闭合符号
        matchBrackets: true,  // 在光标点击紧挨{、]括号左、右侧时，自动突出显示匹配的括号 }、]
        foldGutter: true,  // 可将对象折叠，与下面的gutters一起使用
        // 代码高亮只有一个选择时不会自动选择
        hintOptions: {
          completeSingle: false
        },
        gutters: [
          "CodeMirror-lint-markers",
          "CodeMirror-linenumbers",
          "CodeMirror-foldgutter",
          "breakpoints"
        ],
        highlightSelectionMatches: {//显示当前所选单词
          minChars: 2,
          style: "matchhighlight",
          showToken: true
        },
      },
      themes: [{
        value: 'elegant',
        label: 'elegant'
      },{
        value: '3024-night',
        label: '3024-dark'
      },{
        value: 'idea',
        label: 'idea'
      },{
        value: 'panda-syntax',
        label: 'panda-dark'
      },{
        value: 'zenburn',
        label: 'gray'
      },{
        value: 'paraiso-light',
        label: 'yellow',
      },{
        value: 'rubyblue',
        label: 'blue'
      },
      ],
      tabs:[
        {
          id:0,
          openedFileName: '',//存储打开的文件名
          openedFullFilePath:'', //存储打开的（文件名+路径）
          show:0,
          read:0,
        },
        {
          id:1,
          openedFileName: '',
          openedFullFilePath:'',
          show:0,
          read:0,
        },
        {
          id:2,
          openedFileName: '',//存储打开的文件名
          openedFullFilePath:'', //存储打开的（文件名+路径）
          show:0,
          read:0,
        },
        {
          id:3,
          openedFileName: '',//存储打开的文件名
          openedFullFilePath:'', //存储打开的（文件名+路径）
          show:0,
          read:0,
        },
        {
          id:4,
          openedFileName: '',//存储打开的文件名
          openedFullFilePath:'', //存储打开的（文件名+路径）
          show:0,
          read:0,
        },
        {
          id:5,
          openedFileName: '',//存储打开的文件名
          openedFullFilePath:'', //存储打开的（文件名+路径）
          show:0,
          read:0,
        },
        {
          id:6,
          openedFileName: '',//存储打开的文件名
          openedFullFilePath:'', //存储打开的（文件名+路径）
          show:0,
          read:0,
        },
      ],
    }
  },
  mounted () {
    this._initialize() // 初始化
    // 监听cursorActivity事件，实现代码自动提示功能
    //this.editor.on('cursorActivity', () => {
    //  this.editor.showHint()
    //})

  },
  computed: {
    lineHighValue: function () {
      if (this.myfontSize > 12) {
        return (this.myfontSize + 7) + 'px'
      } else {
        return '19px'
      }
    },
  },
  methods: {
    //

    // 文件标签背景颜色改变
    changeColor(val){
      if(val===0){
        return '#E0E0E0'
      }
      else {
        return '#f5f5f5'
      }
    },
    // 字体大小限制
    limitValue(val){
      if(val>25){
        val =25
      }
      return val
    },
    valueAdd(){
      if (this.myfontSize === ''||this.myfontSize > 25 || this.myfontSize < 12){
        this.myfontSize = 12
      }
      if (this.myfontSize < 25)
        this.myfontSize = this.myfontSize+1
    },
    valueMinus(){
      if (this.myfontSize === ''||this.myfontSize > 25 || this.myfontSize < 12){
        this.myfontSize = 12
      }
      if (this.myfontSize > 12)
        this.myfontSize = this.myfontSize-1
    },
    // 跳至调试所在行，并改变该行背景颜色
    changeline(val,changeFile = false,error = false){
      if(changeFile !== false){
        //console.log("打开了新的文件,高亮行为"+val)
        this.coder.setCursor({line:val-1,ch:0})
        this.coder.setCursor({line:val-1,ch:0})
        if(error === false){
          this.coder.addLineClass(val-1,"background","myLineHighlight")
        }else{
          this.coder.addLineClass(val-1,"background","errorLineHighlight")
        }
        this.runLineCurrent = val;
        return;
      }
      this.coder.setCursor({line:val-1,ch:0})
      this.coder.setCursor({line:val-1,ch:0})
      //console.log("跳至调试所在行，并改变该行背景颜色")
      if(this.runLineCurrent!==0){
       // console.log("changeline:"+this.runLineCurrent)
        this.coder.removeLineClass(this.runLineCurrent-1,"background","myLineHighlight")
        this.coder.removeLineClass(this.runLineCurrent-1,"background","errorLineHighlight")
      }
      if(error === false){
        this.coder.addLineClass(val-1,"background","myLineHighlight")
      }else{
        this.coder.addLineClass(val-1,"background","errorLineHighlight")
      }
      this.runLineCurrent = val;
    },
    //调试中止，取消行高亮，取消调试状态的标记
    changeHighLight(){
      if(this.runLineCurrent!==0){
        // console.log("changeline:"+this.runLineCurrent)
        this.coder.removeLineClass(this.runLineCurrent-1,"background","myLineHighlight")
        this.coder.removeLineClass(this.runLineCurrent-1,"background","errorLineHighlight")
      }
      let filenum = this.filelist.length
      let i = 0
      for (i;i<filenum;i++){
        this.filelist[i]['debug'] = 0
        //console.log('调试状态结束，置为零')
      }
      this.runLineCurrent = 0
    },
    // 获取断点
    getBreakPoints(flag = 0, configdirpath = '', configfilename = ''){
      this.breakpoints = []
      if(flag === 0){
        let maxLine = this.coder.doc.size
        let i = 0;
        for(i;i<maxLine;i++){
          if(this.gutterMarkers_BreakPoint(i)) {
            this.breakpoints.push(i+1)
          }
        }
        console.log(this.breakpoints)
      }
      else {
        let filenum = this.filelist.length
        let i = 0
        for (i; i < filenum; i++) {
          if (this.filelist[i]['fullpath'] === (configdirpath + configfilename)) {
            this.breakpoints = this.filelist[i]['breakpoints']
            return this.breakpoints
          }
        }
      }
      return this.breakpoints
    },
    // 区分断点与折叠
    gutterMarkers_BreakPoint(val){
      if(this.coder.lineInfo(val).gutterMarkers){
        for(let k in this.coder.lineInfo(val).handle.gutterMarkers){
          if(k === "breakpoints"){
            if(this.coder.lineInfo(val).handle.gutterMarkers["breakpoints"]!==null){
              return true
            }
          }
        }
      }
      return false
    },
    makeMarker() {
      let marker = document.createElement("div");
      marker.style.color = "#822";
      marker.innerHTML = "●";
      marker.style.marginLeft = "-35px";
      return marker;
    },
    // 初始化
    _initialize () {
      // 初始化编辑器实例，传入需要被实例化的文本域对象和默认配置
      this.coder = CodeMirror.fromTextArea(this.$refs.text, this.options)
      // 编辑器赋值
      this.coder.setValue(this.value || this.code)
      // 支持双向绑定
      this.coder.on('change', (coder) => {
        this.code = coder.getValue()
        if (this.$emit) {
          this.$emit('input', this.code)
        }
      })
      // 获取文件根目录
      axios.get('/getrootpath').then(res => {
        //console.log(res.data)
        this.rootPath = res.data;
        //console.log("-------------获取文件根目录-----------------")
      })
      // 额外配置快捷键，并且为最高优先级
      var map = {
        'Ctrl-S': () =>  {
          this.downloadCode()
        }
      };
      this.coder.addKeyMap(map);

      // 高亮选中行
      this.coder.on('cursorActivity', () => {
        if(this.lineCurrent !== 0){
          this.coder.removeLineClass(this.lineCurrent-1,"background","normalLineHighlight")
        }
        this.lineCurrent = this.coder.getCursor().line + 1
        //console.log(this.lineCurrent)
        this.coder.addLineClass(this.lineCurrent-1,"background","normalLineHighlight")
        //console.log(this.coder.lineInfo(this.lineCurrent-1).bgClass)
      })
      // 代码自动提示
      this.coder.on("inputRead", (cm, obj) => {
        if (obj.text && obj.text.length >0) {
          let c = obj.text[0][obj.text[0].length - 1]
          if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
            this.coder.execCommand("autocomplete");
            // 动态提示
            // 获取用户当前的编辑器中的编写的代码
            var words = cm.getValue() + "";
            // 利用正则取出用户输入的全部以英文字母或下划线开头，由数字、英文字母、下划线组成的单词
            words = words.replace(/[a-z]+[\-|\']+[a-z0-9]+/ig, '').match(/([_a-z0-9]+)/ig);
            // 将获取到的用户的单词传入CodeMirror,并在所有hint文件中做匹配
            CodeMirror.ukeys = words;

            cm.showHint({ completeSingle:false });
          }
        }
      })
      // 画断点
      this.coder.on("gutterClick", (cm, n) => {
        cm.setGutterMarker(n, "breakpoints", this.gutterMarkers_BreakPoint(n)? null: this.makeMarker(n));
      })

    },
    // 更改模式
    changeMode (val) {
      // 修改编辑器的语法配置
      this.coder.setOption('mode', `text/${val}`)

    },
    // 更改主题
    changetheme(val){
      this.coder.setOption('theme', val)
      this.theme = val
    },

    //文件显示处理
    multiFile(path,file){
      let fullpath = path+file
      for(let i = 0;i<7;i++){
        this.tabs[i].read = 0
      }
      for(let i = 0;i<7;i++){
        if(this.tabs[i]["show"] === 1){
          if(this.tabs[i]["openedFullFilePath"]+this.tabs[i]["openedFileName"]===fullpath){
            this.tabs[i].read = 1
            //console.log("change to file "+i)
            return
          }
        }
        else{
          this.tabs[i]["openedFileName"] = file
          this.tabs[i]["show"] = 1
          this.tabs[i]["openedFullFilePath"] = path
          this.tabs[i].read = 1
          return
        }
      }
      this.fileStack.push({
            'path':this.tabs[0]["openedFullFilePath"],
            'filename':this.tabs[0]["openedFileName"]
          }
      )
      //console.log(this.tabs)
      for(let j = 0;j<6;j++){
        this.tabs[j]["openedFileName"] = this.tabs[j+1]["openedFileName"]
        this.tabs[j]["openedFullFilePath"] = this.tabs[j+1]["openedFullFilePath"]
      }
      this.tabs[6]["openedFileName"] = file
      this.tabs[6]["openedFullFilePath"] = path
      this.tabs[6].read = 1
      console.log(this.tabs)
    },
    // 以相对路径读入文件
    /*
    uploadCode(path,file = 'main.py') {
      //if (this.extname==='py'||this.extname==='js'||this.extname==='cpp'){
      //   this.downloadCode()
      // }
      let _that = this
      this.path = path;
      var form=new FormData()
      let num = file.split('.')
      let ext= num[num.length - 1]
      if(num.length <= 1) {
        this.$message({
          message: '请重新点击选择文件传入符合标准的文件',
          type: 'warning'
        });
        return;
      }
      if (ext === 'py') {
        // 修改codemirror的语法类型
        this.changeMode('x-python')
      }
      else if (ext === 'js') {
        this.changeMode('javascript')
      }
      else if (ext === 'cpp'||ext === 'h'||ext === 'c') {
        this.changeMode('x-objectivec')
      }
      else if (ext === 'md') {
        this.changeMode('markdown')
      }
      else if (ext === 'r') {
        this.changeMode('x-rsrc')
      }
      else if (ext === 'css') {
        this.changeMode('css')
      }
      else if (ext === 'html') {
        this.changeMode('html')
      }
      else if (ext === 'sh') {
        this.changeMode('x-sh')
      }
      else if (ext === 'sql') {
        this.changeMode('x-sql')
      }
      else{
        this.changeMode('')
      }
      // 文件显示处理

      this.multiFile(path,file)

      //console.log(this.show)
      this.extname = ext
      this.filename = file

      //console.log('success');
      form.append('fileName', this.filename); // 通过append向form对象添加数据
      form.append('path',this.path);
      axios.post('/getfile',form, {
        responseType: 'blob',
      })
          .then((res) => {
            let blob_data=res.data;
            const reader = new FileReader()
            reader.readAsText(blob_data,'utf-8')
            reader.onload = function () {
              //当读取完成后回调这个函数,然后此时文件的内容存储到了result
              _that.code = this.result
              _that.coder.setValue(_that.code)

              //获取文件的断点和光标位置，这部分需要放在更新完文件内容之后
              let filenum = _that.filelist.length
              let i = 0
              for (i;i<filenum;i++){
                if(_that.filelist[i]['fullpath'] === (path+file)){
                  //console.log('equal')
                  var linenum = _that.filelist[i]['line']
                  _that.coder.setCursor({line:linenum,ch:0})
                  _that.coder.scrollTo(null,_that.filelist[i]['scroll'])
                  _that.breakpoints = _that.filelist[i]['breakpoints']
                  // console.log(_that.breakpoints)
                  let j = 0;
                  for(j;j<_that.breakpoints.length;j++){
                    var n =parseInt(_that.breakpoints[j]) - 1
                    _that.coder.setGutterMarker(n, "breakpoints", _that.makeMarker(n));
                  }
                }
              }
            }
          })

    },
     */
    // 调试时以全路径打开文件
    uploadCodeFullPath(dirpath,file = 'main.py',line_no = null) {

      let _that = this
      this.path = dirpath;
      var form=new FormData()
      let num = file.split('.')
      let ext= num[num.length - 1]
      if(num.length <= 1) {
        this.$message({
          message: '请检查调试跳转到的文件是否是符合标准的文件',
          type: 'warning'
        });
        return;
      }
      if (ext === 'py') {
        // 修改codemirror的语法类型
        this.changeMode('x-python')
      }
      else if (ext === 'js') {
        this.changeMode('javascript')
      }
      else if (ext === 'cpp'||ext === 'h'||ext === 'c') {
        this.changeMode('x-objectivec')
      }
      else if (ext === 'md') {
        this.changeMode('markdown')
      }
      else if (ext === 'r') {
        this.changeMode('x-rsrc')
      }
      else if (ext === 'css') {
        this.changeMode('css')
      }
      else if (ext === 'html') {
        this.changeMode('html')
      }
      else if (ext === 'sh') {
        this.changeMode('x-sh')
      }
      else if (ext === 'sql') {
        this.changeMode('x-sql')
      }
      else{
        this.changeMode('')
      }
      this.multiFile(dirpath,file)
      this.extname = ext
      this.filename = file
      console.log('success');
      form.append('filefullpath', dirpath+this.filename); // 通过append向form对象添加数据

      axios.post('/get-full-path-file',form, {
        responseType: 'blob',
      })
          .then((res) => {
            let blob_data=res.data;
            const reader = new FileReader()
            reader.readAsText(blob_data,'utf-8')
            reader.onload = function () {
              //当读取完成后回调这个函数,然后此时文件的内容存储到了result
              _that.code = this.result
              _that.coder.setValue(_that.code)
              //获取文件的断点和光标位置，这部分需要放在更新完文件内容之后
              let filenum = _that.filelist.length
              let i = 0
              for (i;i<filenum;i++){
                if(_that.filelist[i]['fullpath'] === (dirpath+file)){
                  //console.log('equal')
                  var linenum = _that.filelist[i]['line']
                  _that.coder.setCursor({line:linenum,ch:0})
                  _that.coder.scrollTo(null,_that.filelist[i]['scroll'])
                  _that.breakpoints = _that.filelist[i]['breakpoints']
                  // console.log(_that.breakpoints)
                  let j = 0;
                  for(j;j<_that.breakpoints.length;j++){
                    var n =parseInt(_that.breakpoints[j]) - 1
                    _that.coder.setGutterMarker(n, "breakpoints", _that.makeMarker(n));
                  }
                  if(line_no!==null){
                    //console.log("切换文件"+line_no)
                    _that.filelist[i]['debug'] = parseInt(line_no)
                  }
                  if(_that.filelist[i]['debug']!==0){
                    //console.log("切换文件"+line_no)
                    _that.changeline(_that.filelist[i]['debug'],true);
                  }
                }
              }

            }
          })
    },
    // 保存
    downloadCode() {
      console.log("--------------保存文件----------")
      if(this.tabs[0].show === 0){
        return;
      }
      let filenum = this.filelist.length
      let i = 0
      let flag = 0
      for (i;i<filenum;i++){
        if(this.filelist[i]['fullpath'] === (this.path+this.filename)){
          flag = 1
          this.filelist[i]['line'] = this.coder.getCursor().line
          this.filelist[i]['scroll'] = this.coder.getScrollInfo().top
          this.filelist[i]['breakpoints'] = this.getBreakPoints()
          this.filelist[i]['debug'] = this.runLineCurrent
        }
      }
      if(flag === 0){
        this.filelist.push({
          'fullpath' : this.path+this.filename,
          'line' : this.coder.getCursor().line,
          'scroll': this.coder.getScrollInfo().top,
          'breakpoints' : this.getBreakPoints(),
          'debug':0,
        })
      }
      console.log(this.filelist)
      var myrootpath = this.rootPath+'/'
      var pathBefore = this.path
      this.path = this.path.replace(myrootpath,"")
      if(pathBefore !== this.path) {
        console.log(this.path)
        //定义文件内容，类型为Blob
        let content = new Blob([this.code])
        var form = new FormData()
        form.append('file', content)
        form.append('filename', this.filename)
        form.append('path', this.path)
        this.path = this.rootPath + '/' + this.path
        axios.post('/save', form, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}},) // 请求头要为表单
            .then(response => {
              console.log(response.data);
              if (response.data == '1') {
              //  this.$message({
              //    type: 'success',
              //    message: '文件保存成功！'
              //  });
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
      }
    },
    closeCode(val){
      this.closetab = val;
      this.downloadCode();
      this.filename ='';
      this.extname ='';
      if(this.tabs[val].read === 1) {
        console.log("read === 1")
        this.code = '';
        this.coder.setValue(this.code);
        if (this.tabs[val + 1].show === 1) {
          this.uploadCodeFullPath(this.tabs[val + 1].openedFullFilePath, this.tabs[val + 1].openedFileName)

        }
        else if (val !== 0) {
          console.log(val)
          console.log("val!==0")
          this.tabs[val].show = 0;
          this.tabs[val].read = 0;
          this.uploadCodeFullPath(this.tabs[val - 1].openedFullFilePath, this.tabs[val - 1].openedFileName)
          console.log(this.filename+"   "+this.path)
        }
      }
      for(let i=val;i<6;i++){
        if(this.tabs[i+1].show===1){
          this.tabs[i].show = this.tabs[i+1].show
          this.tabs[i].read = this.tabs[i+1].read
          this.tabs[i].openedFullFilePath = this.tabs[i+1].openedFullFilePath
          this.tabs[i].openedFileName = this.tabs[i+1].openedFileName
        }
        else{
          this.tabs[i].show = 0
        }
      }
      this.tabs[6].show = 0
      //console.log( "close file:" +val+"show:"+this.tabs[val].show+"read:"+this.tabs[val].read)
      //this.show[val] = 0;
    },
    openCode(val){
      if(this.closetab === val){
        return
      }
      //console.log("openfile"+ this.tabs[val].openedFileName)
      if(this.tabs[val].read===0){
        this.downloadCode()
        this.uploadCodeFullPath(this.tabs[val].openedFullFilePath, this.tabs[val].openedFileName)
      }
      this.closetab = 7
    }

  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus">
.normalLineHighlight
  background-color: #e0f2f1;
  z-index 2
  opacity 0.8
.myLineHighlight
  background-color: #FF3D00;
  z-index 3
  opacity 0.2
.errorLineHighlight
  background-color #FF4433;
  opacity 0.6
  z-index 4
.in-coder-panel
  position relative
  height 100%

  .CodeMirror
    z-index 1
    height 100%
    .CodeMirror-code

    .CodeMirror-hints {
      z-index: 10;
    }
    .CodeMirror-gutters{
      width 40px;
      position absolute;
      left 0px;
    }
    .CodeMirror-match-high-light {
      background-color: #ae00ae;
    }
    .cm-matchhighlight{
      background-color: #a7ffeb;
      //opacity 0.6;
      z-index 40;
    }

.coder-area
  height: 93%;
.place-holder
  position absolute;
  height: 100%;
  width :100%;
  background-color #ffffff;
  z-index 20;
  top: 0px;
  left 0px;
  text-align center;
  .text-box
    position:relative;
    top:80px;
  .user-hint
    list-style-type:none;
    color gray;
.code_top
  position: relative;
  width: 100%;
  height: 7%;
  background-color: rgb(211, 209, 209);
  display: flex;
  lineHeight: 19px;

  .filename
    position :relative;
    text-align:center;
    width :120px;
    font-size 12px;
    lineHeight: 19px;
    border-left: 0px;
    border-bottom 0px;

    .close
      position: absolute;
      top:10%;
      width 20px;
      //background-color #e0e0e0;
      left:95px;
      height 80%;
      border-style: hidden;
      lineHeight: 19px;
      z-index 20
  .code-theme-select
    position absolute;
    z-index 20;
    left 120px;
    top -48px;
    max-width 120px;
    lineHeight: 19px;
  .code-font-size
    position absolute;
    z-index 20;
    left 260px;
    top -48px;
    width 50px;
    text-align right;
    lineHeight: 19px;
  .code-font-size-minus
    position absolute;
    border-color #f5f5f5;
    background-color #fafafa;
    z-index 20;
    left 315px;
    top -28px;
    height 17px;
    text-align center;
  .code-font-size-add
    position absolute;
    border-color #f5f5f5;
    background-color #fafafa;
    z-index 20;
    left 315px;
    top -48px;
    height 17px;
    width 20px;
    text-align center;
    .minus-text
      position absolute;
      left 4px;
      top 0;


</style>
