from flet import *
from helper.appbar import appbarLoginView, highlight, unhighlight
from db.config import collection
from pages.information.info import UserInfo
import hashlib
import base64


class Login(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appbarLoginView("Login", "/about", page, "About")

        self.field_username = TextField(
            height=40,
            width=246,
            hint_text="Username",
            border_color="#BDB5D5",
            border_radius=5,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
        )

        self.field_passw0rd = TextField(
            height=40,
            width=246,
            hint_text="Password",
            border_color="#BDB5D5",
            password=True,
            can_reveal_password=True,
            border_radius=5,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
        )

        self.login_button = Container(
            content=ElevatedButton(
                content=Text(
                    "Log In",
                    size=13,
                ),
                on_click=self.l0gin,
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=10),
                    },
                    color={
                        "": "white",
                    },
                    bgcolor={"": "blue"},
                ),
                height=40,
                width=220,
            ),
        )

        self.moxfy = Text(
            "Moxfy",
            size=20,
            font_family="poppins",
            weight="w400",
        )

        self.moxfy_describe = Text(
            "The Ultimate PDF Toolkit",
            size=20,
            font_family="poppins",
            weight="w400",
        )

        self.ask_for_register = Text(
            size=13,
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "✨ Creat a free Moxfy Account",
                    TextStyle(decoration=TextDecoration.NONE),
                    on_enter=highlight,
                    on_exit=unhighlight,
                    on_click=lambda e: self.page.go("/register"),
                ),
            ],
        )

        self.ask_for_join_discord = Text(
            size=13,
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "🚀 Join our Discord and connect with others",
                    TextStyle(decoration=TextDecoration.NONE),
                    url="https://discord.gg/6HaR7ptR8Y",
                    on_enter=highlight,
                    on_exit=unhighlight,
                ),
            ],
        )

        self.image_logo = Image(
            src=f"/images/moxfy.png",
            width=155,
            height=155,
            fit=ImageFit.CONTAIN,
            repeat=ImageRepeat.NO_REPEAT,
        )

    def verify_password(self, password, salt, hashed_password):
        salt = base64.b64decode(salt)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        encoded_dk = base64.b64encode(dk).decode("utf-8")[:24]
        return encoded_dk == hashed_password

    def l0gin(self, e):
        if (
            not self.field_username.value
            or not self.field_username.value.strip()
            or not self.field_passw0rd.value
            or not self.field_passw0rd.value.strip()
        ):
            return
        self.doL0gin(self.field_username.value, self.field_passw0rd.value)

    def doL0gin(self, username, password):
        user = collection.find_one({"username": username})
        if user:
            if self.verify_password(password, user["salt"], user["password"]):
                UserInfo.user = username
                UserInfo.pwd = password
                UserInfo.service = "MongoDB"
                self.page.go("/main")
            else:
                self.page.show_snack_bar(
                    SnackBar(Text("Invalid credentials. Please try again."), open=True)
                )
        else:
            self.page.show_snack_bar(
                SnackBar(Text("Can't find the user. Please try again."), open=True)
            )
            return

    def build(self):
        return Container(
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Divider(height=10, color="transparent"),
                                self.image_logo,
                                Divider(height=1, color="transparent"),
                                self.moxfy,
                                self.moxfy_describe,
                                Divider(height=1, color="transparent"),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        self.field_username,
                                        self.field_passw0rd,
                                    ],
                                ),
                                Divider(height=1, color="transparent"),
                                self.login_button,
                                Divider(height=5, color="transparent"),
                                self.ask_for_register,
                                self.ask_for_join_discord,
                            ],
                        ),
                    ),
                ],
            ),
        )
