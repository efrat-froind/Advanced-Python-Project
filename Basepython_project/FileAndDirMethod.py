import os
def add_dir(routing,name):
     full_path=os.path.join(routing,name)
     if not os.path.exists(full_path):
        os.mkdir(full_path)
     else:
        raise Exception("The folder already exists.")

def add_file(routing,name):
      full_path = os.path.join(routing, name)
      if not os.path.exists(full_path):
         with open(full_path,"w") as file:
             pass
         file.close()
      else:
         raise Exception("the routing does not exist")

def read_file(routing):
    try:
      if os.path.exists(routing):
         with open(routing,"r") as file:
             print(file.read())
         file.close()
    except:
        raise Exception("the routing does not exist")

def read_file1(routing):
    try:
      if os.path.exists(routing):
         with open(routing,"rb") as file:
             return file.read()
    except:
        raise Exception("the routing does not exist")


def write_file(routing,str):
      if os.path.exists(routing):
         with open(routing,"a") as file:
            file.write(f"{str}\n")
         file.close()
      else:
          raise Exception("the routing does not exist")


def write_file2(routing, str):
    if os.path.exists(routing):
        with open(routing, "w") as file:
            file.write(f"{str}\n")
        file.close()
    else:
        raise Exception("the routing does not exist")


def delete_dir(path):
        os.rmdir(path)

