import sys
import time
import pyautogui
import keyboard
from pynput import mouse
from threading import Thread, Lock

class AutoClicker:
    def __init__(self):
        self.click_positions_list = []
        self.recording_active = True
        self.autoclicking_active = False
        self.list_lock = Lock()
        self.add_clicks_mode = False
        self.sleep_time = 1
        self.current_click_index = 0
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()


    def on_click(self, x, y, button, pressed):
        if pressed and self.recording_active:
            self.click_positions_list.append((x, y))
            print(f"Added {x}, {y} to recording list")

    def record_click_positions(self, stop_key ='x', pause_resume_key ='p', restart_key ='r', view_list_key= 'v',
    delete_last_key= 'd', sleep_time_key = 's', exit_key = 'e'):
        print(f"Recording started. Press '{stop_key}' to stop recording.")
        print(f"Press '{pause_resume_key}' to pause/resume recording.")
        print(f"Press '{restart_key}' to restart recording.")
        print(f"Press '{view_list_key}' to view list of clicks.")
        print(f"Press '{delete_last_key}' to delete most recent recorded click.")
        print(f"Press '{sleep_time_key}' to change the autoclicker speed. The default sleep time is 1 second")
        print(f"Press '{exit_key}' to exit the program.")

        try:
            while True:
                event = keyboard.read_event(suppress=True)
                key = event.name
                state = event.event_type
                with self.list_lock:
                    if key == stop_key and state == keyboard.KEY_DOWN:
                        self.recording_active = not self.recording_active
                        self.autoclicking_active = True
                        break
                    elif key == pause_resume_key and state == keyboard.KEY_DOWN:
                        self.recording_active = not self.recording_active
                        if not self.recording_active:
                            print("Recording paused")
                            print(self.click_positions_list)
                        else:
                            print("Recording resumed")
                            print(self.click_positions_list)
                    elif key == restart_key and state == keyboard.KEY_DOWN:
                        print("Restarting recording")
                        with self.list_lock:
                            self.click_positions_list.clear()
                        print("Recording restarted")
                    elif key == view_list_key and state == keyboard.KEY_DOWN:
                        print(self.click_positions_list)
                    elif key == delete_last_key and state == keyboard.KEY_DOWN:
                        self.click_positions_list = self.click_positions_list[:-1]
                    elif key == sleep_time_key and state == keyboard.KEY_DOWN:
                        user_input_time = input("Enter a sleep time (seconds): ")
                        self.sleep_time= user_input_time
                        print(f"Autoclicker will run on interval: {self.sleep_time} seconds. Press {stop_key} to start autoclicking")
                    elif key == exit_key:
                        sys.exit()

        except KeyboardInterrupt:
            pass

        print("Recording stopped.")

    def run_autoclicker_logic(self):
        try:
            while True:
                if not self.autoclicking_active:
                    continue

                with self.list_lock:
                    list_length = len(self.click_positions_list)
                    for i in range(self.current_click_index, self.current_click_index + list_length):
                        if self.autoclicking_active:
                            index = i % list_length
                            x, y = self.click_positions_list[index]
                            print("Clicking at:", x, y)
                            pyautogui.click(x, y)
                            time.sleep(float(self.sleep_time))
                            self.current_click_index = i + 1

        except KeyboardInterrupt:
            print("Autoclicker stopped.")

    def toggle_autoclicker(self):
        self.autoclicking_active = not self.autoclicking_active
        if self.autoclicking_active:
            self.recording_active = False
            print("Autoclicker resumed.")
        else:
            print("Autoclicker paused.")

    def handle_additional_keys(self,additional_key,add_clicks_key = 'a',
    delete_last_key='d',pause_resume_key = 'p' ,view_list_key = 'v',
    restart_recording_key = 'r',from_first_key = '1', sleep_time_key = 's', exit_key = 'e'):

        if additional_key.name == add_clicks_key:
            print("Entering adding clicks mode")
            self.recording_active = not self.recording_active
        elif additional_key.name == delete_last_key:
            self.click_positions_list = self.click_positions_list[:-1]
            print(f"Deleting {self.click_positions_list[-1]}")
        elif additional_key.name == pause_resume_key:
            return True
        elif additional_key.name == view_list_key:
            with self.list_lock:
                print(self.click_positions_list)
        elif additional_key.name == restart_recording_key:
            print("Restarting recording")
            with self.list_lock:
                self.click_positions_list.clear()
        elif additional_key.name == from_first_key:
            print("Autoclicker will start click from first position")
            with self.list_lock:
                self.current_click_index = 0
        elif additional_key.name == sleep_time_key:
            user_input_time = input("Enter a sleep time (seconds): ")
            self.sleep_time = float(user_input_time)
            print(f"Autoclicker will run on interval: {self.sleep_time} seconds. Press {pause_resume_key} to resume autoclicking")
        elif additional_key.name == exit_key:
            sys.exit()
        return False

    def run_autoclicker(self, exit_key = 'e',pause_resume_key='p'):
        print(
            f"Running autoclicker on an interval of {self.sleep_time} seconds. "
            f"Press '{pause_resume_key}' to pause/resume")

        autoclicker_thread = Thread(daemon=True, target=self.run_autoclicker_logic)
        autoclicker_thread.start()

        try:
            additional_key_pressed = False  # After pause key press, an additional flag to track additional key press

            while True:
                event = keyboard.read_event(suppress=True)
                key = event.name
                state = event.event_type

                if key == exit_key:
                    break

                elif key == pause_resume_key and state == keyboard.KEY_DOWN:
                    self.toggle_autoclicker()

                    # Set the flag and continue reading events to avoid missing additional keys
                    additional_key_pressed = True

                # Check for additional keys only if the flag is set
                elif additional_key_pressed and state == keyboard.KEY_DOWN:
                    self.handle_additional_keys(event)

        except KeyboardInterrupt:
            print("Main program stopped.")
        finally:
            self.listener.stop()
            self.listener.join()

if __name__ == "__main__":
    autoclicker = AutoClicker()

    record_thread = Thread(daemon= True, target=autoclicker.record_click_positions)

    try:
        print("Recording beginning")
        record_thread.start()
        record_thread.join()

        print("Autoclick beginning")
        autoclicker.run_autoclicker()
    except KeyboardInterrupt:
        print("CTRL+C detected. Stopping program.")











