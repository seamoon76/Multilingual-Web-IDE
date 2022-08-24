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

We have supported 3 lanugage(Python,c,c++), you can add more language as long as this language has command line debugger(such as pdb,gdb). Here are the steps to add new language support:

### Step 1

Go to '/backend/tree/run_order.py' and add running and debug order for your language. There is an example in this file, which is written for python and c. Named your new-add function as get_xx_run_cmd() and get_xx_debug_cmd()
```python
def get_python_run_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    cmd = ' '.join([sys.executable, fullpath, run_config['execargs']]) + '\n'
    return cmd

def get_c_run_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    name = str(run_config['execname'].split('.')[0])
    cmd = ' '.join([Paths.gcc_path, '-g', fullpath, run_config['execargs'], '-o', name]) + '\n' + './{}'.format(name) + '\n'
    return cmd
    
```
### Step 2

Go to 'backend/tree/app.py', and import your new function get_xx_run_cmd() and get_xx_debug_cmd() from '/backend/tree/run_order.py', which you have implement in Step 1.

```python
@app.route('/run', methods=['POST'])
def get_run_cmd():
    # fullpath = os.path.join(Paths.rootPath, run_config['execpath'], run_config['execname'])
    # cmd = ' '.join([sys.executable, fullpath, run_config['execargs']])
    cmd = 'cat LANGUAGE_NOT_SUPPORTED'
    if request.form['language'] == 'python':
        cmd = get_python_run_cmd(run_config)
        # fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
        # cmd = ' '.join([sys.executable, fullpath, run_config['execargs']])+'\n'
        # print(cmd)
    elif request.form['language'] == 'c':
        cmd = get_c_run_cmd(run_config)
    elif request.form['language'] == 'c++' or request.form['language'] == 'cpp':
        cmd = get_cpp_run_cmd(run_config)

    ################################################
    # you can add new language support here
    # e.g.:
    #   elif request.form['language'] == 'c':
    #       cmd=get_c_run_cmd(run_config)
    #
    # implement get_c_run_cmd() in 'backend/tree/run_order.py' and import it into this file.
    #
    ################################################
    return json.dumps({'cmd': cmd})


@app.route('/debug-order', methods=['POST'])
def get_debug_cmd():
    # fullpath = os.path.join(Paths.rootPath, run_config['execpath'], run_config['execname'])
    # cmd = ' '.join([sys.executable, fullpath, run_config['execargs']])
    cmd = 'cat LANGUAGE_NOT_SUPPORTED'
    if request.form['language'] == 'python':
        cmd = get_python_debug_cmd(run_config)
    elif request.form['language'] == 'c':
        cmd = get_c_debug_cmd(run_config)
    elif request.form['language'] == 'c++' or request.form['language'] == 'cpp':
        cmd = get_cpp_debug_cmd(run_config)
    ################################################
    # you can add new language support here
    # e.g.:
    #   elif request.form['language'] == 'c':
    #       cmd=get_c_debug_cmd(run_config)
    #
    # implement get_c_debug_cmd() in 'backend/tree/run_order.py' and import it into this file.
    #
    ################################################
    return json.dumps({'cmd': cmd})

```

### Step 3

Go to 'frontend/src/component/DebugConfig.vue', and fill in the command line debugger instructions into get_next_order(),get_continue_order() and other functions. And then you need to write String parsing code in function **handleOutput()** to Extract the information returned by the debugger(you can use regular expression).
Such as:

```javascript
get_continue_order(language) {
      if (language === 'python') {
        return 'c\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'c\n'
      }
      // 
      // you can add new language here
      //
      //
    },
```

## Author & Contact

+ 马骐 Email: <span>seam</span><span>oon2020@</span>163.com
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