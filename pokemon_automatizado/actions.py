import pyautogui
import keyboard
from pynput.keyboard import Listener
from pynput import keyboard
from time import sleep
import config
from twilio.rest import Client

class Actions:

    def __init__(self):
        pass


    def move(self, imagem_position):
        x, y = pyautogui.center(imagem_position)
        pyautogui.moveTo(x, y, 0.3)

    
    def move_to_and_click(self, imagem_position):
        self.move(imagem_position)
        pyautogui.click()


    def check_life(self, name, delay, x, y, rgb, button_name):
        print(f'Checando {name} ... ')
        sleep(delay)
        if pyautogui.pixelMatchesColor(x, y, rgb):
            pyautogui.press(button_name)
            pyautogui.press('f10')
            sleep(0.3)
            pyautogui.press('f11')
            sleep(0.3)
            pyautogui.press('f12')


    def check_energy(self, name, delay, x, y, rgb, button_name):
        print(f'Checando {name} ... ')
        sleep(delay)
        if pyautogui.pixelMatchesColor(x, y, rgb):
            pyautogui.press(button_name)

    def check_cage(self, delay):
        try:
            print("Checando se houve jaulas usadas...")
            for i in range(3):
                sleep(delay)
                cage_close = pyautogui.locateOnScreen('screens/cage_close.png', confidence=0.75)
                cage_curta = pyautogui.locateOnScreen('screens/cage_curta.png', confidence=0.75)
                cage = pyautogui.locateOnScreen('screens/cage.png', confidence=0.75)
                if cage_close is None or cage_curta is None or cage is None:
                    return
                print("Houve uma jaula Usada!")
                self.send_message_whatsapp()
            else:
                print('Não houve jaula usadas')
        except pyautogui.ImageNotFoundException:
            print("Image not Found - Cage")

    def check_death(self, delay):
        try:
            print("Checando se você morreu...")
            for i in range(3):
                sleep(delay)
                death_warning = pyautogui.locateOnScreen('screens/death_warning.png', confidence=0.75)
                chansey = pyautogui.locateOnScreen('screens/chansey.png', confidence=0.75)
                if death_warning is None or chansey is None:
                    return
                print("Infelizmente você morreu.")
                self.send_message_whatsapp_death()
                break
            else:
                print('Continuando a Jornada...')
        except pyautogui.ImageNotFoundException:
            print("Image not Found - Death")


    def poke_stop(self):
        pyautogui.keyDown('shiftleft')
        sleep(0.1)
        pyautogui.press('s')
        sleep(0.1)
        pyautogui.keyUp('shiftleft')

    
    def use_cage(self):
        try:
            for i in range(3):
                if pyautogui.locateOnScreen('{0}/{0}.png'.format(config.POKE_NAME), confidence=0.75) is None:
                    break
            else:
                 self.poke_stop()
                 print("Enviando Jaulas")
                 for i in range(15):
                    pyautogui.press('tab')
                    sleep(0.1)
                    pyautogui.press('capslock')
                    sleep(0.1)
        except pyautogui.ImageNotFoundException:
            print("Image not Found - Pokemon")


    def attack(self):
            print("Hora de atacar")
            for i in range(2):
                sleep(0.4)  
                pyautogui.press('f4')
                sleep(0.4) 
                pyautogui.press('f5')
                sleep(0.4)  
                pyautogui.press('f6')
                sleep(0.4)  
                pyautogui.press('f7')
                sleep(0.4)  
                pyautogui.press('f8')
                sleep(0.4)  
                pyautogui.press('f9')
                sleep(0.4)  
                pyautogui.press('f10')
                sleep(0.4)  
                pyautogui.press('f11')
                sleep(0.4)  
                pyautogui.press('f12')


    def send_message_whatsapp(self):
        account_sid = 'Aqui você coloca o seu Account SID do Twilio'
        auth_token = 'Aqui você coloca o seu Auth Token do Twilio'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='whatsapp:+(Aqui o twilio vai te fornecer um número)',
        body='Foi utilizado uma Jaula, você tem 1 hora para verificar.',
        to='whatsapp:+55 (aqui você coloca o seu número com DDI e DDD, ex: +5511+ Seu número)'
        )

        print('Mensagem enviada no Whatsapp')

    def send_message_whatsapp_death(self):
        account_sid = 'Aqui você coloca o seu Account SID do Twilio'
        auth_token = 'Aqui você coloca o seu Auth Token do Twilio'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='whatsapp:+(Aqui o twilio vai te fornecer um número)',
        body='Você desmaiou, volte e verique seu Robô.',
        to='whatsapp:+55 (aqui você coloca o seu número com DDI e DDD, ex: +5511+ Seu número)'
        )

        print('Mensagem enviada no Whatsapp')
        pyautogui.press('end')