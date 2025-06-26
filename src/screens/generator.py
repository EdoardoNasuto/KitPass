from secrets import token_hex

import flet as ft

from routes import Routes
from utils.password import PasswordGenerator
from utils.data_manager import DataManager


class GeneratorScreen():
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.key = page.session.get("key")
        self.data_manager = DataManager()
        self.data_loaded = False

    def build(self):
        self.domain = ft.Ref[ft.TextField]()
        self.username = ft.Ref[ft.TextField]()
        self.password_length = ft.Ref[ft.TextField]()
        self.excluded_characters = ft.Ref[ft.TextField]()

        # Using Checkboxes
        self.special_character = ft.Ref[ft.Checkbox]()
        self.remove_digits = ft.Ref[ft.Checkbox]()
        self.remove_uppercase = ft.Ref[ft.Checkbox]()
        self.digits_only = ft.Ref[ft.Checkbox]()

        self.checkbox_list = [
            self.special_character,
            self.remove_digits,
            self.remove_uppercase,
            self.digits_only
        ]

        self.snack_bar = ft.Ref[ft.SnackBar]()
        self.snack_bar_text = ft.Ref[ft.Text]()

        return ft.View(
            route=Routes.LOGIN.value,
            spacing=10,
            padding=20,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[
                ft.TextField(ref=self.domain, label="Domain",
                             on_change=self.update_entry, icon=ft.Icons.LANGUAGE),
                ft.TextField(ref=self.username, label="Username",
                             icon=ft.Icons.PERSON),
                ft.TextField(ref=self.password_length,
                             label="Password Length", icon=ft.Icons.NUMBERS),
                ft.TextField(ref=self.excluded_characters,
                             label="Excluded Characters", icon=ft.Icons.CANCEL),

                ft.Checkbox(ref=self.special_character,
                            label="Special Characters", value=True),
                ft.Checkbox(ref=self.remove_digits,
                            label="Remove Digits", value=True),
                ft.Checkbox(ref=self.remove_uppercase,
                            label="Uppercases", value=True),
                ft.Checkbox(ref=self.digits_only,
                            label="Digits Only", value=False),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.ElevatedButton(
                            "Generate Password", on_click=lambda e: self.generate_password()),
                        ft.ElevatedButton(
                            "Change Password", on_click=lambda e: self.generate_new_salt())
                    ]),

                ft.SnackBar(ref=self.snack_bar, content=ft.Text(
                    ref=self.snack_bar_text, value="")),
            ],
        )

    def update_entry(self, e):
        if not self.data_loaded:
            self.data_manager.load_data(self.key)
            self.data_loaded = True
        domain = self.domain.current.value

        if domain in self.data_manager.username_dict:
            self.username.current.value = self.data_manager.username_dict[domain]
            self.password_length.current.value = str(
                self.data_manager.length_dict.get(domain, ""))

            checkbox_states = self.data_manager.checkbox_dict.get(domain, [
                                                                  True]*4)
            for i, checkbox in enumerate(self.checkbox_list):
                checkbox.current.value = checkbox_states[i]
        else:
            self.username.current.value = ""
            self.password_length.current.value = ""
            for checkbox in self.checkbox_list:
                checkbox.current.value = True

        self.page.update()

    def generate_new_salt(self):
        domain = self.domain.current.value
        if not domain:
            self.show_snackbar("Please enter a domain.")
            return

        if domain not in self.data_manager.salt_dict:
            self.show_snackbar("Password never been created")
            return

        new_salt = token_hex(64)
        self.data_manager.salt_dict[domain] = new_salt
        self.show_snackbar(
            "A new password has been generated for this domain.")

    def generate_password(self):
        master_password = self.key
        domain = self.domain.current.value
        username = self.username.current.value
        length = self.password_length.current.value
        excluded_characters = self.excluded_characters.current.value

        if not master_password:
            self.show_snackbar("Please enter the Master Password.")
            return

        if domain == "" or username == "" or length == "":
            self.show_snackbar("Please fill in all the fields.")
            return

        try:
            length = int(length)
        except ValueError:
            self.show_snackbar("The password length must be an integer.")
            return

        if length <= 0:
            self.show_snackbar(
                "The password length must be greater than zero.")
            return

        self.data_manager.username_dict[domain] = username
        self.data_manager.length_dict[domain] = length

        checkbox_states = [cb.current.value for cb in self.checkbox_list]
        self.data_manager.checkbox_dict[domain] = checkbox_states

        # Generate salt if not existing
        salt = self.data_manager.salt_dict.get(domain, token_hex(64))
        self.data_manager.salt_dict[domain] = salt

        password = PasswordGenerator(master_password, username, domain, length, salt).generate(
            *checkbox_states, excluded_characters)

        self.page.set_clipboard(password)
        self.show_snackbar("The password has been copied!")
        self.data_manager.save_data(master_password)

    def show_snackbar(self, message):
        self.snack_bar_text.current.value = message
        self.snack_bar.current.open = True
        self.page.update()
