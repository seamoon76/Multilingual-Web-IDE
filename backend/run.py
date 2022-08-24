import multiprocessing
import os
import sys
from tree.config import Paths

def run_backend(filepath_port):
    filepath,port=filepath_port

    if 'tree/app.py' in filepath:
        os.system(sys.executable + ' ' + filepath)
    elif 'webIdeXterm.py' in filepath:
        os.system(sys.executable + ' ' +filepath + ' --port '+port)
    else:
        print('cannot run'+sys.executable + ' ' +filepath + ' --port '+port)



if __name__ == "__main__":
    if os.path.exists(Paths.rootPath) is not True:
        os.makedirs(Paths.rootPath)
    backend_file_paths = [(os.path.join((os.path.dirname(os.path.abspath(__file__))),f),str(p)) for f,p in zip(['tree/app.py', 'webIdeXterm.py','webIdeXterm.py','webIdeXterm.py'],[5001,5002,5003,5004])]
    for path,p in backend_file_paths:
        if os.path.exists(path) is not True:
            print('cannot find ' + path)
            raise FileNotFoundError
        else:
            print('running '+path)

    pool = multiprocessing.Pool(4)
    pool.map(run_backend, backend_file_paths)

