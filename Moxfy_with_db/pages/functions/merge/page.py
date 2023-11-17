from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doMerge
import helper.pathhandle as upath


class Merge(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Merge")

        """Merge"""
        self.pick_file_merge = BrowsePDF(on_result=self.result_merge)
        self.page.overlay.extend([self.pick_file_merge])
        self.path_merge = []
        self.path_filename = []
        self.title_merge = Text("Custom Merging As Needed")
        self.browse_merge = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_merge.pick_files(
                dialog_title="Open PDF Files",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=True,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.merge = OutlinedButton(
            "Merge",
            icon="CALL_MERGE",
            on_click=self.start_merge,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )

    def result_merge(self, e: FilePickerResultEvent):
        if e.files:
            for file_info in e.files:
                self.path_merge.append(file_info.path)
                self.path_filename.append(file_info.name)
            display_path = ", ".join(self.path_filename)
        else:
            display_path = "No File Attached"
            self.path_merge.clear()
            self.path_filename.clear()
        self.page.show_snack_bar(SnackBar(Text(display_path), open=True))

    def start_merge(self, e):
        try:
            doMerge(self.path_merge, upath.MERGE_RESULT)
            self.page.show_snack_bar(
                SnackBar(Text("File Merged Successfully."), open=True)
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
                                            title=self.title_merge,
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                self.browse_merge,
                                                self.merge,
                                            ],
                                        ),
                                    ],
                                ),
                            )
                        ],
                    ),
                ],
            ),
        )
