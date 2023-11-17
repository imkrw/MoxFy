from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import do2docx, do2png, do2jpg
import helper.pathhandle as upath


class Convert(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Convert")

        self.title_mt = Text("Convert Method")

        """PDF TO DOCX"""
        self.pick_file_docx = BrowsePDF(on_result=self.result_docx)
        self.page.overlay.extend([self.pick_file_docx])
        self.path_docx = None
        self.title_docx = Text("Convert TO DOCX Format")
        self.browse_docx = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_docx.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.convert_docx = OutlinedButton(
            "Convert",
            icon="SWAP_VERT",
            on_click=self.start_convert_docx,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_docx_method = Container(
            content=ElevatedButton(
                content=Text(
                    "TO DOCX",
                ),
                on_click=self.task_docx,
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
                width=125,
            ),
        )

        """PDF TO JPG"""
        self.pick_file_jpg = BrowsePDF(on_result=self.result_jpg)
        self.page.overlay.extend([self.pick_file_jpg])
        self.path_jpg = None
        self.title_jpg = Text("Convert TO JPG Format")
        self.browse_jpg = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_jpg.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.convert_jpg = OutlinedButton(
            "Convert",
            icon="SWAP_VERT",
            on_click=self.start_convert_jpg,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_jpg_method = Container(
            content=ElevatedButton(
                content=Text(
                    "TO JPG",
                ),
                on_click=self.task_jpg,
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
                width=125,
            ),
        )

        """"PDF TO PNG"""
        self.pick_file_png = BrowsePDF(on_result=self.result_png)
        self.page.overlay.extend([self.pick_file_png])
        self.path_png = None
        self.title_png = Text("Convert TO PNG Format")
        self.browse_png = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_png.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.convert_png = OutlinedButton(
            "Convert",
            icon="SWAP_VERT",
            on_click=self.start_convert_png,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_png_method = Container(
            content=ElevatedButton(
                content=Text(
                    "TO PNG",
                ),
                on_click=self.task_png,
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
                width=125,
            ),
        )

        self._column = Column()

        self.convert_method = Row(
            controls=[
                self.select_docx_method,
                self.select_jpg_method,
                self.select_png_method,
            ],
        )

    def _container(self, title, browse_button, process_button):
        return Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=title,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            browse_button,
                            process_button,
                        ],
                    ),
                ],
            ),
        )

    def task_docx(self, e):
        self._column.controls.clear()
        self._column.controls.append(
            self._container(
                self.title_docx,
                self.browse_docx,
                self.convert_docx,
            )
        )

        self.update()

    def task_jpg(self, e):
        self._column.controls.clear()
        self._column.controls.append(
            self._container(
                self.title_jpg,
                self.browse_jpg,
                self.convert_jpg,
            )
        )

        self.update()

    def task_png(self, e):
        self._column.controls.clear()
        self._column.controls.append(
            self._container(
                self.title_png,
                self.browse_png,
                self.convert_png,
            )
        )
        self.update()

    def result_docx(self, e: FilePickerResultEvent):
        self.path_docx = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_docx}"), open=True))

    def result_jpg(self, e: FilePickerResultEvent):
        self.path_jpg = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_jpg}"), open=True))

    def result_png(self, e: FilePickerResultEvent):
        self.path_png = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_png}"), open=True))

    def start_convert_docx(self, e):
        try:
            do2docx(self.path_docx, upath.PDF2DOCX_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Converted [DOCX] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_convert_jpg(self, e):
        try:
            do2jpg(self.path_jpg, upath.PDF2JPG_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Converted [JPG] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_convert_png(self, e):
        try:
            do2png(self.path_png, upath.PDF2PNG_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Converted [PNG] Successfully."), open=True)
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
                        controls=[Container(content=self.convert_method, padding=15)],
                    ),
                    Row(
                        controls=[
                            self._column,
                        ],
                    ),
                ],
            ),
        )
