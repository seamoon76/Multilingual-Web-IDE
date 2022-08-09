# backend


## prepare

```
pip3 install flask
pip3 install flask_cors
pip3 install flask_sqlalchemy
pip3 install flask_socketio
```

in `backend/tree/config.py`，Specifies `rootPath` of the working directory of the IDE backend, which will be used to store the project. Make sure that the specified path exists.

```
class Paths():
    rootPath = '/mnt/d/workspace'
    backendRootPath='/mnt/d/2022summer/IDE/web-ide-dev2.6/backend'
```

## run backend

```
cd backend
python3 run.py   // use 'python3 run.py' if you are on Linux
```

#### note

On Linux ,you should use `python3` instead of `python`, because `python` may refer to `python2` by default in Linux.


## advanced
if you want to add more language support to out IDE, go to '/backend/tree/run_order.py' and add running and debug order for your language. There is an example in this file, which is written for python. Then add your new-add function into get_run_cmd() and get_debug_cmd(), which is in 'backend/tree/app.py'.

```python
@app.route('/run', methods=['POST'])
def get_run_cmd():
    # fullpath = os.path.join(Paths.rootPath, run_config['execpath'], run_config['execname'])
    # cmd = ' '.join([sys.executable, fullpath, run_config['execargs']])
    cmd = 'cat LANGUAGE_NOT_SUPPORTED'
    if request.form['language'] == 'python':
        cmd=get_python_run_cmd(run_config)
        # fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
        # cmd = ' '.join([sys.executable, fullpath, run_config['execargs']])+'\n'
        # print(cmd)

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

    ################################################
    # you can add new language support here
    # e.g.:
    #   elif request.form['language'] == 'c':
    #       cmd=get_c_debug_cmd(run_config)
    # 
    # implement get_c_debug_cmd() in 'backend/tree/run_order.py' and import it into this file.
    #
    ################################################
    return json.dumps({'cmd':cmd})
    
```
