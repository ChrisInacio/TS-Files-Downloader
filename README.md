# TS Files Downloader
- Download multiple .ts files from URL's
- Can also be used to download videos from Dark.Video

______________________
ISSUES (WILL BE FIXED IN THE FUTURE)
- Program will crash if the video being merged is too big. Issue is probably related to system memory since for 1 specific video sometimes it works, while other times it does not.
 
______________________
DOWNLOAD VIDEOS USING TS LINKS FILE

1. Open page source of  the video ( Ctrl + U )
2. Search for "video-js" with the video-watch ID
3. Choose the URL for a specific quality (ie. 1080p)
4. Navigate to that URL and a file will be downloaded
5. Place the file in the same folder as main.py
6. Run the file run.bat
7. Select the option to pick a file
8. Pick the file you downloaded
9. Wait for the process to finish
______________________
DOWNLOAD VIDEOS USING DARK.VIDEO LINKS

1. Run the file run.bat
2. Select the option to input link
3. Input the video link
4. Select the video quality
5. Wait for the process to finish
______________________
OUTPUT FILES:

- The downloaded file will be on the 'Downloads' folder
- All the .ts files are converted to mp4 and grouped to a single video file
- After the process finishes, all the auxiliary files will be removed automatically
- The video name will be based on a timestamp, so any video downloaded will always have a different name
