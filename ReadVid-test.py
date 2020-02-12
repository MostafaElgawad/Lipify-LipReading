import os
import cv2
import csv
import glob
from moviepy.video.io.VideoFileClip import VideoFileClip
from dataclasses import dataclass
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



@dataclass()
class WordInstance:
    '''Class for keeping track of each word'''
    name: str
    start_time: float
    end_time: float
    
###################################### Static Data ########################################
FPS = 25
commands = ['bin', 'lay', 'place', 'set']
prepositions = ['at', 'by', 'in', 'with']
colors = ['blue', 'green', 'red', 'white']
adverbs = ['again', 'now', 'please', 'soon']
alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)] 
numbers = ['one','two','three','four','five','six','seven','eight','nine']
########################################################################################### 

def getAlignFileName(Path):
    '''Helper function to get name of the align file for a certain video'''
    tempPath = Path.split("/")
    newPath = tempPath[0] + '/align/' + (tempPath[2].split('\\')[1]).split('.')[0] + '.align' 
    return newPath  
    
    
def extractWordTimingFromVideo(filename):
    '''Function that extracts each align file into a list of dataclasses'''
    lines = open(filename).read().splitlines()
    wordsWithTimings = []
    for line in lines:
        temp = line.split()
        wordsWithTimings.append(WordInstance(temp[2], temp[0], temp[1]))
    return wordsWithTimings


def cutVideo(videoPath,fileName,start_time,end_time):
    with VideoFileClip(videoPath) as video:
                new = video.subclip(start_time, end_time)
                new.write_videofile(fileName)


def segmentSingleVideo(videoPath, alignFilePath):
    '''Function responsible for segmenting a single video into its underlying words in their prespective folders'''    
    wordTimings = extractWordTimingFromVideo(alignFilePath)
    for word in wordTimings:
        #print("Current Word is: {}".format(word.name))
        start_time = round((float(word.start_time)/(FPS*1000)),3)
        end_time = round((float(word.end_time)/(FPS*1000)),3)
        
        if word.name in commands:
            new_index = len(os.listdir('Videos-After-Extraction/Commands/'))
            fileName = 'Videos-After-Extraction/Commands/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
        
        if word.name in prepositions:
            new_index = len(os.listdir('Videos-After-Extraction/Prepositions/'))
            fileName = 'Videos-After-Extraction/Prepositions/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
        
        if word.name in colors:
            new_index = len(os.listdir('Videos-After-Extraction/Colors/'))
            fileName = 'Videos-After-Extraction/Colors/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
        
        if word.name in numbers:
            new_index = len(os.listdir('Videos-After-Extraction/Numbers/'))
            fileName = 'Videos-After-Extraction/Numbers/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
        
        if word.name in adverbs:
            new_index = len(os.listdir('Videos-After-Extraction/Adverb/'))
            fileName = 'Videos-After-Extraction/Adverb/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
        
        if word.name in alphabet:
            new_index = len(os.listdir('Videos-After-Extraction/Alphabet/'))
            fileName = 'Videos-After-Extraction/Alphabet/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
        
        if word.name == 'sil':
            new_index = len(os.listdir('Videos-After-Extraction/Silence/'))
            fileName = 'Videos-After-Extraction/Silence/{}_{}.mp4'.format(word.name, new_index)
            cutVideo(videoPath, fileName, start_time, end_time)
    

#WIP
def segmentDataSet(Path, Number_Of_Speakers):
    '''Function responsible for segmenting the whole dataset into separate word files '''
    for i in range(Number_Of_Speakers):
        videoPath = Path + "video/S{}/".format(i+1) + "*.mpg"
        videosGen =  glob.iglob(videoPath)
        try:
            for j in range(len(os.listdir(videoPath.split('*')[0]))):
                py = next(videosGen)
                segmentSingleVideo(py,getAlignFileName(py))
        except StopIteration:
            print("Segmented the dataset.")
    
    
#Test function for videos to check that frames are correct    
def getVideoFrames():
    vidcap = cv2.VideoCapture('Videos-After-Extraction/Adverb/0.mp4')
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imshow("frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print(count)    

####################################### MAIN CODE ############################################
dataSetPath = 'GP DataSet/'
numberSpeakers = 1
segmentDataSet(dataSetPath,numberSpeakers)