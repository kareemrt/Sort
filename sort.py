# BinSorter
# Kareem Taha
# 2/12/2021
#
# Builds containers depending on user settings and moves files to appropriate containers.
import os
import shutil
import configparser
import geopy
from geopy import Nominatim
from picture import Picture, Image
path = os.path.expanduser('~') + '\Downloads'
extensions = {"folder":"folders",
            "exe":"executables",
            "bat":"scripts",
            "py":"scripts",
            "zip":"archives",
            "rar":"archives",
            "7z":"archives",
            "tar":"archives",
            "tgz":"archives",
            "iso":"disk-images",
            "pdf":"documents",
            "docx":"documents",
            "png":"images",
            "jpeg":"images"
            }

buckets = ["unknown","folders","executables","scripts","archives","disk-images", "documents", "images"]

def makeDir(bucket): os.mkdir(bucket)
def join(cd, target): return os.path.join(cd, target)
def isFile(cd): return os.path.isfile(cd)
def isDir(cd): return os.path.isdir(cd)
def removeDir(cd): os.removedirs(cd)
def printPath(): print("CD: " + path)
def setPath(target): 
    global path
    path = target
def doNothing(): return
def returnChildren():
    printPath()
    contents = os.listdir(path)
    children = [item for item in contents if isDir(join(path, item))]
    print(children)
    return children

def sort_dir():
    dir_contents = os.listdir()
    print("Sorting...")    
    for bucket in buckets:
        if bucket not in dir_contents: makeDir(bucket)
    for item in dir_contents:
        temp = join(path, item) # temporary path to current file
        if isFile(temp): 
            try: file_ext = item.rsplit(".",1)[1] # if item is file, parse its file extension
            except IndexError: # if file has no extension, give it a blank
                file_ext = "" 
        else: # item is directory
            if item in buckets: continue # if directory is a bucket, skip
            ext = "folder" # otherwise mark it as a folder

        target = join(path, extensions.get(file_ext, "unknown")) # create new path to bucket using current file extension

        try: shutil.move(temp, target) # move
        except shutil.Error: print("File already exists in target directory") # return error if exists
    main()

def reverse():
    dir_contents = os.listdir(path)
    print("Reversing...")
    for bucket in dir_contents:
        if bucket in buckets:
            temp = join(path, bucket)
            bucket_contents = os.listdir(temp)
            for item in bucket_contents:
                item_path = join(temp, item)
                shutil.move(item_path, path)
            removeDir(temp)
    main()

def main():
    os.chdir(path) # change dir to path
    printPath()
    choice = 0
    options = { "1": sort_dir, "2": print_dir, 
                "3": change_dir, "4": edit_buckets,
                "5": edit_ext, "6": reverse,
                "7": metadata, "8": doNothing}
    while(choice not in options):
        choice = input("1. Sort CD\n2. Print CD\n3. Change CD\n4. Edit sorted buckets\n5. Edit target filetypes\n6. Reverse Sort\n7. Metadata\n8. Exit\n")
    options[choice]()

def change_dir():
    global path
    printPath()
    choice = 0
    options = {"1": "By Path", "2": "Child Dir", "3": "Parent Dir", "4": "Exit"}
    while (choice not in options):
        choice = input("1: By Path\n2: Child Dir\n3: Parent Dir\n4: Exit\n")
    choice = options[choice]

    if choice == "By Path": # type path
        temp = input("Enter Path: (.. to escape)")
        if isDir(temp): setPath(temp)
    elif choice == "Child Dir": # child dir
        children = returnChildren() # list of child directories
        
        temp = input("Enter a child dir (.. to escape)")
        if temp in children: setPath(join(path, temp))
    elif choice == "Parent Dir": path = os.path.dirname(path)
    main()

def print_dir(dir_only = False, file_only = False): # print entire dir. can specificy to only print one type, or to return list of child dirs.
    contents = os.listdir(path)
    printPath()
    for item in contents:
        temp = join(path, item)
        if file_only: 
            if isFile(temp): print("File: " + item)
        elif dir_only:
            if isDir(path): print("Dir: " + item)
        else: print(item)
    print("")
    main()

def edit(buckets=False, filetypes=False, config=False):
    if buckets: edit_buckets()
    elif filetypes: edit_ext()
    main()
    
def edit_buckets():
    choice = 0
    while(choice != 1 and choice != 2 and choice != 3 and choice != 4):
        choice = input("1. Add Bucket\n2. Edit Bucket\n3. Remove Bucket\n4. Exit\n")
        choice = int (choice)

    if choice == 1: buckets.append(input("Bucket Name: "))
    elif choice == 2 or choice == 3: 
        bucket = input("Select a bucket: ")
        while bucket not in buckets:
            bucket = input("Not a bucket; select a bucket")
        if choice == 2:
            temp = input("Rename to: ")
            buckets[buckets.index(bucket)] = temp
        elif choice == 3: buckets.remove(bucket)
    return

def edit_ext():
    choice = 0
    while(choice not in [1, 2, 3, 4]):
        choice = input("1. Add Ext\n2. Edit Ext\n3. Remove Ext\n4. Exit\n")
        choice = int (choice)

    if choice == 1:
        ext = input("Add extension: ")
        print(buckets)
        file_type = input("Pick an associated bucket (filetype): ")
        while file_type not in buckets:
            file_type = input("Incorrect; pick an associated filetype: ")
        buckets[ext] = file_type
    if choice == 2:
        for ext, buc in extensions.items():
            print(ext+":"+buc)
        ext = input("Select an extension\n")
        while ext not in table.keys():
            ext = input("Not an ext; select a file extension\n")
        if choice == 2:
            temp = input("Rename to:\n")
            bucket = table.pop(ext)
            extensions[temp] = bucket
        elif choice == 3: table.pop(ext)
    return
        
def metadata():
    dir_contents = os.listdir(path)
    images = []
    for image in dir_contents:
        temp_path = join(path, image)
        with open(temp_path, 'rb') as image_file:
            my_image = Image(image_file)
            images.append(my_image)
    print(images[0].datetime)
    for i in range(len(images)):
        images[i] = Picture(images[i])
        images[i].set_traits()
    sort_md(images)
    
def sort_md(images_list):
    md_buckets = []
    loc = Nominatim(user_agent="Sorter")
    
        



if __name__ == "__main__":
    main()