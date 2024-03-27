from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import FloatLayout
from kivy.lang import Builder


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
        size_hint_x: .9
        hint_text: 'Email:'
        pos_hint: {'center_x': .5, 'center_y': .6}
               
    MDTextField:
        size_hint_x: .9
        hint_text: 'Senha:'
        pos_hint: {'center_x': .5, 'center_y': .5}
    
    MDRaisedButton:
        size_hint_x: .9
        text: 'LOGIN' 
        size_hint_y: .12
        pos_hint: {'center_x': .5, 'center_y': .4}  
        
    MDLabel:
        text: 'Esqueceu sua senha?'  
        halign: 'center'
        pos_hint: {'center_y': .3} 
        
    MDTextButton:
        text: 'Clique aqui!'
        pos_hint: {'center_x': .5, 'center_y': .25}   
        on_release: root.abrir_card()                          
'''
#size_hint recebe uma tupla com valor para x e y onde 1 é o valor maximo.



class SenhaCard(MDCard):
    def fechar(self):
        self.parent.remove_widget(self)


class TelaLogin(FloatLayout):
    def abrir_card(self):
        self.add_widget(SenhaCard())

###requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer==2.1.0


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_hue = '500'
        return Builder.load_string(KV)


MyApp().run()

