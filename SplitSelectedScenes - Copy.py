# set path=%path%;C:\app\FFMPEG;C:\Users\HP\MiniConda3\envs\globalOne\Scripts;
# scenedetect -i "bex_alexis_fawx_tr060416_480p_1000.mp4" detect-content list-scenes  save-images
# REM ffmpeg -i "bex_alexis_fawx_tr060416_480p_1000.mp4" -ss 00:19.1 -to 00:20.7 -strict experimental "scene1.mp4"


from pathlib import Path
import sys
import pandas as pd
from random import shuffle
import random
import numpy as np
import os
import re

SelectedFramesDir = Path('SelectedScene')
VideoPath = next(Path.cwd().glob('*.m[pk][v4]'))

def cutVideo(Ivideo,Outvideo,startTime,EndTime):
    # cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe -hwaccel cuda -hwaccel_output_format cuda  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    cmdTemplate = cmdTemplate.replace('Ivideo', Ivideo)
    cmdTemplate = cmdTemplate.replace('00:00.0', startTime)
    cmdTemplate = cmdTemplate.replace('99:99.9', EndTime)
    cmdTemplate = cmdTemplate.replace('output.mp4', Outvideo)
    print(cmdTemplate)
    os.system(cmdTemplate)

def extractScene(Ivideo):
    # os.system(r'set path=%path%;C:\app\FFMPEG;C:\Users\HP\MiniConda3\envs\globalOne\Scripts;')
    cmdTemplate = 'C:\\Users\\HP\\MiniConda3\\envs\\globalOne\\Scripts\\scenedetect -m 5s --drop-short-scenes -i "Ivideo" detect-content list-scenes  save-images'
    cmdTemplate = cmdTemplate.replace('Ivideo', str(Ivideo))
    print(cmdTemplate)
    os.system(cmdTemplate)

    
    
def main():
    if not SelectedFramesDir.is_dir():
        SelectedFramesDir.mkdir()
    # import pdb;pdb.set_trace()
    csvFilePath = VideoPath.stem + '-Scenes.csv'
    if not Path(csvFilePath).is_file():
        extractScene(VideoPath)
        if input('open the dir[y]:')=='y':
            os.system('start "" "%s"' % str(Path.cwd()))
    df = pd.read_csv(csvFilePath)
    for sceneImageFiles in SelectedFramesDir.glob('*.jp*g'):
        sceneId = re.search('Scene-(\d+)',sceneImageFiles.name).group(1)
        if not Path('extractedVideo').is_dir():
            Path('extractedVideo').mkdir()
        # Outvideo = 'extractedVideo\\' + VideoPath.name.replace('.',sceneId + '.')
        Outvideo = 'extractedVideo\\' + re.sub('\.([^\.]*)$',sceneId + '.\\1',VideoPath.name)
        if Path(Outvideo).is_file():
            sceneImageFiles.unlink()
            continue
        sceneId = int(sceneId)
        # import pdb;pdb.set_trace()
        startTime = df.iloc[sceneId,2]
        EndTime = df.iloc[sceneId,5]
        # Ivideo = sceneImageFiles
        cutVideo(str(VideoPath),Outvideo,startTime,EndTime)
        sceneImageFiles.unlink()
        # sceneImageFiles
main()
    