from itertools import cycle
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout

import cv2
from pyzbar.pyzbar import decode


class Cycle:
    def __init__(self):
        self.cycle = cycle([
            Timer(25), Timer(5),
            Timer(25), Timer(5),
            Timer(25), Timer(5),
            Timer(30)
        ])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.cycle)


class Timer:
    def __init__(self, time):
        self.time = time * 60

    def decrement(self):
        self.time -= 1
        return self.time

    def __str__(self):
        return '{:02d}:{:02d}'.format(*divmod(self.time, 60))


class Pomo(MDFloatLayout):
    timer_string = StringProperty('25:00')
    button_string = StringProperty('Iniciar!')
    running = BooleanProperty(False)
    cycle = Cycle()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._time = next(self.cycle)
        self.timer_string = str(self._time)

    def start(self):
        self.button_string = 'Pausar!'
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 1)

    def stop(self):
        self.button_string = 'Reiniciar!'
        if self.running:
            self.running = False

    def click(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def update(self, *args):
        time = self._time.decrement()
        if time == 0:
            self.stop()
            self._time = next(self.cycle)
        self.timer_string = str(self._time)


class PomoDuno(MDApp):
    def change_color(self):
        theme = self.theme_cls.theme_style
        if theme == 'Dark':
            self.theme_cls.theme_style = 'Light'
        else:
            self.theme_cls.theme_style = 'Dark'

    def build(self):
        self.theme_cls.primary_palette = 'DeepPurple'
        self.theme_cls.primary_hue = '700'
        return Builder.load_file('QR_pomo.kv')


if __name__ == "__main__":
    # Criar instância da classe do App
    app = PomoDuno()

    # Abrir a janela principal do Kivy
    app.run()

    # Iniciar o loop de leitura da câmera e detecção de QR code
    cap = cv2.VideoCapture("http://192.168.137.196:4747/video")
    while True:
        # Capturar um frame da câmera
        ret, frame = cap.read()

        # Detectar QR codes no frame
        decoded_objects = decode(frame)

        # Exibir os QR codes detectados
        for obj in decoded_objects:
            print("Data:", obj.data)

        # Exibir o frame
        cv2.imshow("Camera", frame)

        # Checar se a tecla 'q' foi pressionada para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar os recursos
    cap.release()
    cv2.destroyAllWindows()
