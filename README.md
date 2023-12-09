# Autoclicker 
Autoclicker to simulate left mouse clicks in sequence

The autoclicker has a recording phase and an autoclicking phase

**Press 'e' to exit the program at any time.**

**Recording**
* When run, all user left mouse clicks will be appended to a click list 
* Press 'p' to pause/resume the recording. ie:
once you pause, no further clicks will be added to the list until you press 'p' again to resume
* Press 'd' to delete the last click in the recording
* Press 'r' to restart the recording: the current click list will be deleted
* Press 'v' to view the list of points that are in the click list
* Press 'x' to stop recording and begin autoclicking
* Press 's' to change autoclick speed

**Autoclicking**

* The autoclicker will click in the order that you recorded the clicks in
* Press 'p' to pause/resume the autoclicks 
  * Once paused, you are able to modify the click list:
    * Press 'a' to toggle adding new clicks the click list 
    * The view ,delete, and restart, changing speed keys work the same as before
    * To start autoclicking from the first position, press '1'. i.e, The autoclicker will reset to the first position in your recording 

**Requirements**
* pyautogui, pynput, keyboard is required. 
* to install run pip install -r requirements.txt
