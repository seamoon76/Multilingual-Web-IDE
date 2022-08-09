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



