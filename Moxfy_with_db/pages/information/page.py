from flet import *
from helper.appbar import appBarGeneralView, highlight, unhighlight
from pages.information.info import UserInfo
from db.config import collection
from pages.auth.register.page import Register


class Information(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Information")

        self.username = TextField(
            label="Username",
            read_only=True,
            border_color="#BDB5D5",
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            value=f"{UserInfo.user}",
            icon=icons.EMOJI_EMOTIONS,
        )

        self.passw0rd = TextField(
            label="Password",
            read_only=True,
            border_color="#BDB5D5",
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            password=True,
            can_reveal_password=True,
            value=f"{UserInfo.pwd}",
            icon=icons.EMOJI_EMOTIONS,
        )

        self.content = Column(
            [
                self.username,
                self.passw0rd,
            ],
            height=525,
            width=900,
        )

        self.current_password = TextField(
            hint_text="Current Password",
            border_color="#BDB5D5",
            password=True,
            can_reveal_password=True,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
        )

        self.new_password = TextField(
            hint_text="New Password",
            border_color="#BDB5D5",
            password=True,
            can_reveal_password=True,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
        )

        self.column_password = Container(
            width=400,
            height=100,
            content=Column(
                [
                    self.current_password,
                    self.new_password,
                ],
            ),
        )

        self.change_password = Text(
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "Update Password",
                    TextStyle(decoration=TextDecoration.UNDERLINE),
                    on_click=self.open_dlg,
                ),
            ],
        )

        if UserInfo.service == "MongoDB":
            self.content.controls.append(self.change_password)
            self.update()

        self._container = Container(
            self.content,
            expand=True,
            margin=10,
            padding=10,
            alignment=alignment.top_center,
        )

        self.information = Row([self._container], expand=True)

        self.title_update_password = Text("Update Password")

        self.confirm_in_dialog = Text(
            size=15,
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "Confirm",
                    TextStyle(decoration=TextDecoration.NONE),
                    on_click=lambda e: self.UpdatePassword(
                        UserInfo.user,
                        self.current_password.value,
                        self.new_password.value,
                    ),
                    on_enter=highlight,
                    on_exit=unhighlight,
                ),
            ],
        )

        self.exit_in_dialog = Text(
            size=15,
            font_family="poppins",
            weight="w400",
            disabled=False,
            spans=[
                TextSpan(
                    "Exit",
                    TextStyle(decoration=TextDecoration.NONE),
                    on_click=self.close_dlg,
                    on_enter=highlight,
                    on_exit=unhighlight,
                ),
            ],
        )

        self.dialog = AlertDialog(
            shape=None,
            modal=True,
            title=self.title_update_password,
            content=self.column_password,
            actions=[
                self.confirm_in_dialog,
                self.exit_in_dialog,
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def close_dlg(self, e):
        self.dialog.open = False
        self.page.update()

    def open_dlg(self, e):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def UpdatePassword(self, username, current_password, new_password):
        if (
            not self.current_password.value
            or not self.current_password.value.strip()
            or not self.new_password.value
            or not self.new_password.value.strip()
        ):
            return
        if current_password != UserInfo.pwd:
            self.page.show_snack_bar(
                SnackBar(
                    Text("Password doesn't match."),
                    open=True,
                )
            )
            return
        user = collection.find_one({"username": username})
        if user:
            encoded_salt, encoded_hashed_password = Register.hash_password(
                self, new_password
            )
            collection.update_one(
                {"username": username},
                {"$set": {"salt": encoded_salt, "password": encoded_hashed_password}},
            )
            self.page.show_snack_bar(
                SnackBar(
                    Text(
                        "Password updated successfully. Let's login with the new password!"
                    ),
                    open=True,
                )
            )
            self.page.go("/login")
            return
        else:
            self.page.show_snack_bar(
                SnackBar(
                    Text("User not found. Unable to update password."),
                    open=True,
                )
            )
            return

    def build(self):
        return self.information
