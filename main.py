from Objects import *   # sort.py - Builds containers depending on user settings and moves files to appropriate containers.
def main():
    path = os.path.normcase(os.path.expanduser('~') + '/Downloads') # default path == user downloads folder (os independent)
    Cont = Container()                                              # create 'container' storing folders + file extensions
    Cont.set_extensions()                                           # (IO) read folders/exts from FILE 
    P = Path(path, container=Cont)                                  # create path object
    P.print()                                                       
    P.main()
if __name__ == "__main__": main()
