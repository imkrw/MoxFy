from flet import *
from helper.appbar import appBarGeneralView
from db.config import collection
import hashlib
import base64
import os


class Register(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/login", page, "Register")

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

        self.register_button = Container(
            content=ElevatedButton(
                content=Text(
                    "Register",
                    size=13,
                ),
                on_click=self.on_register,
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

        self.ask_for_help = Text(
            size=13,
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "Are you having a trouble? ",
                    TextStyle(decoration=TextDecoration.NONE),
                ),
                TextSpan(
                    "Get your issues resolved.",
                    TextStyle(
                        decoration=TextDecoration.NONE, weight="w400", color="blue"
                    ),
                    url="https://discord.gg/6HaR7ptR8Y",
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

    def hash_password(self, password):
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        encoded_salt = base64.b64encode(salt).decode("utf-8")[:24]
        encoded_hashed_password = base64.b64encode(dk).decode("utf-8")[:24]
        return encoded_salt, encoded_hashed_password

    def on_register(self, e):
        if (
            not self.field_username.value
            or not self.field_username.value.strip()
            or not self.field_passw0rd.value
            or not self.field_passw0rd.value.strip()
        ):
            return
        if 8 <= len(self.field_username.value) <= 12:
            self.DoRegister(self.field_username.value, self.field_passw0rd.value)
        else:
            self.page.show_snack_bar(
                SnackBar(
                    Text("Username must be between 8 and 12 characters."),
                    open=True,
                )
            )
            return

    def DoRegister(self, username, password):
        encoded_salt, encoded_hashed_password = self.hash_password(password)
        user = collection.find_one({"username": username})
        if user:
            self.page.show_snack_bar(
                SnackBar(
                    Text("Username already exists. Please choose a different one."),
                    open=True,
                )
            )
            return
        else:
            collection.insert_one(
                {
                    "username": username,
                    "salt": encoded_salt,
                    "password": encoded_hashed_password,
                }
            )
            self.page.show_snack_bar(
                SnackBar(Text("Registration successful."), open=True)
            )
            return

    def build(self):
        return Container(
            alignment=alignment.center,
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
                                self.register_button,
                                Divider(height=5, color="transparent"),
                                self.ask_for_help,
                            ],
                        ),
                    ),
                ],
            ),
        )
