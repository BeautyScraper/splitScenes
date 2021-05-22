# set path=%path%;C:\app\FFMPEG;C:\Users\HP\MiniConda3\envs\globalOne\Scripts;
# scenedetect -i "bex_alexis_fawx_tr060416_480p_1000.mp4" detect-content list-scenes  save-images
# REM ffmpeg -i "bex_alexis_fawx_tr060416_480p_1000.mp4" -ss 00:19.1 -to 00:20.7 -strict experimental "scene1.mp4"


from pathlib import Path
from MyUtility import fileListCopy
import sys
import pandas as pd
from random import shuffle
import random
import numpy as np
import os
import re

SelectedFramesDir = Path('SelectedScene')
VideoPath = Path.cwd().glob('*.m[pk][v4]')
supportedVideoExtension = ['mp4','mkv']
cutObjects = []
scannedPath = r'D:\paradise\stuff\Scanned'


def is_movable(vpf):
    imageFiles = Path.cwd().rglob('*%s*.jp*g' % vpf.stem)
    for x in imageFiles:
        return False
    return True

def CleanUpDoneVideo(targetPath=''):
    if targetPath == '':
        targetPath = scannedPath
    targetPath = Path(targetPath)
    fl = []
    import pdb;pdb.set_trace()
    for vpf in VideoPath:
        correspondingCSVname = vpf.stem + '-Scenes.csv'
        ccsvp = Path(correspondingCSVname)
        if not ccsvp.is_file():
            continue
        if is_movable(vpf):
            fl.append(str(vpf))
    
    import pdb;pdb.set_trace()
    fileListCopy(fl,str(targetPath))
        
        
    

def cutVideo(Ivideo,Outvideo,startTime,EndTime):
    # cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe -hwaccel cuda -hwaccel_output_format cuda  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    cmdTemplate = cmdTemplate.replace('Ivideo', Ivideo)
    cmdTemplate = cmdTemplate.replace('00:00.0', startTime)
    cmdTemplate = cmdTemplate.replace('99:99.9', EndTime)
    cmdTemplate = cmdTemplate.replace('output.mp4', Outvideo)
    print(cmdTemplate)
    # with open('continueCommand.bat', 'a+') as fp:
        # fp.write(cmdTemplate+'\n')
    os.system(cmdTemplate)
def getItem(lm,index,defaultV=None):
    try:
        return lm[index]
    except:
        return defaultV
        
def timeStringToValue(tstr):
    krs = re.split('[\:\.]', tstr)
    h = getItem(krs,0,'0')
    m = getItem(krs,1,'0')
    s = getItem(krs,2,'0')
    ms = getItem(krs,3,'0')
    # h, m, s, ms = re.split('[\:\.]', tstr)
    return int(ms) + int(s) * 1000 + int(m) * 60 * 1000 + int(h) * 60 * 60 * 1000

class VideoScene():
    def writeBatFile(self):
        cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe -n -hwaccel cuda -hwaccel_output_format cuda  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
        cmdTemplate = cmdTemplate.replace('Ivideo', self.sceneVideo)
        cmdTemplate = cmdTemplate.replace('00:00.0', self.startTime)
        cmdTemplate = cmdTemplate.replace('99:99.9', self.EndTime)
        cmdTemplate = cmdTemplate.replace('output.mp4', self.Outvideo)
        # print(cmdTemplate)
        with open('continueCommand.bat', 'a+') as fp:
            fp.write(cmdTemplate+'\n')

    def __init__(self,sceneVideo,Outvideo,startTime,EndTime,mifp=frozenset()):
        self.sceneVideo = sceneVideo
        self.Outvideo = Outvideo
        self.startTime = startTime
        self.EndTime = EndTime
        self.mifp = mifp
    
    def shouldMerge(self,SecondVS,threshHold = 30):
        if self.sceneVideo != SecondVS.sceneVideo:
            return False
        if self.Outvideo == SecondVS.Outvideo:
            return True
        threshHold = threshHold * 1000
        myst = timeStringToValue(self.startTime)
        yst = timeStringToValue(SecondVS.startTime)
        myet = timeStringToValue(self.EndTime)
        yet = timeStringToValue(SecondVS.EndTime)
        
        if myst == yst or myet == yet:
            return True
        # import pdb;pdb.set_trace()
        if myst < yst:
            return yst in range(myst,myet+threshHold)
        else:
            return myst in range(yst,yet+threshHold)

    def cutVideo(self):
        cutVideo(self.sceneVideo,self.Outvideo,self.startTime,self.EndTime)
        self.mifp_dellAll()
        
        
    def mifp_add(self,image_fp):
        self.mifp.add(image_fp)
    
    def mifp_dellAll(self):
        # import pdb; pdb.set_trace()
        for mifp in self.mifp:
            mifp.unlink()
            
        
    def Merge(self,SecondVS):
        myst = timeStringToValue(self.startTime)
        yst = timeStringToValue(SecondVS.startTime)
        myet = timeStringToValue(self.EndTime)
        yet = timeStringToValue(SecondVS.EndTime)
        
        mstartTime = self.startTime if myst < yst else SecondVS.startTime
        mendTime = self.EndTime if myet > yet else SecondVS.EndTime
        mifp_merged = self.mifp.union(SecondVS.mifp)
        return VideoScene(self.sceneVideo,self.Outvideo,mstartTime,mendTime,mifp_merged)


