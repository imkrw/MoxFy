from flet import *
from helper.appbar import appBarMainView


class MainView(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarMainView(page)

        def _container(message, ic, hover, destination):
            return Container(
                content=Row(
                    [
                        Text(message, size=14),
                        CircleAvatar(
                            content=ic,
                        ),
                    ],
                    alignment="spaceBetween",
                ),
                margin=10,
                padding=10,
                on_hover=hover,
                scale=Scale(scale=1),
                animate_scale=animation.Animation(50, "bounceOut"),
                width=190,
                height=70,
                border_radius=10,
                on_click=lambda _: self.page.go(f"{destination}"),
                border=border.all(2, color="#BDB5D5"),
            )

        self.container_encrypt = _container(
            "Encrypt",
            Icon(icons.ENHANCED_ENCRYPTION),
            lambda e: self.Hover_Encrypt(e),
            "/encrypt",
        )

        self.container_decrypt = _container(
            "Decrypt",
            Icon(icons.NO_ENCRYPTION),
            lambda e: self.Hover_Decrypt(e),
            "/decrypt",
        )

        self.container_rotate = _container(
            "Rotate",
            Icon(icons.ROTATE_LEFT),
            lambda e: self.Hover_Rotate(e),
            "/rotate",
        )

        self.container_split = _container(
            "Split",
            Icon(icons.CALL_SPLIT),
            lambda e: self.Hover_Split(e),
            "/split",
        )

        self.container_convert = _container(
            "Convert",
            Icon(icons.SWAP_VERT),
            lambda e: self.Hover_Convert(e),
            "/convert",
        )

        self.container_merge = _container(
            "Merge",
            Icon(icons.CALL_MERGE),
            lambda e: self.Hover_Merge(e),
            "/merge",
        )

        self.container_compress = _container(
            "Compress",
            Icon(icons.COMPRESS),
            lambda e: self.Hover_Compress(e),
            "/compress",
        )

        self.container_calendar = _container(
            "Calendar",
            Icon(icons.CALENDAR_MONTH),
            lambda e: self.Hover_Calendar(e),
            "/calendar",
        )

        self.container_management = _container(
            "Management",
            Icon(icons.EDIT),
            lambda e: self.Hover_Management(e),
            "/managements",
        )

        self.container_watermark = _container(
            "Watermark",
            Icon(icons.WATER_DROP),
            lambda e: self.Hover_Watermark(e),
            "/watermark",
        )

        self.moxfy_describe = Container(
            content=Text(
                "The Ultimate PDF ToolKit",
            ),
            height=45,
            width=410,
            alignment=alignment.center,
            border_radius=10,
            border=border.all(2, color="#BDB5D5"),
        )

    def Animated_Hover(self, container, e):
        if e.data == "true":
            container.border = border.only(
                left=border.BorderSide(2, "BLUE500"),
                right=border.BorderSide(2, "BLUE500"),
                top=border.BorderSide(2, "BLUE500"),
                bottom=border.BorderSide(2, "BLUE500"),
            )
        else:
            container.border = border.all(2, color="#BDB5D5")
        container.update()

    def Hover_Encrypt(self, e):
        self.Animated_Hover(self.container_encrypt, e)

    def Hover_Decrypt(self, e):
        self.Animated_Hover(self.container_decrypt, e)

    def Hover_Rotate(self, e):
        self.Animated_Hover(self.container_rotate, e)

    def Hover_Split(self, e):
        self.Animated_Hover(self.container_split, e)

    def Hover_Convert(self, e):
        self.Animated_Hover(self.container_convert, e)

    def Hover_Merge(self, e):
        self.Animated_Hover(self.container_merge, e)

    def Hover_Compress(self, e):
        self.Animated_Hover(self.container_compress, e)

    def Hover_Calendar(self, e):
        self.Animated_Hover(self.container_calendar, e)

    def Hover_Management(self, e):
        self.Animated_Hover(self.container_management, e)

    def Hover_Watermark(self, e):
        self.Animated_Hover(self.container_watermark, e)

    def build(self):
        return Container(
            content=Column(
                [
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.container_encrypt, self.container_decrypt],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.container_rotate, self.container_split],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.container_convert, self.container_merge],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.container_compress, self.container_calendar],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.container_management, self.container_watermark],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[self.moxfy_describe],
                    ),
                ],
            ),
        )
