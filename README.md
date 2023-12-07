# Autoclicker 
Autoclicker to simulate left mouse clicks 

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

**Autoclicking**
* Press 'p' to pause/resume the autoclicks 
  * Once paused, you are able to modify the click list:
    * Press 'a' to toggle adding new clicks the click list 
    * The view ,delete, and restart keybinds and functionality work the same as before

**Requirements**
* pyautogui, pynput, keyboard is required. 
* to install run pip install -r requirements.txt
