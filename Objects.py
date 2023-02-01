import IO   # Objects.py - implimentation for 'Path' and 'Container' objects
import os
import shutil
def isDir(cd): return os.path.isdir(cd)
def isFile(cd): return os.path.isfile(cd)
def combinePath(cd, target): return os.path.join(cd, target)
def makeDir(path): os.mkdir(path)
def removeDir(cd): os.removedirs(cd)
helper_methods = [isDir, isFile, combinePath, makeDir, removeDir]
IO_extensions, IO_folders = IO.IO_get_types()
class Path:
    def __init__(self, path = "", container = None) -> None:
        self.path = path
        self.container = container
    def sort(self) -> None:
        '''Sorts the path contents into folders based on filetypes'''
        print("Sorting...")
        dir = os.listdir(path=self.path)

        for f in self.container.folders:
            if f not in dir: makeDir(combinePath(self.path,f))
        for item in dir:
            old_path = combinePath(self.path, item) # temporary path to current file
            print(old_path)

            if isFile(old_path): # item == file
                try: ext = item.rsplit(".",1)[1] # parse file extension
                except IndexError: ext = ""; print("IndexError! File has no extension")
            elif item not in self.container.folders: ext = "folder" # item == dir

            folder = self.container.extensions.get(ext, "unknown")
            new_path = combinePath(self.path, folder) # create new path to bucket using current file extension

            try: shutil.move(old_path, new_path)
            except shutil.Error: print("File already exists in target directory")
    def reverse(self) -> None:
        '''Reverses a filetype path sort'''
        print("Reversing Sort...")
        dir = os.listdir(self.path)
        for f in dir:
            if f in self.container.folders:
                f_path = combinePath(self.path, f)
                f_contents = os.listdir(f_path)
                for item in f_contents: shutil.move(combinePath(f_path, item), self.path) # move items outside folders
                removeDir(f_path)
    def print(self) -> None: print("CD: " + self.path)
    def print_dir(self, dir = True, file = True) -> None:
        '''Prints the path's contents
            * dir - print dirs
            * file - print files'''
        self.print()
        contents = os.listdir(self.path)
        for item in contents:
            temp = combinePath(self.path, item)
            if file and isFile(temp): print("File: " + item)
            if dir and isDir(temp): print("Dir: " + item)
        print("")
    def children(self) -> list:
        '''Prints/Returns list of child directories in current path'''
        contents = os.listdir(self.path)
        children = [item for item in contents if isDir(combinePath(self.path, item))]
        print(children)
        return children
    def change(self) -> None:
        '''Change the current Path object's path variable (what directory it points to)''' 
        match input("1: By Path\n2: Child Dir\n3: Parent Dir\n4: Exit\n"):
            case "1": 
                p = input("Enter Path: (.. to escape)")
                if isDir(p): self.path = p
            case "2":
                children = self.children() # list of child directories
                dir = input("Enter a child dir (.. to escape)")
                if dir in children: self.path = combinePath(self.path, dir)
            case "3": self.path = os.path.dirname(self.path)
            case _: print("No valid options were selected\nExiting change_dir() method...")
    def main(self) -> None:
        '''Function to let user interact with Path methods'''
        match input("1. Sort CD\n2. Print CD\n3. Change CD\n4. Reverse Sort\n6. Edit folders\n6. Edit extensions\n7. Exit\n"):
            case "1": self.sort()
            case "2": self.print_dir()
            case "3": self.change()
            case "4": self.reverse()
            case "5": self.container.edit_extensions()
            case "6": self.container.edit_folders()
            case _: print("Exiting... (no valid option given)"); return
        self.main()
class Container:
    def __init__(self, folders = [], extensions = {}) -> None:
        self.folders = folders
        self.extensions = extensions
        self.containers = {folder:[] for folder in folders}
    def add_extension(self, ext, f, file_save=False):
        if f not in self.folders:                                  # Create folder
            self.folders.append(f)
            self.containers[f] = []
        if ext not in self.containers[f]: self.containers[f] = ext # Create folder:ext association
        if ext not in self.extensions: self.extensions[ext] = f    # Create ext entry in dict{extensions}
        if file_save: IO.IO_add_type(ext, f) # save to file
    def set_extensions(self):
        for ext, fld in IO_extensions.items(): self.add_extension(ext,fld)
    def edit_folders(self):
        match input("1. Add Folder\n2. Remove Folder\n3. Exit\n"):
            case "1": 
                f = input("Folder name: ")
                self.folders.append(f)
                self.containers[f] = []
            case "2": 
                f = input("Select a folder: ")
                while f not in self.folders: f = input("Not a folder; type a folder")
                self.folders.remove(f)
            case _: print("Exiting... (no option given)")
    def edit_extensions(self):
        match input("1. Add Extension\n2. Remove Ext\n3. Exit\n"):
            case "1":
                ext = input("Type extension: ")
                print(self.folders)
                f = input(f"Pick an associated folder from above for extension {ext}: ")
                while f not in self.folders: f = input("Incorrect; pick an associated filetype: ")
                self.containers[f] = ext
                self.extensions[ext] = f
            case "2":
                print(f"Current file extensions = {self.extensions}")
                ext = input("Select an extension from above\n")
                while ext not in self.extensions.keys(): ext = input("Not an ext; select a file extension\n")
                self.extensions.pop(ext)
            case _: print("Exiting... (no option given")
        


