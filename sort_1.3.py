#Kareem Taha
#2/12/2021
#
#Sorter
#Builds containers depending on filetypes and moves files to appropriate folders.
#1.0 automatically sorts downloads folder into containers as a .py script
#1.1 adds the ability to both change and print directories. Also adds user-input functionality
#1.2 adds editing extensions and buckets. WIP: Moving edit/config functionality to .ini with file I/O
#1.3 fixes a bug where the program would crash with no 
import os
import shutil
import configparser


table = {  "folder":"folders",
            "exe":"executables",
            "bat":"scripts",
            "py":"scripts",
            "zip":"archives",
            "rar":"archives",
            "tar":"archives",
            "tgz":"archives",
            "iso":"disk-images",
            "pdf":"documents",
            "docx":"documents"
            }

types = ["unknown","folders","executables","scripts","archives","disk-images", "documents"]

def sort_dir():
    cd = os.getcwd()
    dir_contents = os.listdir()    
    for bucket in types:
        if bucket not in dir_contents: os.mkdir(bucket)
    for item in dir_contents:
        path = os.path.join(cd, item)
        if os.path.isfile(path): ext = item.rsplit(".",1)[1]
        elif os.path.isdir(path):
            if item in types: continue
            ext = "folder"
        newpath = os.path.join(cd, table.get(ext, "unknown"))
        try:
            shutil.move(path, newpath)
        except shutil.Error:
            print("No biggie")

def main():
    print("CD: " + os.getcwd())
    config = configparser.ConfigParser()
    config.read('C:\Users\karee\onedrive\pywork\sort\config.ini')
    types = config['table']
    print(types)
    print(str(config["table"]))
    choice = 0
    while(choice != 1 and choice != 2 and choice != 3 and choice != 4):
        choice = input("1. Sort CD\n2. Print CD\n3. Change CD\n4. Edit Types\n5. Exit\n")
        choice = int (choice)
    if choice == 1: 
        sort_dir()
        main()
    if choice == 2: 
        print_dir()
        main()
    if choice == 3: 
        change_dir()
        main()
    if choice == 4:
        edit()
        main()
    return

def change_dir():
    choice = 0
    while (choice != 1 and choice != 2 and choice != 3):
        print("CD: " + os.getcwd())
        choice = input("1: List Contents\n2: Change Directory\n3: Exit\n")
        choice = int (choice)
    if choice == 1: 
        print_dir()
        change_dir()
    if choice == 2: 
        pick_dir()
        change_dir()
    if choice == 3: return

def pick_dir():
    choice = 0
    while (choice != 1 and choice != 2 and choice != 3):
        choice = input("1: By Path\n2: Child Dir\n3: Parent Dir\n4: Exit\n")
        choice = int (choice)
    if choice == 1: 
        path = input("Enter Path:")
        if os.path.isdir(path): os.chdir(path)
    elif choice == 2:
        print_dir()
        path = input("Enter a child dir (.. to escape)")
        if path == "..": return
        path = os.path.join(os.getcwd(), path)
        if os.path.isdir(path): os.chdir(path)
    elif choice == 3: os.chdir(os.path.split(os.getcwd())[0])
    elif choice == 4: return

def print_dir(only_dir = False, only_file = False):
    contents = os.listdir()
    print("=\nCD: " + os.getcwd() + "\n=\n")
    for item in contents:
        path = os.path.join(os.getcwd(), item)
        if only_file: 
            if os.path.isfile(path): print("File: " + item)
        elif only_dir:
            if os.path.isdir(path): print("Dir: " + item)
        else: print(item)
    print("")

def edit():
    choice = 0
    while(choice != 1 and choice != 2 and choice != 3):
        choice = input("1. Edit Buckets\n2. Edit Extensions\n3. Exit\n")
        choice = int (choice)
    if choice == 1: edit_buckets() 
    elif choice == 2: edit_ext()
    return
    
def edit_buckets():
    choice = 0
    while(choice != 1 and choice != 2 and choice != 3 and choice != 4):
        choice = input("1. Add Bucket\n2. Edit Bucket\n3. Remove Bucket\n4. Exit\n")
        choice = int (choice)

    if choice == 1: types.append(input("Bucket Name?\n"))
    elif choice == 2: 
        sel = input("Select a bucket")
        while sel not in types:
            sel = input("Not a bucket; select a bucket")
        bucket = input("Rename to:\n")
        types[types.index(sel)] = bucket
    elif choice == 3:
        sel = input("Select a bucket")
        while sel not in types:
            sel = input("Not a bucket; select a bucket")
        types.remove(sel)
    return

def edit_ext():
    choice = 0
    while(choice != 1 and choice != 2 and choice != 3 and choice != 4):
        choice = input("1. Add Ext\n2. Edit Ext\n3. Remove Ext\n4. Exit\n")
        choice = int (choice)

    if choice == 1:
        ext = input("Type extension:\n")
        print(types)
        choice = input("Pick an associated filetype\n")
        while choice not in types:
            choice = input("Incorrect; pick an associated filetype\n")
        table[ext] = choice
    if choice == 2:
        sel = input("Select an extension\n")
        while sel not in table.keys():
            sel = input("Not an ext; select a file extension\n")
        bucket = input("Rename to:\n")
        value = table.pop(sel)
        table[bucket] = value
    if choice == 3:
        for key, ans in table.items():
            print(key+":"+ans)
        sel = input("Select an extension\n")
        while sel not in table.keys():
            sel = input("Not an ext; select a file extension\n")
        table.pop(sel)
    return
        

if __name__ == "__main__":
    os.chdir("C:\\Users\karee\Downloads") # go to cd
    main()