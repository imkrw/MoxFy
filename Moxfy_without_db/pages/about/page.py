from flet import *
from helper.appbar import appBarGeneralView


class About(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        
        self.page.appbar = appBarGeneralView("/main", page, "About")

        self.moxfy = Text("MoxFy", color=colors.RED_400, weight="bold")
        self.moxfy_describe = Text("A PDF Utility Tool Designed To Simplify Your Document Management Process.")
        self.consult_authors = Text("The Project Consultant And Authors", color=colors.RED_400, weight="bold")
        self.consult_authors_describe = Text(
            font_family="poppins",
            disabled=False,
            spans=[
                TextSpan("A list of the project consultant and authors can be found "),
                TextSpan(
                    "Here.",
                    TextStyle(decoration=TextDecoration.NONE, weight="w400", color="blue"),
                    on_click=lambda e: self.page.go("/authors"),
                ),
            ],
        )
        self.encrypt_decrypt = Text("Encrypt And Decrypt", color=colors.RED_400, weight="bold")
        self.encrypt_decrypt_describe = Text("Using algorithms such as AES-256, AES-128, RC4-128, RC4-40 to protect your PDF files with password encryption.")
        self.rotat3 = Text("Rotate", color=colors.RED_400, weight="bold")
        self.rotat3_describe = Text("Choose to rotate all pages or select custom page ranges to adjust the orientation of specific pages.")
        self.split = Text("Split", color=colors.RED_400, weight="bold")
        self.split_describe = Text("Easily split large PDF files into smaller ones, Split all pages or custom page ranges.")
        self.c0nvert = Text("Convert", color=colors.RED_400, weight="bold")
        self.c0nvert_describe_docx = Text("PDF to DOCX Conversion: Seamlessly convert PDF files to DOCX format.")
        self.c0nvert_describe_jpg_png = Text("PDF to JPG/PNG Conversion: Effortlessly transform PDF pages into high-quality JPG or PNG images.")
        self.merge = Text("Merge", color=colors.RED_400, weight="bold")
        self.merge_describe = Text("This feature now offers the capability to combine multiple files")
        self.compress = Text("Compress", color=colors.RED_400, weight="bold")
        self.compress_describe = Text("Using 3 methods Lossless Compression, Removing Duplication, Remove Images, to optimize the content and reduce the file size of PDF pages.")
        self.management = Text("Management", color=colors.RED_400, weight="bold")
        self.management_describe = Text("Effortlessly Delete, Re-Arrange PDF Pages.")
        self.watermark = Text("Watermark", color=colors.RED_400, weight="bold")
        self.watermark_describe = Text("Apply watermarks to PDF files by using an image as the watermark source.")

        self.content = Column(
            [
                self.moxfy,
                self.moxfy_describe,
                self.consult_authors,
                self.consult_authors_describe,
                self.encrypt_decrypt,
                self.encrypt_decrypt_describe,
                self.rotat3,
                self.rotat3_describe,
                self.split,
                self.split_describe,
                self.c0nvert,
                self.c0nvert_describe_docx,
                self.c0nvert_describe_jpg_png,
                self.merge,
                self.merge_describe,
                self.compress,
                self.compress_describe,
                self.management,
                self.management_describe,
                self.watermark,
                self.watermark_describe,
            ],
            scroll=ScrollMode.HIDDEN,
            height=525,
            width=900,
        )

        self._container = Container(
            self.content,
            expand=True,
            alignment=alignment.top_center,
        )

        ...
        ...
        ...

        self.about = Row([self._container], expand=True)

    def build(self):
        return self.about
