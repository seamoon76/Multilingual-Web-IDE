# -*- coding:utf-8 -*-
import datetime
import random

from flask import Flask, request, send_file, render_template
from flask_cors import *
import json
from config import Paths
from file_operation import remove_file, rename_file, getfiletree
import os
# sql
from flask_sqlalchemy import SQLAlchemy
import sys
import time
import shutil
from run_order import get_python_run_cmd, get_python_debug_cmd, get_c_run_cmd, get_cpp_run_cmd, get_c_debug_cmd, \
    get_cpp_debug_cmd

app = Flask(__name__)
CORS(app)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

# 注意app的config要在创建db之前
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

run_config = {'execname': '', 'execpath': '', 'execargs': ''}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(60))
    foundername = db.Column(db.String(20))
    time = db.Column(db.String(20))  # 最后一次修改的时间
    language = db.Column(db.String(20))
    path = db.Column(db.String(60))
    log_path = db.Column(db.String(60))

    def __getdict__(self):
        return {'taskname': self.taskname, 'foundername': self.foundername, 'time': self.time,
                'language': self.language, 'id': self.id, 'log_path': self.log_path}

    def __repr__(self):
        return str(
            {'taskname': self.taskname, 'foundername': self.foundername, 'time': self.time, 'language': self.language,
             'log_path': self.log_path})


# @app.cli.command()
# @click.option('--drop', is_flag=True, help='Create after drop.')
# def initdb(drop):
#     if drop:
#         db.drop_all()
#     db.create_all()
#     click.echo('Initialized database.')

@app.route('/', methods=['GET', 'POST'])
def lists():
    convertedPath = Paths.rootPath
    project_name = ''
    if (request.form['path']):
        project_name = request.form['path']
        print(request.form['path'])
        # convertedPath = os.path.join(convertedPath, request.form['path'])
        convertedPath = os.path.join(convertedPath, request.form['path'])
    return json.dumps(getfiletree(convertedPath, project_name))  # json.dumps(get_dir_list(convertedPath))


@app.route('/delete', methods=['GET', 'POST'])
def delete_f():
    convertedPath = Paths.rootPath
    result = 0
    if (request.form['path']):
        convertedPath = os.path.join(convertedPath, request.form['path'])
    fullPathOfFile = convertedPath + '/' + request.form['file']
    if (remove_file(fullPathOfFile)):
        result = 1
        project = Project.query.filter(Project.path == request.form['path'].split('/')[0]).first()
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.time = time
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',Delete file/directory,name:' + str(request.form['file']) + '.\n')
        db.session.commit()
    return json.dumps(result)


@app.route('/rename', methods=['GET', 'POST'])
def rename():
    convertedPath = Paths.rootPath
    result = 0
    if (request.form['path']):
        convertedPath = os.path.join(convertedPath, request.form['path'])
    oldfullPathOfFile = convertedPath + '/' + request.form['oldFileName']
    newfullPathOfFile = convertedPath + '/' + request.form['newFileName']
    if (rename_file(oldfullPathOfFile, newfullPathOfFile)):
        result = 1
        project = Project.query.filter(Project.path == request.form['path'].split('/')[0]).first()
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.time = time
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',Rename file/directory,Oldname:' + str(
                request.form['oldFileName']) + ',Newname:' + str(request.form['newFileName']) + '.\n')
        db.session.commit()
    return json.dumps(result)


@app.route('/newdir', methods=['GET', 'POST'])
def newdir():
    convertedPath = Paths.rootPath
    res = 0
    if (request.form['path']):
        convertedPath = os.path.join(convertedPath, request.form['path'])
    dirFullPath = convertedPath + '/' + request.form['dirName']
    os.mkdir(dirFullPath)
    if os.path.exists(dirFullPath):
        res = 1
    if res == 1:
        project = Project.query.filter(Project.path == request.form['path'].split('/')[0]).first()
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.time = time
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',Create new directory,dirname:' + str(request.form['dirName']) + '.\n')
        db.session.commit()
    return json.dumps(res)


@app.route('/newfile', methods=['GET', 'POST'])
def newfile():
    convertedPath = Paths.rootPath
    result = 0
    if (request.form['path']):
        convertedPath = os.path.join(convertedPath, request.form['path'])
    fileFullPath = convertedPath + '/' + request.form['fileName']
    try:
        newfile = open(fileFullPath, 'x')
        newfile.close()
        project = Project.query.filter(Project.path == request.form['path'].split('/')[0]).first()
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.time = time
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',Create new file,filename:' + str(request.form['fileName']) + '.\n')
        db.session.commit()
        result = 1
    except:
        result = 0

    return json.dumps(result)


@app.route('/download', methods=['GET', 'POST'])
def downloadfile():
    convertedPath = Paths.rootPath
    result = 0
    if (request.form['path']):
        convertedPath = os.path.join(convertedPath, request.form['path'])
    fileFullPath = convertedPath + '/' + request.form['file']
    if os.path.exists(fileFullPath):
        result = 1
        project = Project.query.filter(Project.path == request.form['path'].split('/')[0]).first()
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',Download file,filename:' + str(request.form['file']) + '.\n')
        return send_file(fileFullPath)
    return json.dumps(result)


@app.route('/upload', methods=['POST'])
def uploadfile():
    file_obj = request.files['file']
    if file_obj is None:
        return json.dumps("no file uploaded")

    convertedPath = Paths.rootPath
    result = 0
    if request.form['path']:
        saveDirFullPath = os.path.join(convertedPath, request.form['path'])
        if os.path.exists(saveDirFullPath):
            file_obj.save(os.path.join(saveDirFullPath, file_obj.filename))
            result = 1
            project = Project.query.filter(Project.path == request.form['path'].split('/')[0]).first()
            time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            project.time = time
            log_path = project.log_path
            with open(log_path, 'a') as f:
                f.write('Time:' + str(time) + ',New file uploaded.\n')
            db.session.commit()
    return json.dumps(result)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# 新建项目
@app.route('/newproject', methods=['POST'])
def new_project():
    if request.method == 'POST':
        taskname = request.form.get('taskname')
        foundername = request.form.get('foundername')
        last_modify_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        language = request.form.get('language')
        save_path = taskname + '_' + language + '_project'
        if os.path.exists(os.path.join(Paths.rootPath, save_path)):
            save_path = save_path + '_' + str(random.randint(1, 10))
        os.mkdir(os.path.join(Paths.rootPath, save_path))
        log_path = os.path.join(Paths.rootPath, save_path, 'task_log.log')
        with open(log_path, 'a') as f:
            f.write('Time:' + str(last_modify_time) + ',FounderName:' + str(
                foundername) + ',Create this task,TaskName:' + str(taskname) + '.\n')
        if not taskname or not foundername or not last_modify_time or len(last_modify_time) > 20 or len(
                taskname) > 60 or len(foundername) > 20:
            return json.dumps('error')

        # 保存表单数据到数据库
        project = Project(taskname=taskname, foundername=foundername, time=last_modify_time, language=language,
                          path=save_path, log_path=log_path)  # 创建记录
        db.session.add(project)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        return json.dumps('create succeed')
    return json.dumps('error')


# 删除项目
@app.route('/delete-project', methods=['POST'])
def delete_project():
    if request.method == 'POST':
        id = request.form.get('id')
        if not id:
            return json.dumps('error')
        # 保存表单数据到数据库
        project = Project.query.get_or_404(id)
        shutil.rmtree(os.path.join(Paths.rootPath, project.path))
        db.session.delete(project)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        return json.dumps('1')
    return json.dumps('error')


# 重命名项目
@app.route('/rename-project', methods=['POST'])
def rename_project():
    if request.method == 'POST':
        id = request.form.get('id')
        newName = request.form.get('newName')
        if not id or not newName:
            return json.dumps('error')
        # 保存表单数据到数据库
        project = Project.query.get_or_404(id)
        oldname = project.taskname
        project.taskname = newName
        # 写入log
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.time = time
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',this task has been renamed. Oldname:' + str(oldname) + ',Newname:' + str(
                newName) + '.\n')
        db.session.commit()  # 提交数据库会话
        return json.dumps('1')
    return json.dumps('error')


# 打开项目
@app.route('/open-project', methods=['POST'])
def open_project():
    if request.method == 'POST':
        id = request.form.get('id')
        if not id:
            return json.dumps('error')
        # 保存表单数据到数据库
        project = Project.query.get_or_404(id)
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',this task has been opened.\n')
        project_path = str(project.path)
        return json.dumps({'path': project_path})
    return json.dumps('error')


@app.route('/getprojects', methods=['GET', 'POST'])
def get_project_list():
    project_list = [i.__getdict__() for i in Project.query.all()]
    print(project_list)
    return json.dumps(project_list)


# 生成虚拟数据
def forge():
    """
    Generate fake data.
    :return:
    """
    db.create_all()
    projects = [
        {'taskname': "task133", 'foundername': "user1", 'time': "1111/11/11 11:11:11", 'language': "python"}
    ]

    for m in projects:
        project = Project(taskname=m['taskname'], foundername=m['foundername'], time=m['time'], language=m['language'])
        db.session.add(project)
    db.session.commit()


# 保存来自codemirror的代码
@app.route("/save", methods=['post'])
def savefile():
    files = request.files
    file_obj = files.get('file')
    if file_obj is None:
        return json.dumps("no file uploaded")
    file_name = request.form['filename']
    convertedPath = Paths.rootPath
    result = 0
    if (request.form['path']):
        saveDirFullPath = os.path.join(convertedPath, request.form['path'])
        project = Project.query.filter(Project.path == request.form['path'][:-1]).first()
        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.time = time
        log_path = project.log_path
        with open(log_path, 'a') as f:
            f.write('Time:' + str(time) + ',files have been saved.\n')
        db.session.commit()
        if os.path.exists(saveDirFullPath):
            file_obj.save(os.path.join(saveDirFullPath, file_name))
            result = 1
    return json.dumps(result)


# 从后端获取文件
@app.route('/getfile', methods=['POST'])
def get_file():
    convertedPath = Paths.rootPath
    result = 0
    if request.form['path'] and request.form['fileName']:
        convertedPath = os.path.join(convertedPath, request.form['path'])
    fileFullPath = convertedPath + '/' + request.form['fileName']
    f = open(fileFullPath, 'rb')
    return f.read()

# 从后端获取文件
@app.route('/get-full-path-file', methods=['POST'])
def get_full_path_file():
    if request.form['filefullpath']:
        fileFullPath = request.form['filefullpath']
        f = open(fileFullPath, 'rb')
        return f.read()
    else:
        print('cannot find file')
        return None



def set_run_config(execname, execpath, execargs):
    run_config['execname'] = execname
    run_config['execpath'] = execpath
    run_config['execargs'] = execargs


# 保存运行配置
@app.route('/saveConfig', methods=['POST'])
def save_config():
    result = 0
    if request.form['name'] and request.form['path']:
        set_run_config(request.form['name'], request.form['path'], request.form['runningArgs'])
        result = 1
    return json.dumps(result)


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


if __name__ == '__main__':
    # app.debug = True
    # 如果发现目录下没有data.db文件，需要创建它(取消下面这行注释），即第一次启动需要进行create_all()
    if os.path.exists('data.db') is not True:
        db.create_all()
    app.run(host='127.0.0.1', port=5001, debug=True)  # , debug=True, threaded=True
