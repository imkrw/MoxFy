from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doEncrypt
import helper.jsonhandle as ujson
import helper.pathhandle as upath
import os
import json


class Encrypt(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Encrypt")

        self.title_mt = Text("Encryption Method")

        """AES-256"""
        self.path_aes_256 = None
        self.pick_file_aes_256 = BrowsePDF(on_result=self.result_aes_256)
        self.page.overlay.extend([self.pick_file_aes_256])
        self.title_aes_256 = Text("Advanced Encryption Standard 256-Bit (AES-256)")
        self.browse_aes_256 = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_aes_256.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.encrypt_aes_256 = OutlinedButton(
            "Encrypt",
            icon="ENHANCED_ENCRYPTION",
            on_click=self.start_encrypt_aes_256,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_aes_256_method = Container(
            content=ElevatedButton(
                content=Text(
                    "AES-256",
                ),
                on_click=self.task_aes_256,
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
        self.suggest_user = Text("THE STRONGEST METHOD", size=13, weight="w400")

        """AES-128"""
        self.path_aes_128 = None
        self.pick_file_aes_128 = BrowsePDF(on_result=self.result_aes_128)
        self.page.overlay.extend([self.pick_file_aes_128])
        self.title_aes_128 = Text("Advanced Encryption Standard 128-Bit (AES-128)")
        self.browse_aes_128 = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_aes_128.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.encrypt_aes_128 = OutlinedButton(
            "Encrypt",
            icon="ENHANCED_ENCRYPTION",
            on_click=self.start_encrypt_aes_128,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_aes_128_method = Container(
            content=ElevatedButton(
                content=Text(
                    "AES-128",
                ),
                on_click=self.task_aes_128,
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

        """RC4-128"""
        self.path_rc4_128 = None
        self.pick_file_rc4_128 = BrowsePDF(on_result=self.result_rc4_128)
        self.page.overlay.extend([self.pick_file_rc4_128])
        self.title_rc4_128 = Text("Rivest Cipher 4 128-Bit (RC4-128)")
        self.browse_rc4_128 = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_rc4_128.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.encrypt_rc4_128 = OutlinedButton(
            "Encrypt",
            icon="ENHANCED_ENCRYPTION",
            on_click=self.start_encrypt_rc4_128,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_rc4_128_method = Container(
            content=ElevatedButton(
                content=Text(
                    "RC4-128",
                ),
                on_click=self.task_rc4_128,
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

        """RC4-40"""
        self.path_rc4_40 = None
        self.pick_file_rc4_40 = BrowsePDF(on_result=self.result_rc4_40)
        self.page.overlay.extend([self.pick_file_rc4_40])
        self.title_rc4_40 = Text("Rivest Cipher 4 40-Bit (RC4-40)")
        self.browse_rc4_40 = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_rc4_40.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.encrypt_rc4_40 = OutlinedButton(
            "Encrypt",
            icon="ENHANCED_ENCRYPTION",
            on_click=self.start_encrypt_rc4_40,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.select_rc4_40_method = Container(
            content=ElevatedButton(
                content=Text(
                    "RC4-40",
                ),
                on_click=self.task_rc4_40,
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

        """Permissions"""
        self.json_file_path = os.path.join(
            upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE
        )
        self.permission_keys = [
            "print",
            "copy",
            "annotate",
            "modify",
            "form",
            "assemble",
            "printhq",
        ]

        self._column = Column()

        self.encrypt_method = Row(
            controls=[
                self.select_aes_256_method,
                self.select_aes_128_method,
                self.select_rc4_128_method,
                self.select_rc4_40_method,
            ],
        )

        self.container_aes_256 = (
            self.title_aes_256,
            self.browse_aes_256,
            self.encrypt_aes_256,
            self.suggest_user,
        )

        self.container_aes_128 = (
            self.title_aes_128,
            self.browse_aes_128,
            self.encrypt_aes_128,
        )

        self.container_rc4_128 = (
            self.title_rc4_128,
            self.browse_rc4_128,
            self.encrypt_rc4_128,
        )

        self.container_rc4_40 = (
            self.title_rc4_40,
            self.browse_rc4_40,
            self.encrypt_rc4_40,
        )

    def _container(self, title, browse_button, encrypt_button, suggest_user=None):
        controls = [
            ListTile(
                leading=Icon(icons.INFO),
                title=title,
            ),
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    browse_button,
                    encrypt_button,
                ],
            ),
        ]
        if suggest_user is not None:
            controls.append(
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Divider(height=40, color="transparent"),
                        suggest_user,
                    ],
                )
            )
        return Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=controls,
            ),
        )

    def task_aes_256(self, e):
        self._column.controls.clear()
        self._column.controls.append(self._container(*self.container_aes_256))
        self.update()

    def task_aes_128(self, e):
        self._column.controls.clear()
        self._column.controls.append(self._container(*self.container_aes_128))
        self.update()

    def task_rc4_128(self, e):
        self._column.controls.clear()
        self._column.controls.append(self._container(*self.container_rc4_128))
        self.update()

    def task_rc4_40(self, e):
        self._column.controls.clear()
        self._column.controls.append(self._container(*self.container_rc4_40))
        self.update()

    def result_aes_256(self, e: FilePickerResultEvent):
        self.path_aes_256 = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_aes_256}"), open=True))

    def result_aes_128(self, e: FilePickerResultEvent):
        self.path_aes_128 = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_aes_128}"), open=True))

    def result_rc4_128(self, e: FilePickerResultEvent):
        self.path_rc4_128 = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_rc4_128}"), open=True))

    def result_rc4_40(self, e: FilePickerResultEvent):
        self.path_rc4_40 = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path_rc4_40}"), open=True))

    def extract_permissions(self, json_file_path, permission_keys):
        try:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            self.page.show_snack_bar(
                SnackBar(Text(f"JSON file not found: {json_file_path}"), open=True)
            )
            return
        except json.JSONDecodeError:
            self.page.show_snack_bar(
                SnackBar(
                    Text(f"Invalid JSON format in the file: {json_file_path}"),
                    open=True,
                )
            )
            return

        permissions = data.get("permissions", {})

        permissions_dict = {}
        for key in permission_keys:
            permissions_dict[key] = permissions.get(key, False)

        return permissions_dict

    def start_encrypt_aes_256(self, e):
        permissions_dict = self.extract_permissions(
            self.json_file_path, self.permission_keys
        )
        try:
            doEncrypt(
                self.path_aes_256,
                ujson.load_value(
                    upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_user_password"
                ),
                ujson.load_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "encrypt_owner_password",
                ),
                "AES_256",
                permissions_dict,
                upath.ENCRYPT_AES_256_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Encrypted [AES-256] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_encrypt_aes_128(self, e):
        permissions_dict = self.extract_permissions(
            self.json_file_path, self.permission_keys
        )
        try:
            doEncrypt(
                self.path_aes_128,
                ujson.load_value(
                    upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_user_password"
                ),
                ujson.load_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "encrypt_owner_password",
                ),
                "AES_128",
                permissions_dict,
                upath.ENCRYPT_AES_128_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Encrypted [AES-128] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_encrypt_rc4_128(self, e):
        permissions_dict = self.extract_permissions(
            self.json_file_path, self.permission_keys
        )
        try:
            doEncrypt(
                self.path_rc4_128,
                ujson.load_value(
                    upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_user_password"
                ),
                ujson.load_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "encrypt_owner_password",
                ),
                "RC4_128",
                permissions_dict,
                upath.ENCRYPT_RC4_128_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Encrypted [RC4-128] Successfully."), open=True)
            )
            return
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def start_encrypt_rc4_40(self, e):
        permissions_dict = self.extract_permissions(
            self.json_file_path, self.permission_keys
        )
        try:
            doEncrypt(
                self.path_rc4_40,
                ujson.load_value(
                    upath.CRYPT_DATA_DIR, upath.CRYPT_DATA_FILE, "encrypt_user_password"
                ),
                ujson.load_value(
                    upath.CRYPT_DATA_DIR,
                    upath.CRYPT_DATA_FILE,
                    "encrypt_owner_password",
                ),
                "RC4_40",
                permissions_dict,
                upath.ENCRYPT_RC4_40_RESULT,
            )
            self.page.show_snack_bar(
                SnackBar(Text("File Encrypted [RC4-40] Successfully."), open=True)
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
                        controls=[Container(content=self.encrypt_method, padding=15)],
                    ),
                    Row(
                        controls=[
                            self._column,
                        ],
                    ),
                ],
            ),
        )
