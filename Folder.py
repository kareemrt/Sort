# Folder.py - Folder object for sorting files into folders based on file extensions.
# Kareem | 7/11/25 
import shutil
from pathlib import Path

class Folder:
    '''Folder object applies sorting logic to a specified path.'''

    def __init__(self, path, manager) -> None:
        self._path = Path(path)
        self.manager = manager

    def sort(self) -> None:
        '''Sorts the folder contents into new folders based on filetypes'''

        for d in self.manager.get_bins(): # Create bin folders
            (self._path / d).mkdir(parents=True, exist_ok=True)

        for item in self._path.iterdir(): # Sort files into folders
            if item.is_file(): file_ext = item.suffix[1:] if item.suffix else ""
            elif item.name not in self.manager.get_bins(): file_ext = "folder"
            else: 
                continue

            print(item)
            target_bin = self.manager.get_config().get(file_ext, "unknown") 
            dest = self._path / target_bin / item.name # New item path

            try: shutil.move(str(item.resolve()).strip(), str(dest))
            except shutil.Error: 
                print("File already exists in target directory - Making copy...")
                shutil.move(str(item.resolve()), str(dest.with_stem(dest.stem + "_SCOPY")))
            except Exception as e:
                print(f"Error moving file {item.resolve()} to {dest}: {e}")
                continue

    def reverse_sort(self) -> None:
        '''Reverses the folder sort'''

        print("Reversing Sort...")
        for item in self._path.iterdir(): # Traverse current folder contents
            if item.name in self.manager.get_bins() and item.is_dir():
                for obj in item.iterdir():
                    dest = self._path / obj.name
                    try: shutil.move(str(obj.resolve()), str(dest))
                    except Exception as e:
                        print(f"Error moving file {obj.resolve()} to {dest}: {e}")
                        #shutil.move(str(obj.resolve()), str(dest.with_stem(dest.stem + "_SCOPY")))
                item.rmdir()

    def get_contents(self, include_dirs = True, include_files = True, log = False) -> list:
        '''Returns folder contents
            * include_dirs - include directories in output
            * include_files - include files in output
            * log - print contents to console
        '''

        output = []
        for item in self._path.iterdir():
            if (include_dirs and item.is_dir()) or (include_files and item.is_file()):
                output.append(item.name)
                if log: print(f"{'Dir' if item.is_dir() else 'File'}: {item.name}")
        return output

    def edit_path(self) -> None:
        '''Edit folder location path''' 

        prompt = input("""
                       1: By Path
                       2: Child Dir
                       3: Parent Dir
                       4: Exit\n""")
        match prompt:

            case "1": 
                p = Path(input("Enter Path: (.. to escape)\n"))
                if p.is_dir():
                    print(f"Changed path to {p}")
                    self._path = p
                else: print("Path does not exist or ")

            case "2":
                child_dirs = self.get_contents(include_files = False, log = True) # list of child directories
                target_dir = input("Enter a child dir (.. to escape)")
                if target_dir in child_dirs: 
                    self._path = self._path / target_dir

            case "3": self._path = self._path.parent
            case _: print("No valid options were selected, exiting method...")

