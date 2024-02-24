import kivy
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager

from login import LoginScreen
from generator import GeneratorScreen


class RootManager(MDBoxLayout):
    def __init__(self, **kwargs):
        super(RootManager, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.screen_manager = ScreenManager()

        self.login_screen = LoginScreen(name="login")
        self.screen_manager.add_widget(self.login_screen)

        self.password_widget = GeneratorScreen(name="generator", key="")
        self.screen_manager.add_widget(self.password_widget)

        self.add_widget(self.screen_manager)
        self.screen_manager.current = "login"


class PasswordGeneratorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        if kivy.platform == 'win':
            screen_width, screen_height = Window.size
            Window.size = (int(screen_width * 0.23), int(screen_height * 0.9))
            self.icon = "icon.png"
            self.title = "Kitpass"
        else:
            from android.permissions import request_permissions, Permission

            request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                                Permission.READ_EXTERNAL_STORAGE])

        return RootManager()


if __name__ == "__main__":
    PasswordGeneratorApp().run()
