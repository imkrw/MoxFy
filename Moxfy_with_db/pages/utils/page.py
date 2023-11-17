from flet import *
from helper.appbar import appBarGeneralView
import random
import string
import helper.jsonhandle as ujson
import helper.pathhandle as upath


def generate_password(
    upper_case=True, lower_case=True, numbers=True, symbols=True, length=8
):
    chars = ""
    if upper_case:
        chars += string.ascii_uppercase
    if lower_case:
        chars += string.ascii_lowercase
    if numbers:
        chars += string.digits
    if symbols:
        chars += string.punctuation
    if not chars:
        chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


class Utils(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Utilities")

        """Encrypt"""
        self.title_encrypt = Text("Encrypt Setting", size=20)
        self.save_encrypt_button = Container(
            content=ElevatedButton(
                content=Text(
                    "Save",
                    size=13,
                ),
                on_click=self.encrypt_save,
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8),
                    },
                    color={
                        "": "white",
                    },
                    bgcolor={"": "blue"},
                ),
                height=40,
                width=125,
            ),
        )
        self.textfield_encrypt_user_password = TextField(
            width=350,
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            text_align="left",
            border_color="#BDB5D5",
            value=ujson.load_value(
                upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_user_password"
            ),
            label="User Password",
        )
        self.textfield_encrypt_owner_password = TextField(
            width=350,
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            text_align="left",
            border_color="#BDB5D5",
            value=ujson.load_value(
                upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_owner_password"
            ),
            label="Owner Password",
        )

        """Decrypt"""
        self.title_decrypt = Text("Decrypt Setting", size=20)
        self.save_decrypt_button = Container(
            content=ElevatedButton(
                content=Text(
                    "Save",
                    size=13,
                ),
                on_click=self.decrypt_save,
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8),
                    },
                    color={
                        "": "white",
                    },
                    bgcolor={"": "blue"},
                ),
                height=40,
                width=125,
            ),
        )
        self.delete_encrypt_button = OutlinedButton(
            "Delete",
            on_click=self.encrypt_remove,
            icon=icons.DELETE,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.delete_decrypt_button = OutlinedButton(
            "Delete",
            on_click=self.decrypt_remove,
            icon=icons.DELETE,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.textfield_decrypt_password = TextField(
            width=350,
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            text_align="left",
            border_color="#BDB5D5",
            value=ujson.load_value(
                upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "decrypt_password"
            ),
            label="Owner or User Password",
        )

        """Generate Password"""
        self.title_generate = Text("Generate Password", size=20)
        self.generate_button = Container(
            content=ElevatedButton(
                content=Text(
                    "Generate",
                    size=13,
                ),
                on_click=self.d0generate,
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8),
                    },
                    color={
                        "": "white",
                    },
                    bgcolor={"": "blue"},
                ),
                height=40,
                width=125,
            ),
        )
        self.copy_button = OutlinedButton(
            "Copy",
            icon=icons.COPY,
            on_click=self.c0py,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.textfield_generate = TextField(
            width=350,
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            read_only=True,
            text_align="left",
            border_color="#BDB5D5",
            hint_text="The Password Will Be Generated Here",
        )

        """Checkboxes for custom type of the password [generate password]"""
        self.upper_case = Checkbox(
            label="\tUppercase",
            on_change=self.d0generate,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.lower_case = Checkbox(
            label="\tLowercase",
            on_change=self.d0generate,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.numbers = Checkbox(
            label="\tNumbers",
            on_change=self.d0generate,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.symbols = Checkbox(
            label="\tSymbols",
            on_change=self.d0generate,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )

        """Slider for custom length of the password [generate password]"""
        self.length_slider = Slider(
            value=8,
            min=8,
            max=128,
            divisions=121,
            height=15,
            width=750,
            thumb_color=colors.BLUE,
            label="Password Length: {value}",
            on_change=self.d0generate,
        )

        self.ask_for_permissions = Text(
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "Permissions",
                    TextStyle(decoration=TextDecoration.UNDERLINE),
                    on_click=lambda e: self.page.go("/setpermissions"),
                ),
            ],
        )

    def d0generate(self, e):
        uppercase = self.upper_case.value
        lowercase = self.lower_case.value
        numbers = self.numbers.value
        symbols = self.symbols.value
        password_length = int(self.length_slider.value)

        key = generate_password(uppercase, lowercase, numbers, symbols, password_length)
        self.textfield_generate.value = key
        self.textfield_generate.update()

    def c0py(self, e):
        if (
            not self.textfield_generate.value
            or not self.textfield_generate.value.strip()
        ):
            return
        e.page.set_clipboard(f"{self.textfield_generate.value}")
        e.page.show_snack_bar(
            SnackBar(Text(f"Copied: {self.textfield_generate.value}"), open=True)
        )

    def encrypt_save(self, e):
        if (
            not self.textfield_encrypt_owner_password.value.strip()
            or not self.textfield_encrypt_owner_password.value
            or not self.textfield_encrypt_user_password.value.strip()
            or not self.textfield_encrypt_user_password.value
        ):
            return
        else:
            try:
                ujson.save_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "encrypt_owner_password",
                    self.textfield_encrypt_owner_password.value,
                )
                ujson.save_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "encrypt_user_password",
                    self.textfield_encrypt_user_password.value,
                )
                e.page.show_snack_bar(SnackBar(Text(f"Done!"), open=True))
            except Exception as ex:
                e.page.show_snack_bar(
                    SnackBar(Text("An error occurred: {}".format(ex)), open=True)
                )
                return

    def encrypt_remove(self, e):
        try:
            ujson.delete_value(
                upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_owner_password"
            )
            ujson.delete_value(
                upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_user_password"
            )
            self.textfield_encrypt_owner_password.value = None
            self.textfield_encrypt_user_password.value = None
            self.textfield_encrypt_owner_password.update()
            self.textfield_encrypt_user_password.update()
        except Exception as ex:
            e.page.show_snack_bar(
                SnackBar(Text("An error occurred: {}".format(ex)), open=True)
            )
            return

    def decrypt_save(self, e):
        if (
            not self.textfield_decrypt_password.value.strip()
            or not self.textfield_decrypt_password.value
        ):
            return
        else:
            try:
                ujson.save_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "decrypt_password",
                    self.textfield_decrypt_password.value,
                )
                e.page.show_snack_bar(SnackBar(Text(f"Done!"), open=True))
            except Exception as ex:
                e.page.show_snack_bar(
                    SnackBar(Text("An error occurred: {}".format(ex)), open=True)
                )
                return

    def decrypt_remove(self, e):
        try:
            ujson.delete_value(
                upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "decrypt_password"
            )
            self.textfield_decrypt_password.value = None
            self.textfield_decrypt_password.update()
        except Exception as ex:
            e.page.show_snack_bar(
                SnackBar(Text("An error occurred: {}".format(ex)), open=True)
            )
            return

    def build(self):
        return Container(
            content=Column(
                [
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.title_generate],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.textfield_generate],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.length_slider],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.upper_case,
                            self.lower_case,
                            self.numbers,
                            self.symbols,
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.generate_button, self.copy_button],
                    ),
                    Divider(height=1, color="transparent"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.title_encrypt],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.textfield_encrypt_owner_password,
                            self.textfield_encrypt_user_password,
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.save_encrypt_button, self.delete_encrypt_button],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.ask_for_permissions],
                    ),
                    Divider(height=1, color="transparent"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.title_decrypt],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.textfield_decrypt_password],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.save_decrypt_button, self.delete_decrypt_button],
                    ),
                ],
            ),
        )
