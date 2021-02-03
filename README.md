# TS-Files-Downloader
Download multiple .ts files from URL's

###############################################
GET THE LINKS FILE
###############################################
1. Open page source of  the video ( Ctrl + U )
2. Search for "video-js" with the video-watch ID
3. Choose the URL for a specific quality (ie. 1080p)
4. Navigate to that URL and a file will be downloaded
5. Place the file in the same folder as main.py

###############################################
RUN THE PROGRAM
###############################################
5. Run the file run.bat
6. Pick the file you downloaded
7. Wait for the process to finish

###############################################
OUTPUT FILES
###############################################
- The downloaded file will be on the media folder
- All the .ts files are converted to mp4 and grouped to a single video file
- After the process finishes, all the auxiliary files will be removed automatically

###############################################
PROGRAM FAIL
###############################################
- If the process fails during the video merge, you must delete the merged video
and rerun the program.

###############################################
FUTURE UPGRADES
###############################################
- Skip the already downloaded video files in case of a program crash
- Delete merged video if the program crashes while merging it
- Create GUI program based on the same code

###############################################
NOTE
###############################################
This python script was created to download .ts files from Dark.Video
