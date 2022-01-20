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
# sys.path.append(r'D:\Developed\Automation\ExtractKeyFrames')

main_dir = r'D:\paradise\stuff\new\pvd2\test'
search_dir_path = r'D:\paradise\stuff\new\pvd2'
target_dir_path = r'D:\paradise\stuff\new\pvd2'
fs_fileSource = r'D:\paradise\stuff\simswappg\srcs'

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
        # import pdb;pdb.set_trace()
        if (Path(search_dir_path) / src_files.stem).is_dir():
            cutObjectsList.append(cutVideo(src_files.stem+'_video',src_files.stem))
    for cutObjectl in cutObjectsList:
        for cutObject in cutObjectl:
            cutObject.cutVideo()
    
    