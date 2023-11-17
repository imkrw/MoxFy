from flet import *
from helper.appbar import appBarGeneralView


class Authors(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        
        self.page.appbar = appBarGeneralView("/about", page, "Authors")

    def build(self):
        return Container(
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Divider(height=10, color="transparent"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=740,
                                height=100,
                                border=border.all(2, "#BDB5D5"),
                                border_radius=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Divider(height=10, color="transparent"),
                                        Text(
                                            "Dr. Warattapop Thapatsuwan",
                                            size=21,
                                            weight="bold",
                                        ),
                                        Text(
                                            "(The Project Consultant)",
                                            size=13,
                                            weight="w400",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=365,
                                height=365,
                                border=border.all(2, "#BDB5D5"),
                                border_radius=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Divider(height=20, color="transparent"),
                                        Text(
                                            "Korrawit Yudying",
                                            size=21,
                                            weight="bold",
                                        ),
                                        Text(
                                            "(Author)",
                                            size=13,
                                            weight="w400",
                                        ),
                                        Image(
                                            src=f"/images/author1.jpg",
                                            width=200,
                                            height=200,
                                            fit=ImageFit.CONTAIN,
                                            repeat=ImageRepeat.NO_REPEAT,
                                            border_radius=border_radius.all(20),
                                        ),
                                        Text(
                                            "Coding and Design",
                                            size=13,
                                            weight="w400",
                                        ),
                                    ],
                                ),
                            ),
                            Container(
                                width=365,
                                height=365,
                                border=border.all(2, "#BDB5D5"),
                                border_radius=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Divider(height=20, color="transparent"),
                                        Text(
                                            "Tangmo Chotika",
                                            size=21,
                                            weight="bold",
                                        ),
                                        Text(
                                            "(Author)",
                                            size=13,
                                            weight="w400",
                                        ),
                                        Image(
                                            src=f"/images/author2.jpg",
                                            width=200,
                                            height=200,
                                            fit=ImageFit.CONTAIN,
                                            repeat=ImageRepeat.NO_REPEAT,
                                            border_radius=border_radius.all(20),
                                        ),
                                        Text(
                                            "Coding and Design",
                                            size=13,
                                            weight="w400",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=740,
                                height=75,
                                border=border.all(2, "#BDB5D5"),
                                border_radius=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Divider(height=10, color="transparent"),
                                        Text(
                                            ">>> 🤍 <<<",
                                            size=21,
                                            weight="bold",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )
