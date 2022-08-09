from flask import Flask,request,jsonify
from flask_cors import *
import json
from config import *
from utils import *
import os
import shutil
from datetime import datetime

def getfiletree(dirFullPathm,project_name):
    id_counter = [0]
    project_tree={'children':[]}
    project_tree['label']=project_name
    project_tree['id'] = 0
    project_tree['isdir'] = 'true'
    # 制作目录json
    def getDirectoryTree(folder,id=id_counter):
        dirtree = {'children':[]}
        if os.path.isfile(folder):
            id[0]=id[0]+1
            return {'label':os.path.basename(folder),'id':str(id[0]),'isdir':'false','children':[]}
        else:
            basename = os.path.basename(folder)
            dirtree['label'] = basename
            id[0]=id[0]+1
            dirtree['id'] = id[0]
            dirtree['isdir'] = 'true'
            for item in os.listdir(folder):
                dirtree['children'].append(getDirectoryTree(os.path.join(folder,item),id))
            return dirtree
    project_tree['children']=list(getDirectoryTree(dirFullPathm).values())[0]
    res = []
    res.append(project_tree)
    print(res)
    return res


def remove_file(filePath):
    if (os.path.isdir(filePath)):
        try:
            shutil.rmtree(filePath)
        except:
            shutil.rmtree(filePath)
    else:
        os.remove(filePath)
    return not os.path.exists(filePath)

def rename_file(oldName,newName):
    try:
        shutil.move(oldName,newName)
    except:
        print("rename file error")
    return os.path.exists(newName)

