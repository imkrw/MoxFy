from flet import *
from routing.views import Router
import string
import random


def randstr(length):
    characters = string.ascii_lowercase
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def main(page: Page):
    page.title = randstr(10)
    page.window_width = 950
    page.window_height = 725
    page.window_maximizable = False
    page.window_resizable = False
    page.window_center()
    page.fonts = {"poppins": f"/font/Poppins-Regular.ttf"}
    page.theme = Theme(use_material3=True, font_family="poppins")
    page.theme_mode = "dark"

    router = Router(page)
    page.on_route_change = router.route_change
    router.initial_view()
    page.add(router.cstate)

if __name__ == "__main__":
    app(target=main, view=FLET_APP, assets_dir="assets")
