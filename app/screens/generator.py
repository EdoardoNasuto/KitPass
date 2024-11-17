from secrets import token_hex

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.utils.password import PasswordGenerator
from app.utils.data_manager import DataManager

Builder.load_string("""
<GeneratorScreen>:
    text_field_height: 0.5
    button_height: 0.3
    chip_height: 0.2
    label_height: 0.05
    
    MDBoxLayout :
        orientation: 'vertical'
        spacing: "5dp"
        padding: "20dp"

        MDTextField:
            id: domain
            hint_text: "Domain"
            on_text: root.update_entry(self, self.text)
            size_hint_y: root.text_field_height
            icon_right: "web"

        MDTextField:
            id: username
            hint_text: "Username"
            size_hint_y: root.text_field_height
            icon_right: "account"

        MDTextField:
            id: password_length
            hint_text: "Password Length"
            size_hint_y: root.text_field_height
            icon_right: "counter"

        MDChip:
            id: special_character
            text: "Special Characters"
            size_hint_x: 1
            size_hint_y: root.chip_height
            icon_left: "pound"
            active: True

        MDChip:
            id: remove_digits
            text: "Lowercases"
            size_hint_x: 1
            size_hint_y: root.chip_height
            icon_left: "numeric-off"
            active: True

        MDChip:
            id: remove_uppercase
            text: "Uppercases"
            size_hint_x: 1
            size_hint_y: root.chip_height
            icon_left: "alpha-a"
            active: True

        MDChip:
            id: digits_only
            text: "Digits"
            size_hint_x: 1
            size_hint_y: root.chip_height
            icon_left: "numeric"
            active: True

        MDLabel:
            size_hint_y: root.label_height

        MDRectangleFlatButton:
            text: "Generate Password"
            on_release: root.generate_password()
            size_hint_x: 1
            size_hint_y: root.button_height

        MDRectangleFlatButton:
            text: "Change Password"
            on_release: root.generate_new_salt()
            size_hint_x: 1
            size_hint_y: root.button_height
""")


class GeneratorScreen(Screen):
    def __init__(self, key, **kwargs):
        super(GeneratorScreen, self).__init__(**kwargs)
        self.data_manager = DataManager()
        self.checkbox_list = [
            self.ids.special_character,
            self.ids.remove_digits,
            self.ids.remove_uppercase,
            self.ids.digits_only
        ]
        self.key = key
        self.data_loaded = False

    def update_entry(self, instance, value):
        if not self.data_loaded:
            self.data_manager.load_data(self.key)
            self.data_loaded = True
        domain = value

        if domain in self.data_manager.username_dict:
            username = self.data_manager.username_dict[domain]
            self.ids.username.text = username

            if domain in self.data_manager.length_dict:
                length = self.data_manager.length_dict[domain]
                self.ids.password_length.text = str(length)

            if domain in self.data_manager.checkbox_dict:
                checkbox_states = self.data_manager.checkbox_dict[domain]
                for i in range(len(checkbox_states)):
                    self.checkbox_list[i].active = checkbox_states[i]
        else:
            self.ids.username.text = ""
            self.ids.password_length.text = ""
            for checkbox_state in self.checkbox_list:
                checkbox_state.active = True

    def generate_new_salt(self):
        domain = self.ids.domain.text
        if not domain:
            self.show_popup("Error", "Please enter a domain.")
            return

        if domain not in self.data_manager.salt_dict:
            self.show_popup("Error", "Password never been created")
            return

        new_salt = token_hex(64)
        self.data_manager.salt_dict[domain] = new_salt
        self.show_popup(
            "New Password", "A new password has been generated for this domain.")

    def generate_password(self):
        master_password = self.key
        domain = self.ids.domain.text
        username = self.ids.username.text
        length = self.ids.password_length.text
        if not master_password:
            self.show_popup("Error", "Please enter the Master Password.")
            return

        if domain == "" or username == "" or length == "":
            self.show_popup("Error", "Please fill in all the fields.")
            return

        try:
            length = int(length)
        except ValueError:
            self.show_popup("Error", "The password length must be an integer.")
            return

        if length <= 0:
            self.show_popup(
                "Error", "The password length must be greater than zero.")
            return

        self.data_manager.username_dict[domain] = username
        self.data_manager.length_dict[domain] = length

        checkbox_states = [
            checkbox.active for checkbox in self.checkbox_list]
        self.data_manager.checkbox_dict[domain] = checkbox_states

        if domain in self.data_manager.salt_dict:
            salt = self.data_manager.salt_dict[domain]
        else:
            salt = token_hex(64)
            self.data_manager.salt_dict[domain] = salt

        password = PasswordGenerator(
            master_password, username, domain, length, salt).generate(*checkbox_states)
        Clipboard.copy(password)
        self.show_popup("Password Copied", "The password has been copied!")
        self.data_manager.save_data(master_password)

    def show_popup(self, title, message):
        text = Label(text=message, halign='center', valign='middle', text_size=(
            Window.width * 0.8, None))
        popup = Popup(title=title, content=text, size_hint=(0.9, 0.25))
        popup.open()
