import time
import pyautogui
import keyboard
from pynput import mouse
from threading import Thread, Lock

class AutoClicker:
    def __init__(self):
        self.click_positions_list = []
        self.recording_active = True
        self.autoclicking_active = True
        self.list_lock = Lock()
        self.add_clicks_mode = False
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()


    def on_click(self, x, y, button, pressed):
        if pressed and self.recording_active:
            with self.list_lock:
                self.click_positions_list.append((x, y))
            print(f"Clicked on {x}, {y}")

    def record_click_positions(self, stop_key ='x', pause_resume_key ='p', restart_key ='r', view_list_key = 'v'):
        print(f"Recording started. Press '{stop_key}' to stop recording.")
        print(f"Press '{pause_resume_key}' to pause/resume recording.")
        print(f"Press '{restart_key}' to restart recording.")
        print(f"Press '{view_list_key}' to view list of clicks.")

        try:
            while True:
                event = keyboard.read_event(suppress=True)
                key = event.name
                state = event.event_type

                if key == stop_key and state == keyboard.KEY_DOWN:
                    self.recording_active = not self.recording_active
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
                    with self.list_lock:
                        self.click_positions_list.clear()
                    print("Recording restarted")
                elif key == view_list_key and state == keyboard.KEY_DOWN:
                    print(self.click_positions_list)
                elif key == 'd' and state == keyboard.KEY_DOWN:
                    self.click_positions_list = self.click_positions_list[:-1]

            print("stopped")
        except KeyboardInterrupt:
            pass

        print("Recording stopped.")

    def run_autoclicker_logic(self):
        try:
            while True:
                if self.autoclicking_active and not self.add_clicks_mode:
                    with self.list_lock:
                        for x, y in self.click_positions_list:
                            print("Clicking at:", x, y)
                            pyautogui.click(x, y)
                            time.sleep(1)


        except KeyboardInterrupt:
            print("Autoclicker stopped.")

    def run_autoclicker(self, pause_resume_key='t', add_clicks_key='a'):
        sleep_time = 1
        print(
            f"Running autoclicker with an interval of {sleep_time} seconds. Press '{pause_resume_key}' to pause/resume. Press '{add_clicks_key}' to add clicks.")
        autoclicker_thread = Thread(daemon=True, target=self.run_autoclicker_logic)
        autoclicker_thread.start()

        try:
            while True:
                event = keyboard.read_event(suppress=True)
                key = event.name
                state = event.event_type

                if key == 'p':
                    break
                elif key == pause_resume_key and state == keyboard.KEY_DOWN:
                    self.autoclicking_active = not self.autoclicking_active
                    if self.autoclicking_active and self.resume:
                        print("Autoclicker resumed.")
                    else:
                        print("Autoclicker paused.")
                elif key == add_clicks_key and state == keyboard.KEY_DOWN:
                    print("autoclicker adding clicks mode")
                    self.add_clicks_mode = True
                    self.autoclicking_active = not self.autoclicking_active
                    self.recording_active = not self.recording_active
                    print(self.recording_active, "recording active")
                    print(self.autoclicking_active, "autoclicker active")
                elif key == 'v' and state == keyboard.KEY_DOWN:
                    print(self.click_positions_list)
                elif key == 'd' and state == keyboard.KEY_DOWN:
                    self.click_positions_list = self.click_positions_list[:-1]


        except KeyboardInterrupt:
            print("Main program stopped.")
        finally:
            self.listener.stop()
            self.listener.join()

    def check_key_pressed(self, stop_key='p'):
        print(f"Press {stop_key} to exit")
        keyboard.wait(stop_key)

if __name__ == "__main__":
    autoclicker = AutoClicker()

    record_thread = Thread(target=autoclicker.record_click_positions)
    autoclick_thread = Thread(daemon=True, target=autoclicker.run_autoclicker)
    exit_thread = Thread(target=autoclicker.check_key_pressed)

    try:
        print("Recording beginning")
        record_thread.start()
        record_thread.join()

        print("Autoclick beginning")
        exit_thread.start()
        autoclick_thread.start()
        exit_thread.join()

    except KeyboardInterrupt:
        print("CTRL+C detected. Stopping program.")











