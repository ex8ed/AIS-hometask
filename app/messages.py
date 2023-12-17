from PySide6.QtWidgets import QMessageBox


class Message:
    def __init__(self, title: str, text: str, icon: QMessageBox.Icon):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.show()
        r = msg_box.exec()


class GnSuccess(Message):
    def __init__(self, title: str, text: str):
        super().__init__(title, text, QMessageBox.Icon.Information)


class GnWarning(Message):
    def __init__(self, title: str, text: str):
        super().__init__(title, text, QMessageBox.Icon.Warning)


class GnCritical(Message):
    def __init__(self, title: str, text: str):
        super().__init__(title, text, QMessageBox.Icon.Critical)
