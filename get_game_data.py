import os
import json
import shutil # use copy & overwrite operations
from subprocess import PIPE, run # runs any terminal command 
import sys # access to command line arguments

# we want to grab from command line arguments  what the source directory
# and the target directory is relative to the current path so we know
# where we should be storing all found games / where to look for the games

# source is where we are looking and target is where we want to put directory
def main(souce, target):
    pass


# grab the command line arguments. only want to execute the main script
# if running this python file directly. 
# will not execute anything in here if you were importing a function / class 
# from this file
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only")
    
    # get the source and target directory
    source, target = args[1:]
    main(source, target)
    
