import os
import sys
from config import Paths


def get_python_run_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    cmd = ' '.join([sys.executable, fullpath, run_config['execargs']]) + '\n'
    return cmd

def get_python_debug_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    cmd = ' '.join(
        [sys.executable, Paths.backendRootPath + '/onlinePdb/mypdb.py', fullpath, run_config['execargs']]) + '\n'
    return cmd