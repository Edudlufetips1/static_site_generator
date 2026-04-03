from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive, generate_page
import os
import shutil
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    if os.path.exists("./docs"):
       shutil.rmtree("./docs")
    
    copy_files_recursive("./static", "./docs")    
    generate_pages_recursive("./content", "./template.html", "./docs",  basepath)


main()
