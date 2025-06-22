import re
import kivy
import hashlib

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.utils.data_manager import DataManager

Builder.load_string("""
<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "5dp"
        padding: "20dp"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: "5dp"

            MDRectangleFlatButton:
                text: "Import data"
                on_release: root.import_data()
                size_hint_x: 0.5
                font_size: "12sp"

            MDRectangleFlatButton:
                text: "Export data"
                on_release: root.export_data()
                size_hint_x: 0.5
                font_size: "12sp"

        MDTextField:
            id: master_password
            hint_text: "Master Password"
            password: True
            icon_right: "key-variant"
            mode: "fill"
            size_hint_x: 1

        MDRectangleFlatButton:
            id: valide_password
            text: "Validate Password"
            on_release: root.password_validate()
            size_hint_x: 1
        
        MDRectangleFlatButton:
            id: reset_data
            text: "Reset Data"
            on_release: root.reset_data()
            size_hint_x: 1
""")


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.data_manager = DataManager()

    def password_validate(self):
        master_password = self.ids.master_password.text
        valid = True

        if len(master_password) < 8:
            valid = False
            self.show_popup(
                "Error", "Master password must be at least 8 characters long.")

        if valid and not re.match(r"^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*\d)(?=.*[A-Z])", master_password):
            valid = False
            self.show_popup(
                "Error", "Master password must contain at least one special character, one digit, and one uppercase letter.")

        if valid:
            key = hashlib.pbkdf2_hmac(
                "sha256", master_password.encode("utf-8"), b"", 100000)
            del (master_password)
            if self.data_manager.load_data(key) is None:
                valid = False
                self.show_popup(
                    "Error", "Failed to validate the master password.")
            else:
                app = MDApp.get_running_app()
                app.root.screen_manager.current = "generator"
                generator_screen = app.root.screen_manager.get_screen(
                    "generator")
                generator_screen.key = key

    def show_popup(self, title, message, dismiss=None):
        text = Label(text=message, halign='center', valign='middle', text_size=(
            Window.width * 0.8, None))
        popup = Popup(title=title, content=text, size_hint=(0.9, 0.25))
        if dismiss:
            popup.bind(on_dismiss=dismiss)
        popup.open()

    def import_data(self):
        if kivy.platform == 'win':
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()
            if file_path:
                if file_path.lower().endswith(".json"):
                    self.data_manager.import_data(file_path)
                    self.show_popup("Info", "Import successful")

            root.destroy()

        else:
            from androidstorage4kivy import Chooser, SharedStorage

            def chooser_callback(shared_file_list):
                kivy.Logger.warning('AHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')

            chooser = Chooser(chooser_callback)
            chooser.choose_content('*/*')

    def exit_manager(self, path):
        self.file_manager.close()

    def export_data(self):
        master_password = self.ids.master_password.text
        key = hashlib.pbkdf2_hmac(
            "sha256", master_password.encode("utf-8"), b"", 100000)
        del (master_password)
        if self.data_manager.load_data(key) is None:
            self.show_popup(
                "Error", "Failed to validate the master password.")
        else:
            if kivy.platform == 'win':
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()

                file_path = filedialog.askdirectory()
                print(file_path)
                if file_path:
                    self.data_manager.export_data("data.json", file_path)
                    root.destroy()
                    self.show_popup("Info", "Export successful")
            elif kivy.platform == 'android':
                self.data_manager.export_data("data.json")
                self.show_popup("Info", "Export successful")

    def reset_data(self):
        master_password = self.ids.master_password.text
        key = hashlib.pbkdf2_hmac(
            "sha256", master_password.encode("utf-8"), b"", 100000)
        del (master_password)
        if self.data_manager.load_data(key) is None:
            self.show_popup(
                "Error", "Failed to validate the master password.")
        else:
            self.data_manager.reset_data("data.json")
            self.show_popup("Info", "Reset data successful")
