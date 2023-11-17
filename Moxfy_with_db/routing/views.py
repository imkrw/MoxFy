from pages.main.page import MainView
from pages.functions.split.page import Split
from pages.functions.encrypt.page import Encrypt
from pages.functions.decrypt.page import Decrypt
from pages.functions.merge.page import Merge
from pages.functions.watermark.page import Watermark
from pages.functions.convert.page import Convert
from pages.functions.manage.page import Manage
from pages.utils.page import Utils
from pages.permissions.page import SetPermissions
from pages.functions.rotate.page import R0tate
from pages.functions.compress.page import Compress
from pages.functions.calendar.page import Calendar
from pages.about.page import About
from pages.auth.login.page import Login
from pages.auth.register.page import Register
from pages.report.page import Report
from pages.information.page import Information
from pages.authors.page import Authors
from flet import *


class Router:
    def __init__(self, page: Page):
        self.page = page
        self.routes = {
            "/login": Login,
            "/register": Register,
            "/about": About,
            "/main": MainView,
            "/encrypt": Encrypt,
            "/decrypt": Decrypt,
            "/rotate": R0tate,
            "/split": Split,
            "/merge": Merge,
            "/compress": Compress,
            "/calendar": Calendar,
            "/convert": Convert,
            "/managements": Manage,
            "/watermark": Watermark,
            "/utils": Utils,
            "/setpermissions": SetPermissions,
            "/report": Report,
            "/information": Information,
            "/authors": Authors,
        }
        self.cstate = None

    def initial_view(self):
        self.cstate = Container(content=self.routes["/login"](self.page))

    def route_change(self, route):
        self.cstate.content = self.routes[route.route](self.page)
        self.cstate.update()
