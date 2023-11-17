from flet import FilePicker


class BrowsePDF(FilePicker):
    def __init__(self, on_result):
        super().__init__(on_result=on_result)

    def pick_files(self, **kwargs):
        super().pick_files(**kwargs)
