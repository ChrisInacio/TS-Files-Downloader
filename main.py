#############################
# LIBRARIES
#############################
# Send HTTP requests
import requests
# Usage of operating system dependent functionality
import os
# High-level operations on files
from shutil import copyfile as cpFile
# Library to use time.sleep
import time
# Library to import csv files
import csv
# Collection of complex mathematical operations suitable for processing statistical data
import numpy as np
# Libraries to combine multiple mp4 files
from moviepy.editor import *
from natsort import natsorted
# Libraries to open file pick dialog
import tkinter as tk
from tkinter import filedialog

print ("-----TS Files Downloader (Console version)-----\n")

#############################
# PICK TS FILE
#############################
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename() # Get the file path with the file dialog
filePathComponents = file_path.split('/', -1) # Split the file path by delimiter
tsFileName = filePathComponents[-1] # Select the part that corresponds to the file name
print('Links file selected!\n')

#############################
# MAIN
#############################
mainDirectory = os.path.dirname(os.path.realpath(__file__)) # Get current working directory
os.chdir(os.path.dirname(os.path.realpath(__file__))) # Set current working directory

# Create CSV file
try:
    fileCopyName = tsFileName + '-copy'
    fileRenameName = tsFileName + '-csv.csv'
    cpFile(tsFileName, fileCopyName) # Make a copy of the original file
    os.rename(fileCopyName, fileRenameName) # Rename the copy of the original file
    print('CSV file created!\n')
except:
    print('CSV file already created!\n')

# Import csv file
with open(fileRenameName, newline='') as csvfile:
    data = list(csv.reader(csvfile))

# Returns an array that contains all the elements of the list
linksArray = np.asarray(data, dtype=None)

# Convert array of objects to array of strings and delete all elements except the links
links = []
for arrayIndex, indexContent in enumerate(linksArray):
    contentStr = ''.join(linksArray[arrayIndex]) # Converts array element to string
    if not(contentStr.startswith('#')): # Check if element doesn't start with char #
        contentStr = 'https:' + contentStr # add https: to the beggining of each string
        links.append(contentStr) # save link to string array

# Folder name created where the current .py file is located
videoFolderName = "Media"

# Check the directory folder exists before creating a new one
if not(os.path.isdir(videoFolderName)):
    os.makedirs(videoFolderName) # Create a folder to download the files into
    print('Creating download folder!\n')
else:
    print('Folder already created!\n')

os.chdir(videoFolderName) # Change the current directory to that folder

# Make sure the connection to the server stays open and configured and also persist cookies
session = requests.Session()

print ("-----Starting Download!-----\n")

# For loop will cycle through every link, downloading them and placing then in the  assigned folder
for videoNumber, downloadLink in enumerate(links):
    print ("Downloading video  %d.. " % (videoNumber), downloadLink)
    fileName = '%04d.mp4' % videoNumber # Assign new file name
    file = open(fileName, 'wb') # Open a new file to place downloaded data
    
    req = session.get(downloadLink) # Request the data from the URL if using session

    for chunk in req.iter_content(100000):
        file.write(chunk) # Put the data into the file
    file.close() # Close the file
    
    time.sleep(1) # Sleep for 1 second to make sure the server is not rate-limiting the connection

print ("\n-----Download complete!-----\n")

# Combine all videos into a single video file
L =[]
for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))): 
    files = natsorted(files)
    for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)
            
final_clip = concatenate_videoclips(L)
outputFileName = r'output-' + str(tsFileName) + '.mp4'
final_clip.to_videofile(outputFileName, fps=30, remove_temp=True)

# Delete AUX files
print('\n-----Removing AUX video files!-----\n')
for x in range(len(links)):
    if x < 10:
        videoToBeRemoved = r'000' + str(x) + '.mp4'
    elif x >= 10 and x < 100:
        videoToBeRemoved = r'00' + str(x) + '.mp4'
    elif x >= 100 and x < 1000:
        videoToBeRemoved = r'0' + str(x) + '.mp4'
    elif x >= 1000:
        videoToBeRemoved = str(x) + '.mp4'
    print('Removing file: ', videoToBeRemoved)
    os.remove(videoToBeRemoved)
print('\n-----Removing AUX links files!-----\n')
os.chdir(mainDirectory) # change to the current working directory
print('Removing file: ', fileRenameName)
os.remove(fileRenameName)

print('\n-----DONE!-----')