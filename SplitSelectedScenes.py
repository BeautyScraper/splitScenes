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
import cv2
import shutil 


VideoPath = Path.cwd().glob('*.m[pk][v4]')
supportedVideoExtension = ['mp4','mkv']

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
        
        
def getDuration(filename):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(filename)
    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    return duration, fps, (width, height)    

def cutVideo(Ivideo,Outvideo,startTime,EndTime):
    # cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    # cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe -y -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    # video = cv2.VideoCapture(Ivideo)
    # duration = video.get(cv2.CAP_PROP_POS_MSEC)
    # import pdb;pdb.set_trace()
    print(timeStringToValue(startTime))
    if timeStringToValue(startTime) <= 30000:
        try:
            if (timeStringToValue(EndTime)/1000 - getDuration(Ivideo)[0]) < 1:
                # import pdb;pdb.set_trace()
                shutil.copy(Ivideo,Outvideo)
                return
        except:
            pass
    # print(getDuration(Ivideo))
    print(Ivideo)
    application = Path('C:\\app\\FFMPEG\\ffmpeg.exe')
    if not application.is_file():
        import pdb;pdb.set_trace()
    # cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe -y -hwaccel cuda -hwaccel_output_format cuda  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
    cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i "Ivideo" -ss 00:00.0 -to 99:99.9 -c:a copy -c:v h264_nvenc -b:v 5M "output.mp4"'
    cmdTemplate = cmdTemplate.replace('Ivideo', Ivideo)
    cmdTemplate = cmdTemplate.replace('00:00.0', startTime)
    cmdTemplate = cmdTemplate.replace('99:99.9', EndTime)
    cmdTemplate = cmdTemplate.replace('output.mp4', Outvideo)
    
    print(cmdTemplate)
    # import pdb;pdb.set_trace()
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
        # import pdb;pdb.set_trace()
        cmdTemplate = 'C:\\app\\FFMPEG\\ffmpeg.exe -n -hwaccel nvdec -hwaccel_output_format cuda  -i "Ivideo" -ss 00:00.0 -to 99:99.9 -strict experimental "output.mp4"'
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
        

    def is_same_as(self,cutVideo):
        conditions = [
        self.sceneVideo == cutVideo.sceneVideo,
        self.startTime == cutVideo.startTime,
        self.EndTime == cutVideo.EndTime
        ]
        return False not in conditions
        
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

    application = Path('C:\\Users\\HP\\MiniConda3\\envs\\globalOne\\Scripts\\scenedetect.exe')
    if not application.is_file():
        cmdTemplate = 'conda activate scene_cut && scenedetect -m 1s --drop-short-scenes -i "Ivideo" detect-content list-scenes  save-images'
    else:
        cmdTemplate = 'conda activate scene_cut && C:\\Users\\HP\\MiniConda3\\envs\\globalOne\\Scripts\\scenedetect -m 1s --drop-short-scenes -i "Ivideo" detect-content list-scenes  save-images'
    cmdTemplate = cmdTemplate.replace('Ivideo', str(Ivideo))
    print(cmdTemplate)
    # import pdb;pdb.set_trace()
    os.system(cmdTemplate)

def GenrateCSVJPG(vp):
    csvFilePath = vp.stem + '-Scenes.csv'
    if not Path(csvFilePath).is_file():
        extractScene(vp)    
        

def doIt(extractVideoDir = 'extractedVideo', SelectedFramesDirN = 'SelectedScene', target_dir = ''):
    # SelectedFramesDir = Path.cwd() / Path(SelectedFramesDirN)
    
    if target_dir == '':
        target_dir = Path.cwd()
    else:
        target_dir = Path(target_dir)
    if not Path(SelectedFramesDirN).is_absolute():
        SelectedFramesDir = target_dir / Path(SelectedFramesDirN)
    if not SelectedFramesDir.is_dir():
        SelectedFramesDir.mkdir()
    for vp in VideoPath:
        GenrateCSVJPG(vp)
    # if input('open the dir[y]:')=='y':
        # os.system('start "" "%s"' % str(Path.cwd()))
    cutObjects = []
    # import pdb; pdb.set_trace()
    for sceneImageFiles in SelectedFramesDir.glob('*.jp*g'):
        sceneVideo = None
        for sve in supportedVideoExtension:
            vfn = re.sub('-Scene-[^\.]+','',sceneImageFiles.stem)
            # import pdb;pdb.set_trace()
            if Path(vfn+'.'+sve).is_file():
                sceneVideo = vfn+'.'+sve
                break
        if sceneVideo == None:
            print('video not found')
            continue
        csvFilePath = Path(sceneVideo).stem + '-Scenes.csv'
        assert Path(csvFilePath).is_file() 
        print(csvFilePath)
        try:
            df = pd.read_csv(csvFilePath,skiprows=1)
        except:
            print('something is wrong with the csv reading YYYYYYYYYYYYYY',csvFilePath)
            import pdb;pdb.set_trace()
            continue
        # df.set_index()
        sceneId = re.search('Scene-(\d+)',sceneImageFiles.name).group(1)

        if not Path(extractVideoDir).is_dir():
            Path(extractVideoDir).mkdir()
        # Outvideo = 'extractedVideo\\' + VideoPath.name.replace('.',sceneId + '.')
        Outvideo = '%s\\' % extractVideoDir + re.sub('\.([^\.]*)$',sceneId + '.\\1',sceneVideo)

        # if Path(Outvideo).is_file():
            # sceneImageFiles.unlink()
            # continue
        sceneId = int(sceneId)
        # import pdb;pdb.set_trace()
        if df.shape[0] == 1:
            sceneId = 0
        try:
            startTime = df.iloc[sceneId-1,2]  
            EndTime = df.iloc[sceneId-1,5]
        except:
            # import pdb;pdb.set_trace()
            print('unable to get timings')
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
    return cutObjects
if __name__ == '__main__':
    cutObjects = doIt()
    secondaryCutObjects = doIt('extractedVideo2', 'PVD2')
        
    for cvideo in cutObjects:
        cvideo.cutVideo()
        sameVideo = [x for x in secondaryCutObjects if x.is_same_as(cvideo)]
        if len(sameVideo) > 0:
            outPath = Path.cwd() / 'extractedVideo2'
            shutil.copy(".\\"+cvideo.Outvideo, outPath)
            # import pdb;pdb.set_trace()
            # secondaryCutObjects.remove(cvideo)
            secondaryCutObjects.remove(sameVideo[0])
            sameVideo[0].mifp_dellAll()
    for cvideo in secondaryCutObjects:
        cvideo.cutVideo()
    
    
    
    