from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doDeletePage, doDeletePages, doReArrange
import helper.pathhandle as upath


class Manage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Managements")

        self.title_mt = Text("Management Method")

        """Delete Page"""
        self.pick_file_delete_page = BrowsePDF(on_result=self.result_delete_page)
        self.page.overlay.extend([self.pick_file_delete_page])
        self.delete_page_file_path = None
        self.title_delete_page = Text("Delete With Custom Page")
        self.browse_file_delete_page = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_delete_page.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.delete_page = OutlinedButton(
            "Delete",
            icon="DELETE",
            on_click=self.start_delete_page,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
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
        self.select_delete_page = Container(
            content=ElevatedButton(
                content=Text(
                    "Delete Page",
                ),
                on_click=self.task_delete_page,
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
                width=175,
            ),
        )

        """Delete Pages"""
        self.pick_file_delete_pages = BrowsePDF(on_result=self.result_delete_pages)
        self.page.overlay.extend([self.pick_file_delete_pages])
        self.delete_pages_file_path = None
        self.title_delete_pages = Text("Delete With Range Of Page")
        self.browse_file_delete_pages = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_delete_pages.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.delete_pages = OutlinedButton(
            "Delete",
            icon="DELETE",
            on_click=self.start_delete_pages,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
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
        self.select_delete_pages = Container(
            content=ElevatedButton(
                content=Text(
                    "Delete Pages",
                ),
                on_click=self.task_delete_pages,
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
                width=175,
            ),
        )

        """Re-Arranging"""
        self.pick_file_re_arrange = BrowsePDF(on_result=self.result_re_arrange)
        self.page.overlay.extend([self.pick_file_re_arrange])
        self.re_arrange_file_path = None
        self.title_re_arrange = Text("Re-Arranging With Moving The Page")
        self.browse_file_re_arrange = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_re_arrange.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.re_arrange_button = OutlinedButton(
            "Re-Arranging",
            icon="star_rounded",
            on_click=self.start_re_arrange,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.field_re_arrange_frompageNum = TextField(
            hint_text="From Page Number (Integer)",
            height=40,
            width=200,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )
        self.field_re_arrange_topageNum = TextField(
            hint_text="To Page Number (Integer)",
            height=40,
            width=200,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )
        self.select_re_arrange = Container(
            content=ElevatedButton(
                content=Text(
                    "Re-Arranging",
                ),
                on_click=self.task_re_arrange,
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
                width=175,
            ),
        )

        self.container_delete_page = Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=self.title_delete_page,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_file_delete_page,
                            self.field_pageNum,
                            self.delete_page,
                        ],
                    ),
                ],
            ),
        )

        self.container_delete_pages = Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=self.title_delete_pages,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_file_delete_pages,
                            self.field_frompageNum,
                            self.field_topageNum,
                            self.delete_pages,
                        ],
                    ),
                ],
            ),
        )

        self.container_re_arrange = Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=self.title_re_arrange,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_file_re_arrange,
                            self.field_re_arrange_frompageNum,
                            self.field_re_arrange_topageNum,
                            self.re_arrange_button,
                        ],
                    ),
                ],
            ),
        )

        self._column = Column()

        self.manage_method = Row(
            controls=[
                self.select_delete_page,
                self.select_delete_pages,
                self.select_re_arrange,
            ],
        )

    def task_re_arrange(self, e):
        self._column.controls.clear()
        self._column.controls.append(self.container_re_arrange)
        self.update()

    def task_delete_page(self, e):
        self._column.controls.clear()
        self._column.controls.append(self.container_delete_page)
        self.update()

    def task_delete_pages(self, e):
        self._column.controls.clear()
        self._column.controls.append(self.container_delete_pages)
        self.update()

    def result_re_arrange(self, e: FilePickerResultEvent):
        self.re_arrange_file_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(
            SnackBar(Text(f"{self.re_arrange_file_path}"), open=True)
        )

    def result_delete_page(self, e: FilePickerResultEvent):
        self.delete_page_file_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(
            SnackBar(Text(f"{self.delete_page_file_path}"), open=True)
        )

    def result_delete_pages(self, e: FilePickerResultEvent):
        self.delete_pages_file_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(
            SnackBar(Text(f"{self.delete_pages_file_path}"), open=True)
        )

    def start_delete_page(self, e):
        try:
            int_val = int(self.field_pageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doDeletePage(self.delete_page_file_path, int_val, upath.DELETE_PAGE_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Successfully Deleted Page."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_delete_pages(self, e):
        try:
            int_val_from = int(self.field_frompageNum.value)
            int_val_to = int(self.field_topageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doDeletePages(
                self.delete_pages_file_path,
                int_val_from,
                int_val_to,
                upath.DELETE_PAGES_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Successfully Deleted Pages."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_re_arrange(self, e):
        try:
            int_value_re_arrange_from = int(self.field_re_arrange_frompageNum.value)
            int_value_re_arrange_to = int(self.field_re_arrange_topageNum.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid page number or missing."), open=True)
            )
            return
        try:
            doReArrange(
                self.re_arrange_file_path,
                int_value_re_arrange_from,
                int_value_re_arrange_to,
                upath.RE_ARRANGE_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Successfully Re-Arranged Page"), open=True)
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
                        controls=[Container(content=self.manage_method, padding=15)],
                    ),
                    Row(
                        controls=[
                            self._column,
                        ],
                    ),
                ],
            ),
        )
