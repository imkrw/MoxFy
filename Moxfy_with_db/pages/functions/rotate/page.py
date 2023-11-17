from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doRotate, doRotateCustomPage, doRotateRangePages
import helper.pathhandle as upath


class R0tate(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Rotate")

        self.title_mt = Text("Rotation Method")

        self.dropdown_option = [
            dropdown.Option("0°"),
            dropdown.Option("45°"),
            dropdown.Option("90°"),
            dropdown.Option("180°"),
            dropdown.Option("270°"),
            dropdown.Option("360°"),
        ]

        """All pages"""
        self.pick_file_all_pages = BrowsePDF(on_result=self.result_all_pages)
        self.page.overlay.extend([self.pick_file_all_pages])
        self.path_all_pages = None
        self.stored_value_all_pages = None
        self.title_all_pages = Text("Rotate With All Pages")
        self.browse_all_pages = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_all_pages.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.rotate_all_pages = OutlinedButton(
            "Rotate",
            icon="ROTATE_LEFT",
            on_click=self.start_rotate_all_pages,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_all_pages_method = Container(
            content=ElevatedButton(
                content=Text(
                    "All Pages",
                ),
                on_click=self.task_all_pages,
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
                width=145,
            ),
        )
        self.dropdown_all_pages = Dropdown(
            options=self.dropdown_option,
            on_change=self.dropdown_change_all_pages,
            border_color="#BDB5D5",
            border_radius=10,
            label="Rotation Angle",
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            height=40,
            width=200,
            alignment=alignment.center,
        )

        """Custom page"""
        self.pick_file_custom_page = BrowsePDF(on_result=self.result_custom_page)
        self.page.overlay.extend([self.pick_file_custom_page])
        self.path_custom_page = None
        self.stored_value_custom_page = None
        self.title_custom_page = Text("Rotate With Custom Page")
        self.browse_custom_page = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_custom_page.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.rotate_custom_page = OutlinedButton(
            "Rotate",
            icon="ROTATE_LEFT",
            on_click=self.start_rotate_custom_page,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_custom_page_method = Container(
            content=ElevatedButton(
                content=Text(
                    "Custom Page",
                ),
                on_click=self.task_custom_page,
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
                width=145,
            ),
        )
        self.dropdown_custom_page = Dropdown(
            options=self.dropdown_option,
            on_change=self.dropdown_change_custom_page,
            border_color="#BDB5D5",
            border_radius=10,
            label="Rotation Angle",
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            height=40,
            width=200,
            alignment=alignment.center,
        )
        self.field_pageNum = TextField(
            hint_text="Page Number (Integer)",
            height=40,
            width=200,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )

        """Range pages"""
        self.pick_file_range_pages = BrowsePDF(on_result=self.result_range_pages)
        self.page.overlay.extend([self.pick_file_range_pages])
        self.path_range_pages = None
        self.stored_value_range_pages = None
        self.title_range_pages = Text("Rotate With Range Pages")
        self.browse_range_pages = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_range_pages.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.rotate_range_pages = OutlinedButton(
            "Rotate",
            icon="ROTATE_LEFT",
            on_click=self.start_rotate_range_pages,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_range_pages_method = Container(
            content=ElevatedButton(
                content=Text(
                    "Range Pages",
                ),
                on_click=self.task_range_pages,
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
                width=145,
            ),
        )
        self.dropdown_range_pages = Dropdown(
            options=self.dropdown_option,
            on_change=self.dropdown_change_range_pages,
            border_color="#BDB5D5",
            border_radius=10,
            label="Rotation Angle",
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            height=40,
            width=200,
            alignment=alignment.center,
        )
        self.field_frompageNum = TextField(
            hint_text="From Page Number (Integer)",
            height=40,
            width=200,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )
        self.field_topageNum = TextField(
            hint_text="To Page Number (Integer)",
            height=40,
            width=200,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )

        self.container_all_pages = Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=self.title_all_pages,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_all_pages,
                            self.dropdown_all_pages,
                            self.rotate_all_pages,
                        ],
                    ),
                ],
            ),
        )

        self.container_custom_page = Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=self.title_custom_page,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_custom_page,
                            self.dropdown_custom_page,
                            self.field_pageNum,
                            self.rotate_custom_page,
                        ],
                    ),
                ],
            ),
        )

        self.container_range_pages = Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=self.title_range_pages,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_range_pages,
                            self.field_frompageNum,
                            self.field_topageNum,
                            self.rotate_range_pages,
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.dropdown_range_pages,
                        ],
                    ),
                ],
            ),
        )

        self._column = Column()

        self.rotate_method = Row(
            controls=[
                self.select_all_pages_method,
                self.select_custom_page_method,
                self.select_range_pages_method,
            ],
        )

    def task_all_pages(self, e):
        self._column.controls.clear()
        self._column.controls.append(self.container_all_pages)
        self.update()

    def task_custom_page(self, e):
        self._column.controls.clear()
        self._column.controls.append(self.container_custom_page)
        self.update()

    def task_range_pages(self, e):
        self._column.controls.clear()
        self._column.controls.append(self.container_range_pages)
        self.update()

    def dropdown_change_all_pages(self, e):
        value = self.dropdown_all_pages.value
        degree_map = {
            "0°": 0,
            "45°": 45,
            "90°": 90,
            "180°": 180,
            "270°": 270,
            "360°": 360,
        }
        if value in degree_map:
            self.stored_value_all_pages = degree_map[value]

    def dropdown_change_custom_page(self, e):
        value = self.dropdown_custom_page.value
        degree_map = {
            "0°": 0,
            "45°": 45,
            "90°": 90,
            "180°": 180,
            "270°": 270,
            "360°": 360,
        }
        if value in degree_map:
            self.stored_value_custom_page = degree_map[value]

    def dropdown_change_range_pages(self, e):
        value = self.dropdown_range_pages.value
        degree_map = {
            "0°": 0,
            "45°": 45,
            "90°": 90,
            "180°": 180,
            "270°": 270,
            "360°": 360,
        }
        if value in degree_map:
            self.stored_value_range_pages = degree_map[value]

    def result_all_pages(self, e: FilePickerResultEvent):
        self.path_all_pages = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_all_pages}"), open=True))

    def result_custom_page(self, e: FilePickerResultEvent):
        self.path_custom_page = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_custom_page}"), open=True))

    def result_range_pages(self, e: FilePickerResultEvent):
        self.path_range_pages = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_range_pages}"), open=True))

    def start_rotate_all_pages(self, e):
        try:
            doRotate(
                self.path_all_pages, self.stored_value_all_pages, upath.ROTATE_RESULT
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Rotated [All Pages] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_rotate_custom_page(self, e):
        try:
            int_val = int(self.field_pageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doRotateCustomPage(
                self.path_custom_page,
                self.stored_value_custom_page,
                int_val,
                upath.ROTATE_ONEPAGE_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Rotated [Custom Page] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_rotate_range_pages(self, e):
        try:
            int_val_from = int(self.field_frompageNum.value)
            int_val_to = int(self.field_topageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doRotateRangePages(
                self.path_range_pages,
                self.stored_value_range_pages,
                int_val_from,
                int_val_to,
                upath.ROTATE_RANGEPAGES_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Rotated [Range Pages] Successfully."), open=True)
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
                            ListTile(
                                leading=Icon(icons.INFO),
                                title=self.title_mt,
                            ),
                        ],
                    ),
                    Row(
                        controls=[Container(content=self.rotate_method, padding=15)],
                    ),
                    Row(
                        controls=[
                            self._column,
                        ],
                    ),
                ],
            ),
        )
