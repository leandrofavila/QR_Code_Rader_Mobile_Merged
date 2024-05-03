from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
#from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
#from kivy.core.window import Window
from pyzbar import pyzbar
#import webbrowser
import cv2
#import requests


# Create global variables, for storing and displaying barcodes
outputtext = ''
weblink = ''
leb = Label(text=outputtext,
            size=(200, 48),
            pos_hint={'center_x': 0.5},
            #font_name='caminho/para/sua/fonte.ttf',
            font_size=42  # Tamanho da fonte em pontos
            )
found = set()  # this will not allow duplicate barcode scans to be stored
togglflag = True
barcodeData = ''


class MainScreen(BoxLayout):
    # first screen that is displayed when program is run
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # vertical placing of widgets

        self.cam = cv2.VideoCapture("http://192.168.137.244:4747/video")  # start OpenCV camera
        self.cam.set(3, 1280)  # set resolution of camera
        self.cam.set(4, 720)
        self.img = Image()  # Image widget to display frames

        self.add_widget(self.img)
        Clock.schedule_interval(self.update, 1.0 / 30)  # update for 30fps

    # update frame of OpenCV camera
    def update(self, dt):
        if togglflag:
            ret, frame = self.cam.read()  # retrieve frames from OpenCV camera

            if ret:
                buf1 = cv2.flip(frame, 0)  # convert it into texture
                buf = buf1.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img.texture = image_texture  # display image from the texture

                # detect barcode from image
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    #print(barcode)
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    #weblink = barcodeData
                    text = f"{barcodeData}"
                    print(text)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    if barcodeData not in found:  # check if detected barcode is a duplicate
                        outputtext = text
                        leb.text = outputtext  # display the barcode details
                        found.add(barcodeData)
                    self.change_screen()


    def stop_stream(self, *args):
        self.cam.release()  # stop camera


    def change_screen(self, *args):
        main_app.sm.current = 'second'  # once barcode is detected, switch to second screen


class SecondScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.but1 = Button(text='OK',
                           #on_press=self.make_api_request,
                           size_hint=(None, None),
                           size=(200, 48),
                           pos_hint={'center_x': 0.5})

        self.cancel = Button(text='Cancel',
                            on_press=self.return_to_main_screen,
                            size_hint=(None, None),
                            size=(200, 48),
                            pos_hint={'center_x': 0.5})

        self.add_widget(leb)
        self.add_widget(self.but1)
        self.add_widget(self.cancel)


    def return_to_main_screen(self, *args):
        main_app.sm.current = 'main'
        barcodeData = ''



class QRApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.mainsc = MainScreen()
        scrn = Screen(name='main')
        scrn.add_widget(self.mainsc)
        self.sm.add_widget(scrn)
        self.secondsc = SecondScreen()
        scrn = Screen(name='second')
        scrn.add_widget(self.secondsc)
        self.sm.add_widget(scrn)

        return self.sm


if __name__ == '__main__':
    main_app = QRApp()
    main_app.run()
    cv2.destroyAllWindows()
