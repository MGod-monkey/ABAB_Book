from PyQt5.QtWidgets import QMainWindow, QDesktopWidget,  QLabel, QLineEdit, QWidget,QPushButton
from PyQt5.QtGui import QFont,QRegExpValidator
from PyQt5.QtCore import Qt, QRect, pyqtSignal,QRegExp

# 登录界面
# https://v.guet.edu.cn/do-login
# 重写输入框的鼠标点击事件
class Login_Edit(QLineEdit):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super(Login_Edit, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

# # 重写标签的鼠标按钮事件
# class Login_Label(QLabel):
#     clicked = pyqtSignal()
#     def __init__(self, parent=None):
#         super(Login_Edit, self).__init__(parent)
#     def mouseReleaseEvent(self, QMouseEvent):
#         if QMouseEvent.button() == Qt.LeftButton:
#             self.clicked.emit()

class Login_Window(QMainWindow):
    def __init__(self):
        super(Login_Window, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口样式
        self.setWindowFlag(Qt.WindowTitleHint)
        self.setWindowTitle('ABAB阅读器')
        # 设置窗口最小尺度
        self.setMinimumSize(900, 540)
        self.setMaximumSize(900, 540)
        # 获取窗口坐标
        screen_size = QDesktopWidget().geometry()
        win_size = self.geometry()
        self.win_x = int(screen_size.width() / 2 - win_size.width() / 2)
        self.win_y = int(screen_size.height() / 2 - win_size.height() / 2)
        self.move(int(screen_size.width() / 2 - win_size.width() / 2),
                  int(screen_size.height() / 2 - win_size.height() / 2))

        # 编辑窗口背景图
        self.setObjectName('login_UI')
        self.setStyleSheet("#login_UI{border-image:url(./img/login_UI/login_bg1.png)}")

        # 登录框组件
        widget = QWidget(self)
        widget.setGeometry(QRect(500, 145, 300, 500))
        # 标签控件
        id_lab = QLabel('账号:', widget)
        id_lab.setFont(QFont('华文新魏', 14))
        id_lab.setGeometry(20, 3, 70, 50)
        passwd_lab = QLabel('密码:', widget)
        passwd_lab.setGeometry(20, 125, 70, 50)
        passwd_lab.setFont(QFont('华文新魏', 14))
        # 输入框
        self.id_lineEdit = Login_Edit(widget)
        self.passwd_lineEdit = Login_Edit(widget)
        # 设置输入框的提示文本
        self.id_lineEdit.setPlaceholderText('请输入账号')
        self.passwd_lineEdit.setPlaceholderText('请输入密码')
        # 设置输入框的清除按钮
        self.id_lineEdit.setClearButtonEnabled(True)
        self.passwd_lineEdit.setClearButtonEnabled(True)
        # 设置绝对位置
        self.id_lineEdit.setGeometry(75, 13, 180, 30)
        self.passwd_lineEdit.setGeometry(75, 135, 180, 30)
        # 设置输入框的点击信号
        self.id_lineEdit.clicked.connect(self.changeBG_2)
        self.passwd_lineEdit.clicked.connect(self.changeBG_1)
        # 设置密码框的回显模式
        self.passwd_lineEdit.setEchoMode(QLineEdit.Password)
        # 设置校验器显示文本输入
        reg1 = QRegExp('[0-9]{18}$')
        reg1validation = QRegExpValidator()
        reg1validation.setRegExp(reg1)
        self.id_lineEdit.setValidator(reg1validation)
        self.id_lineEdit.textChanged.connect(self.isWarning)
        # self.passwd_lineEdit.textChanged(self.login)
        # self.passwd_lineEdit.editingFinished(self.login)
        # 密码只能有字母,数字，符号
        reg = QRegExp('[0-9A-Za-z!-/ -@]{18}$')
        regexpvalidation = QRegExpValidator()
        regexpvalidation.setRegExp(reg)
        self.passwd_lineEdit.setValidator(regexpvalidation)

        # 协议标签
        accord_lab = QLabel(self)
        accord_lab.setGeometry(QRect(510, 480, 300, 30))
        accord_lab.setText('登录即代表你同意<a href="https://www.bilibili.com/protocal/licence.html">用户协议</a>'
                           '和<a href="https://www.bilibili.com/blackboard/privacy-pc.html">隐私政策</a>')
        # 设置标签能打开超文本
        accord_lab.setOpenExternalLinks(True)
        # 注册，忘记密码标签
        forget_lab = QLabel(self)
        forget_lab.setGeometry(QRect(620,326,160,30))
        forget_lab.setText('已有账号，但<a href="https://o8.cn/X0uGQu">忘记密码?</a>')
        forget_lab.setOpenExternalLinks(True)
        reg_lab = QLabel(self)
        reg_lab.setGeometry(QRect(520,326,60,30))
        reg_lab.setText('<a href="https://o8.cn/Dj7Ucl">注册账号</a>')
        reg_lab.setOpenExternalLinks(True)

        # 编辑框不规范输入提示
        self.id_warn = QLabel('<font color=red><b>账号过长</b></font>',self)
        self.id_warn.setGeometry(QRect(785,160,65,30))
        self.id_warn.setVisible(False)
        self.id_warn1 = QLabel('<font color=red><b>账号不能为空</b></font>', self)
        self.id_warn1.setGeometry(QRect(785, 160, 95, 30))
        self.id_warn1.setVisible(False)
        self.passwd_warn = QLabel('<font color=red><b>密码错误</b></font>',self)
        self.passwd_warn.setGeometry(QRect(785,283,65,30))
        self.passwd_warn.setVisible(False)
        self.passwd_warn1 = QLabel('<font color=red><b>密码不能为空</b></font>', self)
        self.passwd_warn1.setGeometry(QRect(785, 283, 95, 30))
        self.passwd_warn1.setVisible(False)

        # 登录与注册按钮
        login_btn = QPushButton('登       录',self)
        #7,188,252
        login_btn.setStyleSheet('background-color: rgb(7, 188, 252);')
        # 设置按钮文本
        login_btn.setFont(QFont('华文新魏',14))
        # 设置按钮的绝对位置
        login_btn.setGeometry(QRect(520,385,240,40))


    # 切换233娘遮掩动作
    def changeBG_1(self):
        self.setStyleSheet("#login_UI{border-image:url(./img/login_UI/login_bg.png)}")
        if len(self.id_lineEdit.text())==0:
            self.id_warn1.setVisible(True)
        else:
            self.id_warn1.setVisible(False)
    def changeBG_2(self):
        self.setStyleSheet("#login_UI{border-image:url(./img/login_UI/login_bg1.png)}")

    # 编辑框不规范提醒
    def isWarning(self):
        # 当id输入框的长度大于10
        if len(self.id_lineEdit.text()) > 0:
            self.id_warn1.setVisible(False)
        elif len(self.id_lineEdit.text()) > 10:
            self.id_warn.setVisible(True)
        else:
            self.id_warn.setVisible(False)


