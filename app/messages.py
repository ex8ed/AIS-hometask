from PySide6.QtWidgets import QMessageBox
from config.internationalization import all_languages


class Message:
    def __init__(self, lang: str, title: str, tag: str, icon: QMessageBox.Icon):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(all_languages[lang][tag])
        msg_box.show()
        r = msg_box.exec()


class GnSuccess(Message):
    def __init__(self, lang: str, tag: str):
        super().__init__(lang, all_languages[lang]["SUCCESS"], tag, QMessageBox.Icon.Information)


class GnWarning(Message):
    def __init__(self, lang: str, tag: str):
        super().__init__(lang, all_languages[lang]["WARNING"], tag, QMessageBox.Icon.Warning)


class GnCritical(Message):
    def __init__(self, lang: str, tag: str):
        super().__init__(lang, all_languages[lang]["ERROR"], tag, QMessageBox.Icon.Critical)


# lang-box-keys:

langs = {0: 'ru',
         1: 'en'}
