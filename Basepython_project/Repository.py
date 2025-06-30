import glob
import shutil
from os.path import isfile
import requests
import FileAndDirMethod as fd
import os
from Version import Version

arr_commit: Version = []
class Repository:

    def __init__(self,routing_project):
        fd.add_dir(routing_project,".wit")
        fd.add_dir(os.path.join(routing_project,".wit"), "commit")
        fd.add_dir(os.path.join(routing_project, ".wit"), "add")
        fd.add_file(os.path.join(routing_project,".wit"),"log.txt")


def init(routing_project, hascode):
     r = Repository(routing_project)
     routing=os.path.join(routing_project,".wit\\")
     print(f"Initializing repository in: {routing}")
     v = Version("HEAD")
     full_path = os.path.join(routing_project, ".wit/commit")
     fd.add_dir(full_path, str(v.hashCode))
     current_commit = os.path.join(full_path, v.hashCode)
     fd.add_file(current_commit, "log.txt")
     fd.write_file(os.path.join(current_commit, "log.txt"), "HEAD")
     v.routing = os.path.join(full_path, v.hashCode)
     files = os.listdir(routing_project)
     for f in files:
        isdir = os.path.isdir(f)
        if not isdir:
            shutil.copy2(os.path.join(routing_project, f), v.routing)
     hascode = v.hashCode
     arr_commit.append(v)


def add(routing_project,name_files):
       full_path = os.path.join(routing_project, ".wit/add")
       for f in name_files:
         full_path2=os.path.join(routing_project,f)
         shutil.copy(full_path2,full_path)

def commit(routing_project,hascode,message):
      v=Version(message)
      full_path=os.path.join(routing_project,".wit\\commit")
      full_path4 = os.path.join(routing_project, ".wit\\add")
      v.routing=os.path.join(full_path,v.hashCode)
      files1 = os.listdir(full_path)
      paths = [os.path.join(full_path, basename) for basename in files1]
      last_commit = max(paths, key=os.path.getctime)
      fd.add_dir(full_path, v.hashCode)
      current_commit=os.path.join(full_path,v.hashCode)
      if len(files1)==0:
        full_path2 = os.path.join(routing_project, ".wit/add")
        full_path3 = os.path.join(full_path,v.hashCode)
        files = os.listdir(full_path2)
        for f in files:
            isdir: bool = os.path.isdir(f)
            if not isdir:
                shutil.copy2(os.path.join(full_path2, f), full_path3)
      else:
         full_path2=os.path.join(full_path,v.hashCode)
         full_path3=os.path.join(full_path,last_commit)
         files1 = os.listdir(full_path3)
         for f in files1:
            isdir= os.path.isdir(f)
            if not isdir:
                shutil.copy2(os.path.join(full_path3, f), full_path2)
         files2 = os.listdir(full_path4)
         for f in files2:
             isdir: bool = os.path.isdir(f)
             if not isdir:
                 shutil.copy2(os.path.join(full_path4, f), full_path2)
      files = os.listdir(full_path4)
      for f in files:
         os.remove(os.path.join(full_path4,f))
      fd.write_file2(os.path.join(current_commit, "log.txt"), message)
      fd.write_file(os.path.join(routing_project,".wit/log.txt"),v.hashCode)
      fd.write_file(os.path.join(routing_project, ".wit/log.txt"), v.routing)
      fd.write_file(os.path.join(routing_project, ".wit/log.txt"), v.date)
      fd.write_file(os.path.join(routing_project, ".wit/log.txt"), v.message)
      arr_commit.append(v)

def log(routing_project):
    print(fd.read_file(os.path.join(routing_project,".wit/log.txt")))

def checkout(routing_project,name_commit):
    files = os.listdir(routing_project)
    for f in files:
        isdir = os.path.isdir(f)
        if not isdir:
          os.remove(os.path.join(routing_project,f))
    full_path=os.path.join(routing_project,f".wit/commit/{name_commit}")
    files = os.listdir(full_path)
    for f in files:
        shutil.copy2(os.path.join(full_path, f), routing_project)

def status(routing_project):
    full_path = os.path.join(routing_project, ".wit\\commit")
    files = os.listdir(routing_project)
    files2 = os.listdir(full_path)
    paths = [os.path.join(full_path, basename) for basename in files2]
    last_commit = max(paths, key=os.path.getctime)
    full_path3 = os.path.join(full_path, last_commit)
    files1 = os.listdir(full_path3)
    for f in files:
        flag= 0
        isdir = os.path.isdir(f)
        if not isdir:
            for f1 in files1:
                if f1==f:
                    if fd.read_file1(os.path.join(full_path3,f1))==fd.read_file1(os.path.join(routing_project,f)):
                        flag=-1
            if flag==0:
                print(f)





def push(path, server_url):
    add_dir = os.path.join(path, ".wit", "add")
    if not os.path.exists(add_dir):
        print("No '.wit/add' directory found.")
        return
    files = []
    for filename in os.listdir(add_dir):
        file_path = os.path.join(add_dir, filename)
        if os.path.isfile(file_path):
            files.append(("files", (filename, open(file_path, "rb"), "text/plain")))
    if not files:
        print("No files to push.")
        return
    try:
        alert_response = requests.post(f"{server_url}/alerts", files=files)
        print("Alerts:")
        print(alert_response.json())
        files = [("files", (filename, open(os.path.join(add_dir, filename), "rb"), "text/plain"))
                 for filename in os.listdir(add_dir)]
        analyze_response = requests.post(f"{server_url}/analyze", files=files)
        print("\n Analysis:")
        print(analyze_response.json())
    except Exception as e:
        print(f"Failed to push: {e}")
