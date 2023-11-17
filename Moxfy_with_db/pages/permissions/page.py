from flet import *
from helper.appbar import appBarGeneralView
import helper.jsonhandle as ujson
import helper.pathhandle as upath


class SetPermissions(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/utils", page, "Permissions")

        self.print = Checkbox(
            label="\tprint - permit printing",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "print"
            ),
        )

        self.print.on_change = self.permission_changed

        self.copy = Checkbox(
            label="\tcopy - permit copying",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "copy"
            ),
        )

        self.annotate = Checkbox(
            label="\tannotate - permit Add or modify text annotations and interactive form fields",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "annotate"
            ),
        )

        self.modify = Checkbox(
            label="\tmodify - permit Modify the document’s contents",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "modify"
            ),
        )

        self.form = Checkbox(
            label="\tform - permit Fill in forms and sign the document",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "form"
            ),
        )

        self.assemble = Checkbox(
            label="\tassemble - permit Insert, rotate, or delete pages, bookmarks, thumbnail images",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "assemble"
            ),
        )

        self.printhq = Checkbox(
            label="\tprinthq - permit High quality printing",
            on_change=self.permission_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
            value=ujson.load_value(
                upath.PERMISSION_DATA_DIR, upath.PERMISSION_DATA_FILE, "printhq"
            ),
            disabled=True,
        )

        self.checkboxes = {
            "print": self.print,
            "copy": self.copy,
            "annotate": self.annotate,
            "modify": self.modify,
            "form": self.form,
            "assemble": self.assemble,
            "printhq": self.printhq,
        }

        self.content = Column(
            [
                self.print,
                self.copy,
                self.annotate,
                self.modify,
                self.form,
                self.assemble,
                self.printhq,
            ],
        )

        self._container = Container(
            self.content,
            margin=10,
            padding=10,
            alignment=alignment.top_center,
        )

        self.permissions = Row([self._container])

    def permission_changed(self, e):
        permissions = {}
        for permission, checkbox in self.checkboxes.items():
            if checkbox.value:
                permissions[permission] = True
            if not checkbox.value:
                permissions[permission] = False

        if self.print.value == True:
            self.printhq.disabled = False
            self.printhq.update()
        else:
            self.printhq.disabled = True
            self.printhq.value = None
            permissions["printhq"] = False
            self.printhq.update()

        ujson.save_value(
            upath.PERMISSION_DATA_DIR,
            upath.PERMISSION_DATA_FILE,
            "permissions",
            permissions,
        )

    def build(self):
        return self.permissions
