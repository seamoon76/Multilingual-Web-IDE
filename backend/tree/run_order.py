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
        [sys.executable, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/onlinePdb/mypdb.py', fullpath, run_config['execargs']]) + '\n'
    return cmd

def get_c_run_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    name = str(run_config['execname'].split('.')[0])
    cmd = ' '.join([Paths.gcc_path, '-g', fullpath, run_config['execargs'], '-o', name]) + '\n' + './{}'.format(name) + '\n'
    return cmd

def get_c_debug_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    name = str(run_config['execname'].split('.')[0])
    cmd = ' '.join([Paths.gcc_path, '-g', fullpath, run_config['execargs'], '-o', name]) + '\n' + '{}'.format(Paths.gdb_path)+' -silent {}'.format(name) + '\n'
    return cmd

def get_cpp_run_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    name = str(run_config['execname'].split('.')[0])
    cmd = ' '.join([Paths.gpp_path, '-g', fullpath, run_config['execargs'], '-o', name]) + '\n' + './{}'.format(name) + '\n'
    return cmd

def get_cpp_debug_cmd(run_config):
    fullpath = os.path.join(Paths.rootPath, run_config['execpath'])
    name = str(run_config['execname'].split('.')[0])
    cmd = ' '.join([Paths.gpp_path, '-g', fullpath, run_config['execargs'], '-o', name]) + '\n' + '{}'.format(Paths.gdb_path)+' -silent {}'.format(name) + '\n'
    return cmd