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
import time as timeLib
# Library to import csv files
import csv
# Collection of complex mathematical operations suitable for processing statistical data
import numpy as np
# Libraries to combine multiple mp4 files
# from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
# Libraries to open file pick dialog
import tkinter as tk
from tkinter import filedialog
# Library to exit a script
import sys
# Library to generate timestamps to video file name
from datetime import datetime

print ("-----TS Files Downloader (Console version)-----")

#############################
# INITIAZATION
#############################
mainDirectory = os.path.dirname(os.path.realpath(__file__)) # Get current working directory
os.chdir(os.path.dirname(os.path.realpath(__file__))) # Set current working directory

#############################
# AUXILIARY FUNCTIONS
#############################
def showMenu():
    print ("\nSelect an option:")
    print ("1) Video URL (only works for Dark.Video)")
    print ("2) Select a file")
    print ("3) Exit")
    data = int(input("Enter your choice: "))
    return data

def showDownloadOptions():
    print ("\nSelect the video quality you want to download:")
    print ("1) 240p")
    print ("2) 320p")
    print ("3) 480p")
    print ("4) 720p")
    print ("5) 1080p")
    data = int(input("Enter your choice: "))
    return data

#############################
# INPUT METHOD SELECTION
#############################
selectedOption = showMenu()
keepCycleAlive = True
while keepCycleAlive:
    if selectedOption == 1:
        keepCycleAlive = False
        videoUrl = str(input("\nPaste your URL here: "))
    elif selectedOption == 2:
        keepCycleAlive = False
        print("\nOpening file dialog...")
    elif selectedOption == 3:
        keepCycleAlive = False
        print("\nExiting...")
        sys.exit(0)
    else:
        print("\nUnavaiable option. Try again!")
        selectedOption=showMenu()

#############################
# PASTE URL OF VIDEO
#############################
if selectedOption == 1:
    urlSourceCode = requests.get(videoUrl) # Request source code of URL
    urlSourceCodeText = urlSourceCode.text # Extract the text of the source code
    sources = urlSourceCodeText.split('<source src=') # Split the source code to seperate the links from the rest
    sourcesArray = np.asarray(sources, dtype=None) # Returns an array that contains all the elements of the list
    sourcesArray = np.delete(sourcesArray, 0) # Delete first element of array (text before the links)
    sourcesArrayModified = sourcesArray # Make copy of array

    # Delete every char before https and after the end of the link
    for arrayIndex, indexContent in enumerate(sourcesArray):
        str = indexContent
        index = str.find('https') # Stores the index of a substring or char
        str = str[index:] # Discards whatever is before https
        index = str.find('type') # Stores the index of a substring or char
        str = str[:index-2] # Discards whatever is after the end of the link
        sourcesArrayModified[arrayIndex] = str # Saves the clean URL string to an array
        
    sourcesArray = sourcesArrayModified # Update original array
    # Delete unwanted variables
    del urlSourceCode, urlSourceCodeText, sources, sourcesArrayModified, arrayIndex, indexContent, str, index

    ###############################################
    # ALLOW THE USER TO CHOOSE VIDEO QUALITY
    ###############################################
    selectedOptionQuality = showDownloadOptions()
    keepCycleAlive = True
    videoQualityUrl = ''
    while keepCycleAlive:
        if selectedOptionQuality == 1:
            try:
                videoQualityUrl =  sourcesArray[0]
                keepCycleAlive = False
            except:
                print("\nQuality unavailable! Try another one!")
                keepCycleAlive = True
        elif selectedOptionQuality == 2:
            try:
                videoQualityUrl =  sourcesArray[1]
                keepCycleAlive = False
            except:
                print("\nQuality unavailable! Try another one!")
                keepCycleAlive = True
        elif selectedOptionQuality == 3:
            try:
                videoQualityUrl =  sourcesArray[2]
                keepCycleAlive = False
            except:
                print("\nQuality unavailable! Try another one!")
                keepCycleAlive = True
        elif selectedOptionQuality == 4:
            try:
                videoQualityUrl =  sourcesArray[3]
                keepCycleAlive = False
            except:
                print("\nQuality unavailable! Try another one!")
                keepCycleAlive = True
        elif selectedOptionQuality == 5:
            try:
                videoQualityUrl =  sourcesArray[4]
                keepCycleAlive = False
            except:
                print("\nQuality unavailable! Try another one!")
                keepCycleAlive = True
        else:
            print("\nUnavaiable option. Try again!")
            
        # If the selected option wasn't available, let user choose another one
        if keepCycleAlive:
            selectedOptionQuality = showDownloadOptions()
            
    ###############################################
    # DOWNLOAD THE FILE BASED ON THE URL CHOOSEN
    ###############################################
    now = datetime.now() # Retrieve current date and time
    year = now.strftime("%Y") # Get current year
    month = now.strftime("%m") # Get current month
    day = now.strftime("%d") # Get current day
    time = now.strftime("%H-%M-%S") # Get current time
    # Build the filename
    generatedFileName = 'video-ts-fragments-' + year + '-' + month + '-' + day + '-' + time
    
    print("\nDownloading the file...")
    r = requests.get(videoQualityUrl) # Download the file
    with open(generatedFileName, 'wb') as f:
        print("\nWriting the file to current directory...")
        f.write(r.content) # Write the file

    # Make file name attribution
    tsFileName = generatedFileName
    
    del keepCycleAlive, now, year, month, day, time, generatedFileName

