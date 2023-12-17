# -*- coding: UTF-8 -*-
"""Contains GUI-core and all applied logic.
    Run this file to start the app."""

import sys
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

from app.app_widgets import (Uocns,
                             Booksim,
                             Newxim,
                             Topaz,
                             Dec9,
                             GpNocSim,
                             GnCritical,
                             show_msg_success_box)

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
        main_layout.addStretch()

        # combobox with sim types; main chooser:
        # self.c_box = QComboBox(self)
        # self.c_box.addItems(list(all_languages.keys()))

        # combobox with sim types; main chooser:
        self.c_box = QComboBox(self)
        self.c_box.addItems(['uocns',
                             'booksim',
                             'newxim',
                             'topaz',
                             'dec9',
                             'gpNocSim'])
        self.c_box.setFixedWidth(Q_SIM_COMBO_BOX_WIDTH)

        # lineedit with name of file. (By default writes as JSON)
        self.file_name = QLineEdit(self)
        self.file_name.setFixedWidth(Q_SIM_FILE_NAME_FIELD_WIDTH)

        # Lineedit for directory
        self.directory_name = QLineEdit(self)
        self.directory_name.setFixedWidth(Q_SIM_DIRECTORY_FIELD_WIDTH)

        # Button to choose directory via system
        self.directory_btn = QPushButton('...', self)
        self.directory_btn.setFixedWidth(Q_SIM_DIR_BUTTON_WIDTH)

        # Button to create file
        self.creation_btn = QPushButton('Create file', self)
        self.creation_btn.setFixedWidth(Q_SIM_CREATE_BUTTON_WIDTH)

        # up-side layout for sim combo and file-information fields
        upper_layout = QGridLayout()
        upper_layout.addWidget(QLabel('<h3>Select sim:</h3>', self), 0, 1)
        upper_layout.addWidget(self.c_box, 0, 2)
        upper_layout.addWidget(QLabel('<h3>Name of file:</h3>', self), 0, 3)
        upper_layout.addWidget(self.file_name, 0, 4)
        upper_layout.addWidget(QLabel('<h3>Choose directory:</h3>', self), 1, 1)
        upper_layout.addWidget(self.directory_name, 1, 2)
        upper_layout.addWidget(self.directory_btn, 1, 3)
        upper_layout.addWidget(self.creation_btn, 1, 4)

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
        self.directory_btn.clicked.connect(self.__choose_directory)
        self.creation_btn.clicked.connect(self.__save_info_to_file)
        self.setLayout(main_layout)

    def __index_changed(self):
        self.Stack.setCurrentIndex(self.c_box.currentIndex())

    def __choose_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Выберите директорию", self.directory_name.text(),
                                                     options=options)
        if directory:
            self.directory_name.setText(directory)

    def __save_info_to_file(self):
        if self.file_name.text() == "":
            GnCritical("Ошибка!", 'Имя файла не может быть пустым!')
            return

        if self.directory_name == "":
            GnCritical("Ошибка!", 'Имя директории не может быть пустым!')
            return

        e = Extractor(self.file_name.text(), dir_=self.directory_name.text()+'/')

        sim = self.ui_list[self.c_box.currentIndex()].read_fields()
        json_model = e.to_json(sim.export())
        e.writer(json_model)
        show_msg_success_box('Успех!', 'Файл успешно записан!')


def main():
    app = QApplication(sys.argv)
    win = SimulatorApp()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
