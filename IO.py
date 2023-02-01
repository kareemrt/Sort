import re   # IO.py - implimentation for File IO (for R/W folders/extensions)
def IO_get_types():
    pattern = "(.*):(.*)"
    extensions = {}
    folders = []
    with open('extensions.txt', "r") as ext_file:
        for line in ext_file.readlines():
            line = line.strip()
            extension, folder = re.findall(pattern, line)[0]
            folders.append(folder)
            extensions[extension] = folder
    folders.append('unknown')
    return extensions, folder
def IO_add_type(ext, folder): 
    with open('extensions.txt', "r") as ext_file: ext_file.write(f"{ext}:{folder}")