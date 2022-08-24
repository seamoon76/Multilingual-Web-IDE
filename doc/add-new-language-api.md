
# add more language

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