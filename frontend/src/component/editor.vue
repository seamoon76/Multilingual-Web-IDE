<template>
  <div class="in-coder-panel" :style="{fontSize: myfontSize+'px', lineHeight: lineHighValue}">
    <div class="code_top">
      <button class="filename" v-if="show1==1">
        {{filename}}
        <button class="close" @click="closeCode"><a>&#10005;</a></button>
      </button>
      <el-select  class="code-theme-select" v-model="theme" @change="changetheme">
        <el-option v-for="theme in themes" :key="theme.value" :label="theme.label" :value="theme.value">
        </el-option>
      </el-select>
      <el-input  class="code-font-size" v-model.number="myfontSize" @input="myfontSize = limitValue(myfontSize)" placeholder="12"></el-input>
      <button class="code-font-size-minus" @click="valueMinus"><a class="minus-text">-</a></button>
      <button class="code-font-size-add" @click="valueAdd"><a class="minus-text">+</a></button>
      <button @click="downloadCode" style="position:absolute; height: 23px;right: 20px;">保存</button>

    </div>
    <textarea ref="textarea">

    </textarea>
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
import 'codemirror/theme/darcula.css'
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
import 'codemirror/addon/hint/javascript-hint.js';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/hint/xml-hint.js';
import 'codemirror/addon/hint/sql-hint.js';
import 'codemirror/addon/hint/html-hint.js';
import 'codemirror/addon/hint/css-hint.js';
import 'codemirror/addon/hint/show-hint.js';
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
import {Pos} from "codemirror/src/line/pos";



// 获取全局实例
const CodeMirror = window.CodeMirror || _CodeMirror

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
      filelist : [], //存储曾打开过的文件路径对应的断点、光标位置
      breakpoints : [],   // 断点
      show1: 0, //文件名显示
      myfontSize: 12,//字体大小
      filename:'',   // 文件名
      extname:'',   // 文件后缀
      path:'',  //路径
      lineCurrent: 0, //当前行,行号从1开始
      runLineCurrent:0,
      code: '',   // 内部真实的内容
      mode: 'x-python',   // 默认的语法类型
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
        value: 'darcula',
        label: 'darcula'
      },{
        value: 'paraiso-light',
        label: 'yellow',
      },{
        value: 'rubyblue',
        label: 'blue'
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
    lineHighValue: function() {
      if(this.myfontSize>12){
        return (this.myfontSize+7) + 'px'
      }
      else{
        return '19px'
      }
    }
    },
  methods: {
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
    changeline(val,error = false){
      if(this.runLineCurrent!==0){
        this.coder.removeLineClass(this.runLineCurrent-1,"background","myLineHighlight")
        this.coder.removeLineClass(this.runLineCurrent-1,"background","errorLineHighlight")
      }
      if(error === false){
        this.coder.addLineClass(val-1,"background","myLineHighlight")
      }else{
        this.coder.addLineClass(val-1,"background","errorLineHighlight")
      }
      this.coder.setCursor({line:val-1,ch:0})
      this.coder.setCursor({line:val-1,ch:0})
      this.runLineCurrent = val;
    },

    // 获取断点
    getBreakPoints(){
      this.breakpoints = []
      let maxLine = this.coder.doc.size
      let i = 0;
      this.coder.state.foldGutter = false

      for(i;i<maxLine;i++){
        if(this.gutterMarkers_BreakPoint(i)) {
          this.breakpoints.push(i+1)
        }
      }
      console.log(this.breakpoints)
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
      this.coder = CodeMirror.fromTextArea(this.$refs.textarea, this.options)
      // 编辑器赋值
      this.coder.setValue(this.value || this.code)
      // 支持双向绑定
      this.coder.on('change', (coder) => {
        this.code = coder.getValue()
        if (this.$emit) {
          this.$emit('input', this.code)
        }
      })
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

    // 读入文件
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
      this.extname = ext
      this.filename = file
      this.show1 = 1
      console.log('success');
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
              //获取文件的断点和光标位置，需要放在更改完文件内容之后
              let filenum = _that.filelist.length
              let i = 0
              for (i;i<filenum;i++){
                if(_that.filelist[i]['fullpath'] === (path+file)){
                  //console.log('equal')
                  var linenum = _that.filelist[i]['line']
                  _that.coder.setCursor({line:linenum,ch:0})
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
    // 保存
    downloadCode() {
      //定义文件内容，类型为Blob
      let content = new Blob([this.code])
      var form=new FormData()
      form.append('file',content)
      form.append('filename',this.filename)
      console.log(this.path)
      form.append('path',this.path)

      let filenum = this.filelist.length
      let i = 0
      let flag = 0
      for (i;i<filenum;i++){
        if(this.filelist[i]['fullpath'] === (this.path+this.filename)){
          flag = 1
          this.filelist[i]['line'] = this.coder.getCursor().line
          this.filelist[i]['breakpoints'] = this.getBreakPoints()
        }
      }
      if(flag === 0){
      this.filelist.push({
        'fullpath' : this.path+this.filename,
        'line' : this.coder.getCursor().line,
        'breakpoints' : this.getBreakPoints(),
      })
      }
      console.log(this.filelist)
      axios.post('/save', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } },) // 请求头要为表单
          .then(response => {
            console.log(response.data);
            if (response.data == '1') {
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

    },
    closeCode(){
      this.downloadCode();
      this.filename ='';
      this.extname ='';
      this.code ='';
      this.coder.setValue(this.code);
      this.show1 = 0;
    },

  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus">
.normalLineHighlight
  background-color: #e1f5fe;
  z-index 2
  opacity 0.6
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
    height 93%
    .CodeMirror-code

    .CodeMirror-hints {
      z-index: 10;
    }
    .CodeMirror-match-high-light {
        background-color: #ae00ae;
      }

    .cm-matchhighlight{
      background-color: #b3e5f7;
      opacity 0.6;
      z-index 40;
    }
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
    .close
      position: absolute;
      top:0px;
      width 20px;
      left:95px;
      height 100%;
      border-style: hidden;
      lineHeight: 19px;
  .code-theme-select
    position absolute;
    z-index 20;
    left 120px;
    top -42px;
    max-width 120px;
    lineHeight: 19px;
  .code-font-size
    position absolute;
    z-index 20;
    left 260px;
    top -42px;
    width 50px;
    text-align right;
    lineHeight: 19px;
  .code-font-size-minus
    position absolute;
    border-color #f5f5f5;
    background-color #fafafa;
    z-index 20;
    left 315px;
    top -22px;
    height 17px;
    text-align center;
  .code-font-size-add
    position absolute;
    border-color #f5f5f5;
    background-color #fafafa;
    z-index 20;
    left 315px;
    top -42px;
    height 17px;
    width 20px;
    text-align center;
    .minus-text
      position absolute;
      left 4px;
      top 0;


</style>
