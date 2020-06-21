import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QSize

from mainwindow import MainWindow

windowSize = QSize(1000, 800)

if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)

    app = MainWindow()
    screen: QScreen = app.screen()
    size: QSize = screen.size()

    app.setGeometry(
        size.width()//2 - windowSize.width()//2,
        size.height()//2 - windowSize.height()//2,
        windowSize.width(),
        windowSize.height(),
    )
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()

