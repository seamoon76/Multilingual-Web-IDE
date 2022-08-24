# Multilingual-Web-IDE:A web integrated development environment that can support multiple languages

<img src="https://img.shields.io/badge/Vue-^2.6.14-blue.svg"> <img src="https://img.shields.io/badge/Flask-2.2.2-blue"> <img src="https://img.shields.io/badge/CodeMirror-5.65-blue"> <img src="https://img.shields.io/badge/xterm-^4.19.0-blue"> <img src="https://img.shields.io/badge/element_ui-^2.15.9-blue">


<img src="https://img.shields.io/badge/license-MIT-green">

## introduction
A web integrated development environment (IDE) built with Vue and Flask, supports Python, C, and C++ (more languages can be added).

## setup
### backend
Backend cannot run on Windows OS. You should run it on **Linux or macOS**, if your OS is Windows, you can use [WSL](https://docs.microsoft.com/en-us/windows/wsl/about) or [virtual machine](https://www.vmware.com/).

#### prepare

```
pip3 install flask
pip3 install flask_cors
pip3 install flask_sqlalchemy
pip3 install flask_socketio
pip3 install psutil
sudo apt install gdb
```

In `backend/tree/config.py`，specifies `rootPath` of the working directory of the IDE backend, which will be used to store projects. Make sure that the specified path exists.
If you are using WSL, '/mnt/c' means disk "C:" in Windows.
```
class Paths():
    rootPath = '/mnt/c/workspace'
```

#### run backend

```
cd backend
python3 run.py   // use 'python3 run.py' if you are on Linux
```

##### Note

On Linux ,you should use `python3` instead of `python`, because `python` may refer to `python2` by default in Linux.

### frontend
#### Project setup
```
cd frontend
npm install
```

#### Compiles and hot-reloads for development
```
cd frontend
npm run serve
```

#### Compiles and minifies for production
```
cd frontend
npm run build
```

#### Lints and fixes files
```
cd frontend
npm run lint
```

## Usage

see `doc/usage.pdf`

## Advanced:add more language

We have supported 3 lanugage(Python,c,c++), you can add more language as long as this language has command line debugger(such as pdb,gdb). See `doc/add-new-language-api.md`



## Author & Contact

+ 马骐 Email:<span>seamoon2020 at 163 dot com</span>

+ 余欣然
+ 孙骜
+ 潘乐怡
+ 徐霈然
+ 许钧愉


## reference
+ [CodeMirror5](https://codemirror.net/5/)
+ [vue2](https://v2.vuejs.org/)
+ [Flask](https://pypi.org/project/Flask/)
+ [Xterm](https://xtermjs.org/)
+ [Element-UI](https://www.npmjs.com/package/element-ui)
+ [pdb](https://docs.python.org/3/library/pdb.html)
+ [pyxtermjs](https://github.com/cs01/pyxtermjs)
+ [flaskFileManagerVue](https://github.com/flaskFileManagerVue)


## License
MIT