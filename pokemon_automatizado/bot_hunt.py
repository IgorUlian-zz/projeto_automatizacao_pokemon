import pyautogui
from pynput.keyboard import Listener
from pynput import keyboard
import threading
import json
from actions import Actions
from time import sleep
import config

class Hunt:

    def __init__(self):
        self.isStarded = True
        with open('{0}/{0}.json'.format(config.POKE_NAME), 'r') as file:
            infos = file.read()
        self.infos = json.loads(infos) 
        self.actions = Actions()

    
    def go_to_flag(self, item):
        try:
            for i in range(3):
                flag_position = pyautogui.locateOnScreen(item['path'], confidence=0.75)
                if flag_position is None:
                    return
                self.actions.move_to_and_click(flag_position)
                sleep(item["wait"])
                print("Bandeira encontrada:", flag_position)
            else:
                print("Bandeira não encontrada")
        except pyautogui.ImageNotFoundException:
            print("Image not Found - Flag")


    def go_attack(self, time, item):
        try:
            for i in range(time):
                if pyautogui.locateOnScreen('{0}/{0}.png'.format(config.POKE_NAME), confidence=0.75) is not None:
                    print("Pokemon Encontrado")
                    pyautogui.press('f')
                    pyautogui.press('tab', presses=3)
                    self.actions.check_life('Vida', 3, *config.POSITION_LIFE, config.COLOR_LIFE, '1')
                    self.actions.check_energy('Energia', 3, *config.POSITION_ENERGY, config.COLOR_ENERGY, '2')
                    self.actions.attack()
                    self.actions.check_life('Vida', 3, *config.POSITION_LIFE, config.COLOR_LIFE, '1')
                    self.actions.check_energy('Energia', 3, *config.POSITION_ENERGY, config.COLOR_ENERGY, '2')
                    self.actions.poke_stop()
                else:
                    pyautogui.press('1')
                    pyautogui.press('f')
                    print("Pokemon Não Encontrado") 
                    break  
        except pyautogui.ImageNotFoundException:
            print("Image not Found - Pokemon")


    def moviment(self, item):
        try:
            position = pyautogui.locateOnScreen('screens/order.png', confidence=0.75)
            print("Hora de posicionar o Pokemon")
            for i in range(3):
                if position is None:
                    return
                self.actions.move_to_and_click(position)
                pyautogui.rightClick()
                sleep(0.2)
                pyautogui.moveTo(item["blink_move"][0], item["blink_move"][1], 0.1)
                sleep(0.2)
                pyautogui.leftClick()
            else:
                print("Pokemon não posicionado")
            print("Pokemon Posicionado")
            self.actions.poke_stop()
        except pyautogui.ImageNotFoundException:
            print("Image not Found - Position")


    def collect_items(self, item):
            pyautogui.moveTo(item["blink_move"][0], item["blink_move"][1], 0.1)
            sleep(0.5)
            pyautogui.rightClick()
            sleep(3)
            pyautogui.press('e')
            print("Tentativa de Loot Completa")
            self.actions.check_death(3)


    def start_hunt(self):
        while self.isStarded:
            for item in self.infos:
                self.go_to_flag(item)
                self.moviment(item)
                self.go_attack(5, item)
                self.collect_items(item)


    def target_key(self, key):
        print(key)
        if key == keyboard.Key.end:
            return False
        if key == keyboard.Key.delete:
            threading.Thread(target=self.start_hunt).start()


    def start_keyboard(self):
        with Listener(on_press=self.target_key) as listener:
            listener.join()


hunt = Hunt()
hunt.start_keyboard()