#############################
# PICK TS FILE
#############################
if selectedOption == 2:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename() # Get the file path with the file dialog
    filePathComponents = file_path.split('/', -1) # Split the file path by delimiter
    tsFileName = filePathComponents[-1] # Select the part that corresponds to the file name
    print('\nLinks file selected!')

#############################
# MAIN
#############################
# Create CSV file
try:
    fileCopyName = tsFileName + '-copy'
    fileRenameName = tsFileName + '-csv.csv'
    cpFile(tsFileName, fileCopyName) # Make a copy of the original file
    os.rename(fileCopyName, fileRenameName) # Rename the copy of the original file
    print('\nCSV file created!\n')
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
videoFolderName = "Downloads"

# Check the directory folder exists before creating a new one
if not(os.path.isdir(videoFolderName)):
    os.makedirs(videoFolderName) # Create a folder to download the files into
    print('Creating downloads folder!\n')
else:
    print('Downloads folder already created!\n')

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
    
    timeLib.sleep(1) # Sleep for 1 second to make sure the server is not rate-limiting the connection

print("\n-----Download complete!-----\n")

# Combine all clips into a single video file
keepCycleAlive = True
while keepCycleAlive:
    try:
        L = []
        print('\nAttempting to combine videos')
        for root, dirs, files in os.walk('.'):
            for filename in files:
                # Check if the filename starts with 'output' to discard any complete downloaded videos
                if not(filename.startswith('output')):
                    filePath = os.path.join(root, filename)
                    clip = VideoFileClip(filePath)
                    L.append(clip)
                    print('.')
                    del clip
        keepCycleAlive = False
    except:
        print('\nError occurred while attempting to merging videos! Trying again...')
       
final_clip = concatenate_videoclips(L)
outputFileName = r'output-' + str(tsFileName) + '.mp4'
final_clip.write_videofile(outputFileName, fps=30, remove_temp=True)

# Close the videos for efficiency
final_clip.close()
for x in range(len(L)):
    L[x].close()

# Delete all the videos
del L, root, dirs, files, final_clip, filePath, outputFileName

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
print('Removing file: ', tsFileName)
os.remove(tsFileName)

# Delete unwanted variables
del arrayIndex, chunk, contentStr, csvfile, data, downloadLink, f, file, fileCopyName, fileName, fileRenameName, indexContent
del links, linksArray, r, req, selectedOption, selectedOptionQuality, session, sourcesArray, tsFileName
del videoFolderName, videoNumber, videoQualityUrl, videoToBeRemoved, x

print('\n-----DONE!-----')
