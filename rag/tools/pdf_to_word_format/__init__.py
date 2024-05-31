
import sys
import os

def add_not_found_module():
    "/".join(os.getcwd().split("/")[:-2])
    sys.path.append("/".join(os.getcwd().split("/")[:-2]))
