from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder


class HotReload(MDApp):
    KV_FILES = ['QR_pomo.kv']
    DEBUG = True

    def build(self):
        return Builder.load_file(self.KV_FILES[0])


HotReload().run()
