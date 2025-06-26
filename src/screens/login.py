import re
import hashlib

import flet as ft

from routes import Routes
from utils.data_manager import DataManager


class LoginScreen():
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.data_manager = DataManager()

    def build(self):
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        self.page.overlay.append(self.file_picker)

        self.master_password = ft.Ref[ft.TextField]()

        self.snack_bar = ft.Ref[ft.SnackBar]()
        self.snack_bar_text = ft.Ref[ft.Text]()

        return ft.View(
            route=Routes.LOGIN.value,
            spacing=10,
            padding=20,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.ElevatedButton(
                            text="Import data", on_click=lambda _: self.import_data(), width=150
                        ),
                        ft.ElevatedButton(
                            text="Export data", on_click=lambda _: self.export_data(), width=150
                        )
                    ],
                ),
                ft.TextField(
                    ref=self.master_password,
                    label="Master Password",
                    password=True,
                    icon=ft.Icons.KEY,
                ),
                ft.ElevatedButton(
                    text="Validate Password", on_click=lambda _: self.password_validate()
                ),
                ft.ElevatedButton(
                    text="Reset Data", on_click=lambda _: self.reset_data()
                ),

                ft.SnackBar(ref=self.snack_bar, content=ft.Text(
                    ref=self.snack_bar_text, value="")),
            ],
        )

    def password_validate(self):
        master_password = self.master_password.current.value
        valid = True

        if len(master_password) < 8:
            valid = False
            self.show_snackbar(
                "Master password must be at least 8 characters long.")

        if valid == True and not re.match(r"^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*\d)(?=.*[A-Z])", master_password):
            valid = False
            self.show_snackbar(
                "Master password must contain at least one special character, one digit, and one uppercase letter.")

        if valid == True:
            key = hashlib.pbkdf2_hmac(
                "sha256", master_password.encode("utf-8"), b"", 100000)
            del (master_password)
            if self.data_manager.load_data(key) is None:
                valid = False
                self.show_snackbar("Failed to validate the master password.")
            else:
                self.page.go(Routes.GENERATOR.value)
                self.page.session.set("key", key)

    def show_snackbar(self, message):
        self.snack_bar_text.current.value = message
        self.snack_bar.current.open = True
        self.page.update()

    def import_data(self):
        self.importing = True
        self.file_picker.pick_files(allowed_extensions=["json"])

    def export_data(self):
        master_password = self.master_password.current.value
        key = hashlib.pbkdf2_hmac(
            "sha256", master_password.encode("utf-8"), b"", 100000)
        del (master_password)
        if self.data_manager.load_data(key) is None:
            self.show_snackbar("Failed to validate the master password.")
        else:
            self.importing = False
            self.file_picker.get_directory_path()

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        if self.importing:
            if e.files and e.files[0].name.endswith(".json"):
                self.data_manager.import_data(e.files[0].path)
                self.show_snackbar("Import successful.")
        else:
            if e.path:
                self.data_manager.export_data("data.json", e.path)
                self.show_snackbar("Export successful.")

    def reset_data(self):
        master_password = self.master_password.value
        key = hashlib.pbkdf2_hmac(
            "sha256", master_password.encode("utf-8"), b"", 100000)
        del (master_password)
        if self.data_manager.load_data(key) is None:
            self.show_snackbar("Failed to validate the master password.")
        else:
            self.data_manager.reset_data("data.json")
            self.show_snackbar("Reset data successful.")
