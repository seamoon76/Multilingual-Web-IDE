import multiprocessing
import os
import sys
from tree.config import Paths

def run_backend(filepath:str):
    os.system(sys.executable + ' ' +filepath)



if __name__ == "__main__":
    backend_file_paths = [Paths.backendRootPath + os.path.sep + f for f in ['tree/app.py', 'webIdeXterm.py', 'debug_console.py', 'output_console.py']]
    for path in backend_file_paths:
        if os.path.exists(path) is not True:
            print('cannot find ' + path)
            raise FileNotFoundError
        else:
            print('running '+path)

    pool = multiprocessing.Pool(3)
    pool.map(run_backend, backend_file_paths)

