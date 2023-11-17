from flet import *
from helper.appbar import appBarGeneralView
from helper.filepicker import BrowsePDF
from core.methods import doWatermarkImage
import helper.pathhandle as upath


class Watermark(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.page.appbar = appBarGeneralView("/main", page, "Watermark")

        """Image Method"""
        self.pick_file_path = BrowsePDF(on_result=self.result_file_path)
        self.pick_img_path = BrowsePDF(on_result=self.result_img_path)
        self.page.overlay.extend([self.pick_file_path])
        self.page.overlay.extend([self.pick_img_path])
        self.title_img = Text(
            "Watermark With Image File"
        )
        self.subtitle = Text("Supports only JPG and PNG formats, and assumes the same paper size on every single page")
        self.path = None
        self.img_path = None
        self.browse_file = OutlinedButton(
            "Browse File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_file_path.pick_files(
                dialog_title="Open PDF File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["pdf"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.browse_img = OutlinedButton(
            "Browse Image File",
            icon="ATTACH_FILE",
            on_click=lambda _: self.pick_img_path.pick_files(
                dialog_title="Open Image File",
                file_type=FilePickerFileType.ANY,
                allowed_extensions=["jpg", "png"],
                allow_multiple=False,
            ),
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.watermark = OutlinedButton(
            "Watermark",
            icon="WATER_DROP",
            on_click=self.start_watermark,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)),
        )
        self.field_size = TextField(
            hint_text="Size (Example: 5)",
            height=40,
            width=150,
            border_color="#BDB5D5",
            border_radius=10,
            content_padding=Padding(left=5, top=3, right=5, bottom=3),
            keyboard_type=KeyboardType.TEXT,
        )
        self.top_left = Checkbox(
            label="\tTop Left",
            on_change=self.align_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.top_center = Checkbox(
            label="\tTop Center",
            on_change=self.align_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.top_right = Checkbox(
            label="\tTop Right",
            on_change=self.align_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.bottom_left = Checkbox(
            label="\tBottom Left",
            on_change=self.align_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.bottom_center = Checkbox(
            label="\tBottom Center",
            on_change=self.align_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.bottom_right = Checkbox(
            label="\tBottom Right",
            on_change=self.align_changed,
            fill_color={MaterialState.DEFAULT: colors.BLUE},
        )
        self.checkboxes = {
            "Top Left": self.top_left,
            "Top Center": self.top_center,
            "Top Right": self.top_right,
            "Bottom Left": self.bottom_left,
            "Bottom Center": self.bottom_center,
            "Bottom Right": self.bottom_right,
        }
        self.checkbox_row = Container(
            content=Row(
                [
                    self.top_left,
                    self.top_center,
                    self.top_right,
                    self.bottom_left,
                    self.bottom_center,
                    self.bottom_right,
                ],
                alignment="start",
            ),
            scale=Scale(scale=1),
            padding=9,
            width=900,
            height=45,
        )

    def _container(self, title):
        return Container(
            width=self.page.width,
            height=self.page.height,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    ListTile(
                        leading=Icon(icons.INFO),
                        title=title,
                        subtitle=self.subtitle,
                    ),
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            self.checkbox_row,
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.field_size,
                        ],
                    ),
                    Divider(height=1, color="transparent"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.browse_file,
                            self.browse_img,
                            self.watermark,
                        ],
                    ),
                ],
            ),
        )

    def align_changed(self, e):
        selected_checkbox = None
        for checkbox_name, checkbox in self.checkboxes.items():
            if checkbox.value:
                selected_checkbox = checkbox
                break

        if selected_checkbox:
            for checkbox_to_disable in self.checkboxes.values():
                if checkbox_to_disable != selected_checkbox:
                    checkbox_to_disable.disabled = True
                    checkbox_to_disable.update()
        else:
            for checkbox_to_enable in self.checkboxes.values():
                checkbox_to_enable.disabled = False
                checkbox_to_enable.update()

    def result_file_path(self, e: FilePickerResultEvent):
        self.path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.path}"), open=True))

    def result_img_path(self, e: FilePickerResultEvent):
        self.img_path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "No File Attached"
        )
        self.page.show_snack_bar(SnackBar(Text(f"{self.img_path}"), open=True))

    def start_watermark(self, e):
        try:
            int_val = int(self.field_size.value)
        except ValueError:
            self.page.show_snack_bar(
                SnackBar(Text("Invalid size number or missing."), open=True)
            )
            return
        try:
            selected_alignment = None
            for alignment, checkbox in self.checkboxes.items():
                if checkbox.value:
                    selected_alignment = alignment
                    break
            if selected_alignment:
                doWatermarkImage(
                    self.path,
                    self.img_path,
                    int_val,
                    selected_alignment.lower(),
                    upath.WATERMARKIMAGE_RESULT,
                )
                self.page.show_snack_bar(
                    SnackBar(
                        Text("File Watermarked [With Image] Successfully."), open=True
                    )
                )
                return
            else:
                raise ValueError("Please select an alignment.")
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(str(ex)), open=True))
            return

    def build(self):
        return Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            self._container(
                                self.title_img,
                            )
                        ],
                    ),
                ],
            ),
        )
