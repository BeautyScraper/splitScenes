from ast import arg
import os
import argparse
import re
import random
import sys
import time
import math
import logging
import shutil 
from pathlib import Path
from SplitSelectedScenes import doIt as cutVideo
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')

#check if sting is a valid path

#argument to parse the input and output directories
parser.add_argument('--main_dir', type=str, default=r'D:\paradise\stuff\new\pvd\test', help='input directory')
parser.add_argument('--search_dir_path', type=str, default=r'D:\paradise\stuff\new\pvd', help='output directory')
parser.add_argument('--target_dir_path', type=str, default=r'D:\paradise\stuff\new\pvd', help='output directory')
parser.add_argument('--fs_fileSource', type=str, default=r'D:\paradise\stuff\simswappg\srcs', help='output directory')
args = parser.parse_args()

main_dir = args.main_dir
search_dir_path = args.search_dir_path
target_dir_path = args.target_dir_path
fs_fileSource = args.fs_fileSource

def get_corresponding_file(imgfiles,search_dir):
    #Yummyx (17) @hudengi pvd2 W1t81N callmesherni(6827262467731617414341)-Scene-001-02
    file_path = Path(imgfiles)
    needle_fileName = file_path.name.split(' W1t81N ')[-1]
    if (Path(search_dir) / needle_fileName).is_file():
        return str(Path(search_dir) / needle_fileName)
    else:
        return None
def move_corresponding_file(src_dir,search_dir,target_path):
    for imgfiles in Path(src_dir).glob('*.jpg'):
        cr_file = get_corresponding_file(str(imgfiles),search_dir)
        if cr_file is None:
            continue
        target_path1 = Path(target_path) / (imgfiles.name.split(' @hudengi ')[0])
        target_path1.mkdir(exist_ok=True)
        shutil.copy(cr_file,target_path1)
        imgfiles.unlink()

if __name__ == '__main__':
    mdp = Path(main_dir)
    selectedPath = mdp / 'SelectedScene'
    move_corresponding_file(selectedPath,search_dir_path,target_dir_path)
    cutObjectsList = []
    for src_files in Path(fs_fileSource).glob('*.jpg'):
        if (Path(search_dir_path) / src_files.stem).is_dir():
            cutObjectsList.append(cutVideo(src_files.stem+'_video',src_files.stem))
    # import pdb;pdb.set_trace()
    for cutObjectl in cutObjectsList:
        for cutObject in cutObjectl:
            cutObject.cutVideo()
    
    