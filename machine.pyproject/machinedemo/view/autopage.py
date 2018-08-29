
from PyQt5.QtWidgets import QApplication,QWidget,QDialog,QMessageBox
from PyQt5 import uic

from PyQt5 import QtCore

import sys


class AutoPage(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('autopage.ui', self)

        self.pushButton_start.clicked.connect(self.pushButton_clicked)

        self.show()
        pass

    def pushButton_clicked(self):

        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            print('No clicked.')


if __name__ == '__main__':

    app = QApplication(sys.argv)

    auto = AutoPage()

    sys.exit(app.exec_())
    pass