def extractScene(Ivideo):
    # os.system(r'set path=%path%;C:\app\FFMPEG;C:\Users\HP\MiniConda3\envs\globalOne\Scripts;')
    cmdTemplate = 'C:\\Users\\HP\\MiniConda3\\envs\\globalOne\\Scripts\\scenedetect -m 5s --drop-short-scenes -i "Ivideo" detect-content list-scenes  save-images'
    cmdTemplate = cmdTemplate.replace('Ivideo', str(Ivideo))
    print(cmdTemplate)
    os.system(cmdTemplate)

def GenrateCSVJPG(vp):
    csvFilePath = vp.stem + '-Scenes.csv'
    if not Path(csvFilePath).is_file():
        extractScene(vp)    
        
def main():
    if not SelectedFramesDir.is_dir():
        SelectedFramesDir.mkdir()
    for vp in VideoPath:
        GenrateCSVJPG(vp)
    # if input('open the dir[y]:')=='y':
        # os.system('start "" "%s"' % str(Path.cwd()))

    for sceneImageFiles in SelectedFramesDir.glob('*.jp*g'):
        for sve in supportedVideoExtension:
            vfn = re.sub('-Scene-[^\.]+','',sceneImageFiles.stem)
            # import pdb;pdb.set_trace()
            if Path(vfn+'.'+sve).is_file():
                sceneVideo = vfn+'.'+sve
                break
        assert sceneVideo != None
        csvFilePath = Path(sceneVideo).stem + '-Scenes.csv'
        assert Path(csvFilePath).is_file() 
        print(csvFilePath)
        try:
            df = pd.read_csv(csvFilePath)
        except:
            print('something is wrong with the csv reading YYYYYYYYYYYYYY',csvFilePath)
            continue
        sceneId = re.search('Scene-(\d+)',sceneImageFiles.name).group(1)
        if not Path('extractedVideo').is_dir():
            Path('extractedVideo').mkdir()
        # Outvideo = 'extractedVideo\\' + VideoPath.name.replace('.',sceneId + '.')
        Outvideo = 'extractedVideo\\' + re.sub('\.([^\.]*)$',sceneId + '.\\1',sceneVideo)
        # if Path(Outvideo).is_file():
            # sceneImageFiles.unlink()
            # continue
        sceneId = int(sceneId)
        # import pdb;pdb.set_trace()
        if df.shape[0] == 1:
            sceneId = 0
        try:
            startTime = df.iloc[sceneId,2]  
            EndTime = df.iloc[sceneId,5]
        except:
            continue
        # Ivideo = sceneImageFiles
        newVideoSec = VideoScene(sceneVideo,Outvideo,startTime,EndTime,frozenset({sceneImageFiles}))
        for cvideo in cutObjects:
            if cvideo.shouldMerge(newVideoSec):
               newVideoSec = cvideo.Merge(newVideoSec)
               cutObjects.remove(cvideo)
               # import pdb;pdb.set_trace() 
               #remove the cvideo
        cutObjects.append(newVideoSec)
        # sceneImageFiles.unlink()
        # sceneImageFiles
if __name__ == '__main__':
    main()
    for cvideo in cutObjects:
        cvideo.writeBatFile()
        
    for cvideo in cutObjects:
        cvideo.cutVideo()
    
    