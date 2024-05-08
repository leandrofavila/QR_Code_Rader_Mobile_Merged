from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from pyzbar import pyzbar
import requests
import cv2

outputtext = ''
weblink = ''
leb = Label(text=outputtext,
            size=(200, 48),
            pos_hint={'center_x': 0.5},
            #font_name='caminho/para/sua/fonte.ttf',
            font_size=42
            )
found = set()
togglflag = True
barcodeData = ''

KV = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Qr Reader'
            left_action_items: [['menu', lambda x: x]]
            right_action_items: [['dots-vertical', lambda x: x]]
        TelaLogin:
<SenhaCard>:
    id: card
    orientation: 'vertical'
    size_hint: .7, .7
    pos_hint: {'center_x': .5, 'center_y': .5}
    MDBoxLayout:
        size_hint_y: .15
        padding: [25, 25, 0, 25]
        md_bg_color: app.theme_cls.primary_color

        MDLabel:
            text: 'Mudar senha'
        MDIconButton:
            pos_hint: {'center_x': .9, 'center_y': .5} 
            icon: 'close'
            on_release: root.fechar()

    MDFloatLayout: 
        MDTextField:
            pos_hint: {'center_x': .5, 'center_y': .8}
            size_hint_x: .9
            hint_text: 'Código enviado por email'
        MDTextField:
            pos_hint: {'center_x': .5, 'center_y': .6}
            size_hint_x: .9
            hint_text: 'Nova senha'
        MDTextField:
            pos_hint: {'center_x': .5, 'center_y': .4}
            size_hint_x: .9
            hint_text: 'Confirmar senha'                
        MDRaisedButton:
            text: 'Recadastrar'
            pos_hint: {'center_x': .5, 'center_y': .15}

<TelaLogin@FloatLayout>:      
    MDIconButton:
        pos_hint: {'center_x': .5, 'center_y': .8}
        icon: 'language-python'
        icon_size: '75sp'

    MDTextField:
        id: cracha
        size_hint_x: .9
        hint_text: 'Crachá:'
        pos_hint: {'center_x': .5, 'center_y': .6}

    MDTextField:
        id: senha
        size_hint_x: .9
        hint_text: 'Senha:'
        pos_hint: {'center_x': .5, 'center_y': .5}

    MDRaisedButton:
        size_hint_x: .9
        text: 'LOGIN' 
        size_hint_y: .12
        pos_hint: {'center_x': .5, 'center_y': .4}  
        on_release: root.con_api()

    Label:
        id: mensagem
        text: ''  # Inicialmente vazio
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        color: 1, 0, 0, 1

    MDLabel:
        text: 'Esqueceu sua senha?'  
        halign: 'center'
        pos_hint: {'center_y': .3} 

    MDTextButton:
        text: 'Clique aqui!'
        pos_hint: {'center_x': .5, 'center_y': .25}   
        on_release: root.abrir_card()                          
'''

KV_second_screen = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Qr Reader'
        TelaLogin:
<SecondScreen@BoxLayout>: 
    MDLabel:
        id: mensagem
        text: ''
        text: 'Esqueceu sua senha?'  
        halign: 'center'
        pos_hint: {'center_y': .3}          
'''


class SenhaCard(MDCard):
    def fechar(self):
        self.parent.remove_widget(self)


class TelaLogin(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def abrir_card(self):
        self.add_widget(SenhaCard())


    def con_api(self):
        cracha = self.ids.cracha.text
        senha = self.ids.senha.text
        print(cracha, senha)
        url = f"http://10.40.3.78:7282/Login?code={str(cracha)}&password={str(senha)}"
        try:
            response = requests.post(url)

            if response.status_code == 200:
                print(response.json())
                token = response.json()['data']['token']
                user = response.json()['data']['user']['name']
                print("Token:", token)
                print("User:", user)
                return response.json()
            else:
                print("Error Code:", response.status_code)
                self.ids.mensagem.text = "Erro ao conectar."
                return False

        except Exception as err:
            print("Erro:", err)
            self.ids.mensagem.text = "Erro ao conectar, servidor ausente."
            return False


    def change_screen(self, *args):
        main_app.sm.current = 'main'


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.cam = cv2.VideoCapture("http://192.168.137.244:4747/video")
        self.cam.set(3, 1280)
        self.cam.set(4, 720)
        self.img = Image()
        self.add_widget(self.img)
        Clock.schedule_interval(self.update, 1.0 / 30)


    def update(self, dt):
        if togglflag:
            ret, frame = self.cam.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img.texture = image_texture

                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = f"{barcodeData}"
                    print(text)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    if barcodeData not in found:  #check if detected barcode is a duplicate
                        outputtext = text
                        leb.text = outputtext
                        found.add(barcodeData)
                    self.change_screen()


    def stop_stream(self, *args):
        self.cam.release()  # para a camera


    def change_screen(self, *args):
        main_app.sm.current = 'second'  # once barcode is detected, switch to second screen


KV_second_screen = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Qr Reader'
        TelaLogin:
<SecondScreen@BoxLayout>: 
    MDLabel:
        id: mensagem
        text: ''
        text: 'Esqueceu sua senha?'  
        halign: 'center'
        pos_hint: {'center_y': .3}          
'''


class SecondScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.ok = Button(text='OK',
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
        self.add_widget(self.ok)
        self.add_widget(self.cancel)


    def return_to_main_screen(self, *args):
        main_app.sm.current = 'main'



class QRApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_hue = '500'

        scrn = Screen(name='login')
        #scrn.add_widget(TelaLogin())
        Builder.load_string(KV)


        self.sm = ScreenManager()

        scrn_mai = Screen(name='main')
        scrn.add_widget(MainScreen())
        self.sm.add_widget(scrn_mai)

        scrn_sec = Screen(name='second')
        scrn.add_widget(SecondScreen())
        self.sm.add_widget(scrn_sec)

        return self.sm


if __name__ == '__main__':
    main_app = QRApp()
    main_app.run()
    cv2.destroyAllWindows()
