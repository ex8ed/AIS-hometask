from PySide6.QtWidgets import QMessageBox
from config.internationalization import all_languages


class Message:
    def __init__(self, title: str, tag: str, icon: QMessageBox.Icon):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(all_languages["ru"][tag])
        msg_box.show()
        r = msg_box.exec()


class GnSuccess(Message):
    def __init__(self, tag: str):
        super().__init__(all_languages["ru"]["SUCCESS"], tag, QMessageBox.Icon.Information)


class GnWarning(Message):
    def __init__(self, tag: str):
        super().__init__(all_languages["ru"]["WARNING"], tag, QMessageBox.Icon.Warning)


class GnCritical(Message):
    def __init__(self, tag: str):
        super().__init__(all_languages["ru"]["ERROR"], tag, QMessageBox.Icon.Critical)
