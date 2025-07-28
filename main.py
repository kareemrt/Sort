# main.py - Handles main logic for SORT: a file sorting utility.
# Kareemrt | 7/11/25

import sys
from Folder import Folder
from BinManager import BinManager
from pathlib import Path

default_path = Path.home() / "Downloads" # default: downloads folder
Manager = BinManager() # create 'container' storing folders + file extensions
Dir = Folder(default_path, Manager)

def main():
    '''Main function to run the SORT utility.'''
    print(f"""\nCurrent Path: {Dir._path}\n""")
    prompt = input("""
                   1. Sort CD
                   2. Print CD
                   3. Change CD
                   4. Reverse Sort
                   5. Add binding
                   6. Edit binding
                   7. Remove binding
                   8. Exit\n""")
    match prompt:
        case "1": Dir.sort()
        case "2": Dir.get_contents(log = True)
        case "3": Dir.edit_path()
        case "4": Dir.reverse_sort()

        case "5": # Add ext:folder binding
            ext = input("What is the file extension? (e.g. txt, jpg, etc.)\n")
            bins = list(set(Manager.get_bins()))
            dir = input(f"Where would you like to store these files? {bins}: ")
            while dir not in bins: 
                dir = input(f"That is not a valid folder, please select from the list\n{bins}\n")
            Manager.add_bind(ext, dir)
            
        case "6": # Edit binding
            ext = input("What is the file extension? (e.g. txt, jpg, etc.)\n")
            new_dir = input(f"Where would you like to store these files? {bins}: ")
            Manager.edit_bind(ext, new_dir)

        case "7": # Remove binding
            print(f"Current file extensions: {Manager.get_extensions()}")
            ext = input("Select an extension from above\n")
            while ext not in Manager._config.keys(): 
                ext = input(f"Not a valid extension; select a file extension\n{Manager._config.keys()}\n")
            Manager.remove_bind(ext)

        case _: 
            print("Exiting...")
            return False
    return True

if __name__ == "__main__":
    #print(sys.version) 
    print("""
            Welcome to SORT!\n
            This utility sorts files into folders based on file extensions.\n
            You can edit the file extension bindings in the config file or via the command line.\n
            You can also reverse the sort operation.\n
            Press Ctrl+C to exit at any time.""")
    valid = True
    while valid:
        try: valid = main()
        except KeyboardInterrupt:
            print("\nExiting SORT...")
            valid = False
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            valid = False
