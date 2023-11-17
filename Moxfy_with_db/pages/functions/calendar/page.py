from flet import *
from helper.appbar import appBarGeneralView
from core.methods import doCreateCalendar
import helper.pathhandle as upath


class Calendar(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Calendar")

        self.title_lt = Text("Specify The Year For Calendar Creation")

        """Calendar"""
        self.field_year = TextField(
            hint_text="Starting Year (Example: 2023)",
            height=40,
            width=250,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )
        self.field_toyear = TextField(
            hint_text="Ending Year (Example: 1)",
            height=40,
            width=250,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )
        self.creat_calendar = OutlinedButton(
            "Creat",
            icon="CALENDAR_MONTH",
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
            on_click=self.start_make_calendar,
        )

    def start_make_calendar(self, e):
        try:
            int_yearNum = int(self.field_year.value)
            int_toyearNum = int(self.field_toyear.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid year number or missing."), open=True)
            )
            return
        try:
            doCreateCalendar(int_yearNum, int_toyearNum, upath.CALENDAR_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Successfully Created."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def build(self):
        return Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Container(
                                width=self.page.width,
                                height=self.page.height,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        ListTile(
                                            leading=Icon(icons.INFO),
                                            title=self.title_lt,
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                self.field_year,
                                                self.field_toyear,
                                            ],
                                        ),
                                        self.creat_calendar,
                                    ],
                                ),
                            )
                        ],
                    ),
                ],
            ),
        )
