# -*- coding: UTF-8 -*-
"""Contains GUI-core and all applied logic.
    Run this file to start the app."""

import sys
from pathlib import Path

from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QVBoxLayout,
                               QGridLayout,
                               QLabel,
                               QComboBox,
                               QLineEdit,
                               QWidget,
                               QStackedWidget,
                               QPushButton,
                               QFileDialog)

import app

from app.app_widgets import (Uocns,
                             Booksim,
                             Newxim,
                             Topaz,
                             Dec9,
                             GpNocSim)

from app.messages import (GnSuccess, GnWarning, GnCritical, langs)

from config.style_settings import (Q_MAIN_WINDOW_STYLE,
                                   Q_SIM_COMBO_BOX_WIDTH,
                                   Q_SIM_FILE_NAME_FIELD_WIDTH,
                                   Q_SIM_DIRECTORY_FIELD_WIDTH,
                                   Q_SIM_DIR_BUTTON_WIDTH,
                                   Q_SIM_CREATE_BUTTON_WIDTH)

from app.app_core import Extractor

from config.internationalization import all_languages


class SimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UHLNoCS config generator")
        self.setStyleSheet(Q_MAIN_WINDOW_STYLE)

        # main widgets and layout:
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # combobox with sim types; main chooser:
        self.lang_box = QComboBox(self)
        self.lang_box.addItems(list(all_languages.keys()))
        self.lang_box.setFixedWidth(Q_SIM_COMBO_BOX_WIDTH)

        # combobox with sim types; main chooser:
        self.c_box = QComboBox(self)
        self.c_box.addItems(['uocns',
                             'booksim',
                             'newxim',
                             'topaz',
                             'dec9',
                             'gpNocSim'])
        self.c_box.setFixedWidth(Q_SIM_COMBO_BOX_WIDTH)

        # Button to create file
        self.creation_btn = QPushButton('Create file', self)
        self.creation_btn.setFixedWidth(Q_SIM_CREATE_BUTTON_WIDTH)

        # Button to upload data from file
        self.upload_btn = QPushButton('Upload file', self)
        self.upload_btn.setFixedWidth(Q_SIM_CREATE_BUTTON_WIDTH)

        # up-side layout for sim combo and file-information fields
        upper_layout = QGridLayout()
        upper_layout.addWidget(QLabel('<h3>Select sim:</h3>', self), 0, 0)
        upper_layout.addWidget(self.c_box, 0, 1)
        upper_layout.addWidget(QLabel('<h3>Select language:</h3>', self), 1, 0)
        upper_layout.addWidget(self.lang_box, 1, 1)
        upper_layout.addWidget(self.creation_btn, 2, 0)
        upper_layout.addWidget(self.upload_btn, 2, 1)

        # instances for sim-params parts:
        self.ui_list = [Uocns(), Booksim(), Newxim(), Topaz(), Dec9(), GpNocSim()]

        # bottom-side widget
        self.Stack = QStackedWidget(self)
        for ui in self.ui_list:
            self.Stack.addWidget(ui)

        # compiling main layout from parts
        main_layout.addLayout(upper_layout)
        main_layout.addWidget(self.Stack)
        self.c_box.setCurrentIndex(0)
        self.c_box.currentIndexChanged.connect(self.__index_changed)
        self.lang_box.setCurrentIndex(0)
        app.app_widgets.LANGUAGE = langs[self.lang_box.currentIndex()]
        self.lang_box.currentIndexChanged.connect(self.__language_changed)
        self.creation_btn.clicked.connect(self.__save_info_to_file)
        self.setLayout(main_layout)

    def __index_changed(self):
        self.Stack.setCurrentIndex(self.c_box.currentIndex())

    def __language_changed(self):
        app.app_widgets.LANGUAGE = langs[self.lang_box.currentIndex()]

    def __save_info_to_file(self):
        if self.ui_list[self.c_box.currentIndex()].check_fields():
            options = QFileDialog.Options()
            directory = Path(QFileDialog.getSaveFileName(self, "Выберите файл",
                                                         options=options)[0])

            e = Extractor(directory.stem, dir_=directory)

            sim = self.ui_list[self.c_box.currentIndex()].read_fields()
            json_model = e.to_json(sim.export())
            e.writer(json_model)
            GnSuccess(app.app_widgets.LANGUAGE, "FILE_CREATE")


def main():
    app = QApplication(sys.argv)
    win = SimulatorApp()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
