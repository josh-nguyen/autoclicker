# Autoclicker 
Autoclicker to simulate left mouse clicks 

The autoclicker has a recording phase and an autoclicking phase

Recording 
* When the program is run, all user left mouse clicks will be appended to a click list 
* Press 'p' to pause the recording. ie: no further clicks will be added to the list until you press 'p' again
* Press 'r' to restart the recording: the current click list will be deleted
* Press 'v' to view the list of points that are in the click list
* Press 'x' to stop recording and begin autoclicking 

Autoclicking
* Press 'p' to exit the program. 
* The default sleep time between clicks is 0.5 seconds.

Requirements
* pyautogui, pynput, keyboard is required. 
* to install, run:  pip install -r requirements.txt
