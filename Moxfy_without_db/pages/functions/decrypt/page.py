from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doDecrypt
import helper.jsonhandle as ujson
import helper.pathhandle as upath


class Decrypt(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Decrypt")

        """Decrypt"""
        self.path_decrypt = None
        self.pick_file_decrypt = BrowsePDF(on_result=self.result_decrypt)
        self.page.overlay.extend([self.pick_file_decrypt])
        self.title_decrypt = Text("Decrypt With AES-256, AES-128, RC4-128, RC4-40")
        self.browse_decrypt = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_decrypt.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.decrypt = OutlinedButton(
            "Decrypt",
            icon="NO_ENCRYPTION",
            on_click=self.start_decrypt,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )

    def result_decrypt(self, e: FilePickerResultEvent):
        self.path_decrypt = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_decrypt}"), open=True))

    def start_decrypt(self, e):
        try:
            doDecrypt(
                self.path_decrypt,
                ujson.load_value(
                    upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "decrypt_password"
                ),
                upath.DECRYPT_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Decrypted Successfully."), open=True)
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
                                            title=self.title_decrypt,
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                self.browse_decrypt,
                                                self.decrypt,
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
