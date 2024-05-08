from kivymd.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import NumericProperty



KV_second_screen = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        SecondScreen:
<SecondScreen@FloatLayout>: 
    Label:
        id: mensagem
        text: ''  # Inicialmente vazio
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        color: 1, 0, 0, 1  
     
    MDRaisedButton:
        size_hint_x: .9
        text: 'OK' 
        size_hint_y: .12
        pos_hint: {'center_x': .5, 'center_y': .4}  
        on_release: root.set_message()
        
    MDRaisedButton:
        size_hint_x: .9
        text: 'CANCEL' 
        size_hint_y: .12
        pos_hint: {'center_x': .5, 'center_y': .2}  
        on_release: root.return_to_main_screen()               
'''


class SecondScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.leb = NumericProperty(2)


    def set_message(self):
        self.ids.mensagem.text = str(self.leb)

    def return_to_main_screen(self, *args):
        main_app.sm.current = 'main'



class QRApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_hue = '500'

        return Builder.load_string(KV_second_screen)



if __name__ == '__main__':
    main_app = QRApp()
    main_app.run()
