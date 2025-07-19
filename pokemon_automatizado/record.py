import pyautogui
from pynput.keyboard import Listener
from pynput import keyboard
import time
import json
import os
import config

def create_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)


class Record:
    def __init__(self):
        self.count = 0
        self.coordinates = []
        create_folder(config.POKE_NAME)


    def photo(self):
        x, y = pyautogui.position()
        print_screen = pyautogui.screenshot(region=(x - 8, y - 8, 16, 16))
        path = '{1}/flag_{0}.png'.format(self.count, config.POKE_NAME)
        print_screen.save(path)
        self.count = self.count +1
        infos = {
            "path": path,
            "blink_move": [], 
            "wait": 0,
            "start": None
        }
        self.coordinates.append(infos)


    def stopwatch(self):
        last_cordinates = self.coordinates[-1]
        if last_cordinates["start"] is None:
            last_cordinates["start"] = time.time()
        else:
            last_cordinates["wait"] =  time.time() - last_cordinates["start"]
            del last_cordinates["start"]
        print(last_cordinates)


    def blink_move_position(self):
        x , y = pyautogui.position()
        last_cordinates = self.coordinates[-1]
        last_cordinates["blink_move"] = [x , y]
        print(last_cordinates)


    def key_code(self, key):
        if key == keyboard.Key.end:
            with open('{0}/{0}.json'.format(config.POKE_NAME), 'w') as file:
                file.write(json.dumps(self.coordinates))
            return False
        if key == keyboard.Key.insert:
            self.photo()
        if key == keyboard.Key.home:
            self.blink_move_position()
            pyautogui.leftClick()
        if key == keyboard.Key.page_up:
            self.stopwatch()
        if key == keyboard.Key.page_down:
            self.stopwatch()
        print(key)

    def start(self):
        with Listener(on_press=self.key_code) as listener:
            listener.join()


Bot_record = Record ()
Bot_record.start()