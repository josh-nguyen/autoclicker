import time
import pyautogui
import keyboard
from pynput import mouse
from threading import Thread, Lock

class AutoClicker:
    def __init__(self):
        self.click_positions_list = []
        self.recording_active = True
        self.list_lock = Lock()

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

        listener = mouse.Listener(on_click=self.on_click)
        listener.start()

        try:
            while True:
                event = keyboard.read_event(suppress=True)
                key = event.name
                state = event.event_type

                if key == stop_key and state == keyboard.KEY_DOWN:
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

        except KeyboardInterrupt:
            pass
        finally:
            listener.stop()

        print("Recording stopped.")

    def run_autoclicker(self):
        sleep_time = 0.5
        print(f"Running autoclicker with an interval of {sleep_time} seconds.")

        try:
            while True:
                with self.list_lock:
                    for x, y in self.click_positions_list:
                        if self.recording_active:
                            try:
                                pyautogui.click(x, y)
                                print(f"Clicked on {x}, {y}")
                            except Exception as e:
                                print(f"Error during click: {e}")
                            time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("Autoclicker stopped.")

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












