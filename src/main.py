import platform

import flet as ft

from routes import Routes
from screens.login import LoginScreen
from screens.generator import GeneratorScreen


def main(page: ft.Page):
    page.title = "Kitpass"
    page.theme_mode = "Dark"

    if platform.system() == 'Windows':
        page.window.height = page.window.height * 0.9
        page.window.width = page.window.width * 0.3

    if platform.system() == 'Android':
        from android.permissions import request_permissions, Permission

        request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                            Permission.READ_EXTERNAL_STORAGE])

    def route_change(route):
        page.views.clear()

        page.views.append(LoginScreen(page).build())

        if page.route == Routes.GENERATOR.value:
            page.views.append(GeneratorScreen(page).build())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)
