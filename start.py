from sys import exit,argv
from PyQt5.QtWidgets import QApplication
from login_UI import Login_Window
from main_UI import Main_UI

if __name__ == '__main__':
    app = QApplication(argv)
    main_win = Main_UI()    # 创建主窗口实例
    login_win = Login_Window(main_win)
    exit(app.exec_())