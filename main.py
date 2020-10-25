from login_UI import Login_Window
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtGui import QIcon
from sys import argv

if __name__ == '__main__':
    app = QApplication(argv)
    app.setWindowIcon(QIcon('./img/ABAB阅读器.png'))
    mainWindow = QMainWindow()
    login_window = Login_Window(mainWindow)
    login_window.show()
    exit(app.exec_())