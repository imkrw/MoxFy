from flet import *
from helper.appbar import appBarGeneralView
from pages.information.info import UserInfo
from dotenv import load_dotenv
import requests
import json
import os


load_dotenv()

WEBHOOK = os.getenv("WEBHOOK")

def send_discord_message(content):
    if UserInfo.service == "MongoDB":
        username = UserInfo.user
    webhook = WEBHOOK
    message = {"content": f"Username: {username}\nReport: " + content}
    json_message = json.dumps(message)
    response = requests.post(webhook, data=json_message, headers={"Content-Type": "application/json"})
    if response.status_code == 204:
        return True
    else:
        return False


class Report(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Report")

        self.title_text = Text("Having an issue?", size=20)
        self.title_report = Text(
            "Write a bug you found here and keep up with updates on Discord.",
            size=18,
            weight="w400",
        )
        self.textfield_report = TextField(
            multiline=True,
            hint_text="Write something here...",
            value="",
            width=500,
            border_color="#BDB5D5",
            max_lines=5,
            expand=True,
            border_radius=10,
            min_lines=5,
            max_length=1024,
            keyboard_type=KeyboardType.TEXT,
        )
        self.send_report_button = IconButton(
            icon=icons.SEND_ROUNDED,
            icon_color="blue400",
            icon_size=40,
            on_click=self.send,
        )
        self.warn_message = ElevatedButton(
            "Sending messages to disturb may lead to a ban.",
            icon="WARNING",
            icon_color="amber400",
            disabled=True,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )

    def send(self, e):
        if not self.textfield_report.value.strip() or not self.textfield_report.value:
            return
        if send_discord_message(self.textfield_report.value):
            e.page.show_snack_bar(
                SnackBar(
                    Text(
                        "Your report has been sent to the developers. Thank you for your help!"
                    ),
                    open=True,
                )
            )
            return
        else:
            e.page.show_snack_bar(
                SnackBar(
                    Text("Your report could not be sent. Please try again later."),
                    open=True,
                )
            )
            return

    def build(self):
        return Container(
            content=Column(
                [
                    Row(alignment=MainAxisAlignment.CENTER, controls=[self.title_text]),
                    Row(
                        alignment=MainAxisAlignment.CENTER, controls=[self.title_report]
                    ),
                    Divider(height=10, color="transparent"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.textfield_report],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.send_report_button],
                    ),
                    Divider(height=10, color="transparent"),
                    Row(
                        alignment=MainAxisAlignment.CENTER, controls=[self.warn_message]
                    ),
                ],
            ),
        )
