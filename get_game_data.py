import os
import json
import shutil # use copy & overwrite operations
from subprocess import PIPE, run # runs any terminal command 
import sys # access to command line arguments

# we want to grab from command line arguments  what the source directory
# and the target directory is relative to the current path so we know
# where we should be storing all found games / where to look for the games

DIRECTORY_PATTERN = "game" # what we are looking for in the directory 

# find all game directories from the source directory
# walk through source directory and match directories containing the pattern
def find_all_game_paths(source):
    game_paths = []

    # only want top level directory, so run it once = put break at the end
    for root, dirs, files in os.walk(source): # walk the source path
        for directory in dirs: # get name of directories & check if contains pattern
            if DIRECTORY_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break

    return game_paths

# stores names of game directories from paths without the to_strip string in them
def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


# create the target directory to place files into
def create_dir(path): # takes in the path to the directory we want
    if not os.path.exists(path):
        os.mkdir(path)


# copy the source into the destination 
# if the directory already exists, overwrite it
def copy_and_overwrite(source, dest):
    # recursive delte and copy functions
    if os.path.exists(dest): 
        shutil.rmtree(dest) 
    shutil.copytree(source, dest)


# create a json file for the new target directory
# path: where do you want the file to be?
# game_dirs: directories we want to write meta data for
def make_json_metadata_file(path, game_dirs):
    data = { # data we want to write into the json file
        "gameNames" : game_dirs,
        "numberOfGames" : len(game_dirs)
    }

    # using a context manager to open file. with keyword closes file for us
    with open(path, "w") as f: # w: write mode, overwrites file if alr exists
        json.dump(data, f) # dump data into file


# source is where we are looking and target is where we want to put directory
def main(source, target):
    # we need to create a complete path from location of where we are
    # running our python file to desired directory

    cwd = os.getcwd() # current working directory, where we're running this file
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path) # found all game paths we are interested in
    new_game_dirs = get_name_from_paths(game_paths, "_game") # set new directory names

    create_dir(target_path) # create directory to copy all game directories into

    # tuples the lists together with the zip function:
    # ex - [1, 2, 3] & [a, b, c] -> (1, a), (2, b), (3, c)
    for src, dest in zip(game_paths, new_game_dirs): # performing the copy operation
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
    
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)



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
    
