from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doSplit, doSplitCustomPage, doSplitRangePages
import helper.pathhandle as upath


class Split(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Split")

        self.title_mt = Text("Split Method")

        """All Pages"""
        self.pick_file_all_pages = BrowsePDF(on_result=self.result_all_pages)
        self.page.overlay.extend([self.pick_file_all_pages])
        self.split_all_pages_path = None
        self.title_all_pages = Text("Split With All Pages")
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
        self.split_all_pages = OutlinedButton(
            "Split",
            icon="CALL_SPLIT",
            on_click=self.start_split_all_pages,
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

        """One Page --> Custom"""
        self.pick_file_one_page = BrowsePDF(on_result=self.result_one_page)
        self.page.overlay.extend([self.pick_file_one_page])
        self.split_one_page_path = None
        self.title_custom_page = Text("Split With Custom Page")
        self.browse_one_page = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_one_page.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.split_one_page = OutlinedButton(
            "Split",
            icon="CALL_SPLIT",
            on_click=self.start_split_one_page,
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
        self.field_pageNum = TextField(
            hint_text="Page Number (Integer)",
            height=40,
            width=200,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )

        """Range Pages"""
        self.pick_file_range_pages = BrowsePDF(on_result=self.result_range_pages)
        self.page.overlay.extend([self.pick_file_range_pages])
        self.split_range_pages_path = None
        self.title_range_pages = Text("Split With Range Pages")
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
        self.split_range_pages = OutlinedButton(
            "Split",
            icon="CALL_SPLIT",
            on_click=self.start_split_range_pages,
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

        self._column = Column()

        self.split_method = Row(
            controls=[
                self.select_all_pages_method,
                self.select_custom_page_method,
                self.select_range_pages_method,
            ],
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
                            self.split_all_pages,
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
                            self.browse_one_page,
                            self.field_pageNum,
                            self.split_one_page,
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
                            self.split_range_pages,
                        ],
                    ),
                ],
            ),
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

    def result_all_pages(self, e: FilePickerResultEvent):
        self.split_all_pages_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(
            SnackBar(Text(f"{self.split_all_pages_path}"), open=True)
        )

    def result_one_page(self, e: FilePickerResultEvent):
        self.split_one_page_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(
            SnackBar(Text(f"{self.split_one_page_path}"), open=True)
        )

    def result_range_pages(self, e: FilePickerResultEvent):
        self.split_range_pages_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(
            SnackBar(Text(f"{self.split_range_pages_path}"), open=True)
        )

    def start_split_all_pages(self, e):
        try:
            doSplit(self.split_all_pages_path, upath.SPLIT_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Successfully Split Into Parts."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_split_one_page(self, e):
        try:
            int_val = int(self.field_pageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doSplitCustomPage(
                self.split_one_page_path, int_val, upath.SPLIT_ONEPAGE_RESULT
            )
            self.page.show_snack_bar(
                SnackBar(
                    Text("File Successfully Split Into Part [One Page]."), open=True
                )
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_split_range_pages(self, e):
        try:
            int_val_from = int(self.field_frompageNum.value)
            int_val_to = int(self.field_topageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doSplitRangePages(
                self.split_range_pages_path,
                int_val_from,
                int_val_to,
                upath.SPLIT_RANGEPAGES_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(
                    Text("File Successfully Split Into Part [Range Pages]."), open=True
                )
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
                        controls=[Container(content=self.split_method, padding=15)],
                    ),
                    Row(
                        controls=[
                            self._column,
                        ],
                    ),
                ],
            ),
        )
