from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def clicked():
    print("DOWNLOAD")

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle('Youtube downloader')

    label = QtWidgets.QLabel(win)
    label.setText("Hello there!")
    label.move(50,50)

    b1 = QtWidgets.QPushButton(win)
    b1.setText("Download")
    b1.move(100,100)
    b1.clicked.connect(clicked)

    win.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    window()
