

from machinedemo.view.autopage import *
from machinedemo.view.testpage import TestPage
from machinedemo.view.manualpage import ManualPage

from PyQt5.QtWidgets import QWidget


class MainWindow(QWidget):
    autopage = AutoPage()
    testpage = TestPage()
    manualpage = ManualPage()
    #window = QWidget()

    def __init__(self):

        super(QWidget,self).__init__()
        pass