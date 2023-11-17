from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import (
    doCompressLoseLess,
    doCompressRemoveDuplication,
    doCompressRemoveImages,
)
import helper.pathhandle as upath


class Compress(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Compress")

        self.title_mt = Text("Compression Method")

        """Remove Images"""
        self.pick_file_ri = BrowsePDF(on_result=self.result_ri)
        self.page.overlay.extend([self.pick_file_ri])
        self.path_ri = None
        self.title_ri = Text("Compress With Remove Images")
        self.browse_ri = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_ri.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.compress_ri = OutlinedButton(
            "Compress",
            icon="COMPRESS",
            on_click=self.start_ri,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_ri_method = Container(
            content=ElevatedButton(
                content=Text(
                    "Remove Images",
                ),
                on_click=self.task_ri,
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

        """Removing Duplication"""
        self.pick_file_rd = BrowsePDF(on_result=self.result_rd)
        self.page.overlay.extend([self.pick_file_rd])
        self.path_rd = None
        self.title_rd = Text("Compress With Remove Duplication")
        self.browse_rd = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_rd.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.compress_rd = OutlinedButton(
            "Compress",
            icon="COMPRESS",
            on_click=self.start_rd,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_rd_method = Container(
            content=ElevatedButton(
                content=Text(
                    "Remove Duplication",
                ),
                on_click=self.task_rd,
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
                width=195,
            ),
        )

        """Lossless Compression"""
        self.pick_file_lc = BrowsePDF(on_result=self.result_lc)
        self.page.overlay.extend([self.pick_file_lc])
        self.path_lc = None
        self.title_lc = Text("Compress With Lossless")
        self.browse_lc = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_lc.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.compress_lc = OutlinedButton(
            "Compress",
            icon="COMPRESS",
            on_click=self.start_lc,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_lc_method = Container(
            content=ElevatedButton(
                content=Text(
                    "Lossless",
                ),
                on_click=self.task_lc,
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

        self.compress_method = Row(
            controls=[
                self.select_ri_method,
                self.select_rd_method,
                self.select_lc_method,
            ],
        )

    def _container(self, title, browsebtn, processbtn):
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
                            browsebtn,
                            processbtn,
                        ],
                    ),
                ],
            ),
        )

    def task_ri(self, e):
        self._column.controls.clear()
        self._column.controls.append(
            self._container(
                self.title_ri,
                self.browse_ri,
                self.compress_ri,
            )
        )
        self.update()

    def task_rd(self, e):
        self._column.controls.clear()
        self._column.controls.append(
            self._container(
                self.title_rd,
                self.browse_rd,
                self.compress_rd,
            )
        )
        self.update()

    def task_lc(self, e):
        self._column.controls.clear()
        self._column.controls.append(
            self._container(
                self.title_lc,
                self.browse_lc,
                self.compress_lc,
            )
        )
        self.update()

    def result_ri(self, e: FilePickerResultEvent):
        self.path_ri = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_ri}"), open=True))

    def result_rd(self, e: FilePickerResultEvent):
        self.path_rd = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_rd}"), open=True))

    def result_lc(self, e: FilePickerResultEvent):
        self.path_lc = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_lc}"), open=True))

    def start_ri(self, e):
        try:
            doCompressRemoveImages(self.path_ri, upath.COMPRESS_RI_RESULT)
            self.page.show_snack_bar(
                SnackBar(
                    Text("File Compressed [Remove Images] Successfully."), open=True
                )
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_rd(self, e):
        try:
            doCompressRemoveDuplication(self.path_rd, upath.COMPRESS_RD_RESULT)
            self.page.show_snack_bar(
                SnackBar(
                    Text("File Compressed [Remove Duplication] Successfully."),
                    open=True,
                )
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_lc(self, e):
        try:
            doCompressLoseLess(self.path_lc, upath.COMPRESS_LL_RESULT)
            self.page.show_snack_bar(
                SnackBar(
                    Text("File Compressed [Lossless Compression] Successfully."),
                    open=True,
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
                        controls=[Container(content=self.compress_method, padding=15)],
                    ),
                    Row(
                        controls=[
                            self._column,
                        ],
                    ),
                ],
            ),
        )
