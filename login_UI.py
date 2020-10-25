from PyQt5.QtWidgets import QMainWindow, QDesktopWidget,  QLabel, QLineEdit, QWidget,QPushButton,QMessageBox,QCheckBox,QDialog
from PyQt5.QtGui import QFont,QRegExpValidator,QMovie,QPixmap
from PyQt5.QtCore import Qt, QRect, pyqtSignal,QRegExp,QTimer
from guet_VPN import Guet_VPN
from sys import exit


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

# 加载动画的窗口
class Loading_Win(QDialog):
    def __init__(self):
        super(Loading_Win, self).__init__()
        self.initUI()
    def initUI(self):
        # 设置窗口基础类型
        self.resize(250,250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # 无边框|对画框|置顶
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 加载动画画面
        self.loading_gif = QMovie('./img/loading_b.gif')
        self.loading_label = QLabel(self)
        self.loading_label.setMovie(self.loading_gif)
        # self.loading_label.setGeometry(QRect(0,0,250,250))
        self.loading_gif.start()

# # 重写标签的鼠标按钮事件
# class Login_Label(QLabel):
#     clicked = pyqtSignal()
#     def __init__(self, parent=None):
#         super(Login_Edit, self).__init__(parent)
#     def mouseReleaseEvent(self, QMouseEvent):
#         if QMouseEvent.button() == Qt.LeftButton:
#             self.clicked.emit()

class Login_Window(QMainWindow):
    def __init__(self,mainWindow):
        super(Login_Window, self).__init__()
        self.initUI()
        self.mainWindow = mainWindow

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
        # 创建加载动画窗口
        self.loading_win = Loading_Win()
        self.loading_win.hide() # 隐藏加载窗口

        # 编辑窗口背景图
        self.setObjectName('login_UI')
        self.setStyleSheet("#login_UI{border-image:url(./img/login_UI/login_bg1.png)}")

        # 图片切换
        # 计时器，3秒换一张图
        self.png_num = 1
        self.png = QLabel(self)
        self.png.setScaledContents(True)    # 设置照片全照
        self.png.setGeometry(QRect(22, 25, 330, 498))
        self.timer = QTimer()
        self.timer.start(3000)
        self.timer.timeout.connect(self.changePNG)

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
        self.passwd_lineEdit.editingFinished.connect(self.login)
        self.passwd_lineEdit.textEdited.connect(self.clearWarn)
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
        forget_lab.setText('已有账号，但<a href="https://cas.guet.edu.cn:4102/#/password/passwordFound">忘记密码?</a>')
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
        self.passwd_warn = QLabel('<font color=red><b>账号或密<br>码错误</b></font>',self)
        self.passwd_warn.setGeometry(QRect(786,265,65,60))
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
        # 设置登录按钮的槽函数
        login_btn.clicked.connect(self.login)

        # 不需要vpn账号登录
        self.not_vpn = QCheckBox(self)
        self.not_vpn.setGeometry(QRect(780,380,150,50))
        self.not_vpn.setText('我正在使\n用校园网')

    # 切换233娘遮掩动作
    def changeBG_1(self):
        self.setStyleSheet("#login_UI{border-image:url(./img/login_UI/login_bg.png)}")
        if len(self.id_lineEdit.text())==0:
            self.id_warn1.setVisible(True)
        else:
            self.id_warn1.setVisible(False)
    def changeBG_2(self):
        self.setStyleSheet("#login_UI{border-image:url(./img/login_UI/login_bg1.png)}")

    # 切换图片
    def changePNG(self):
        if self.png_num == 4:
            self.png.setPixmap(QPixmap("./img/login_UI/play_" + str(self.png_num) + '.png'))
            self.png_num = 1
        else:
            self.png.setPixmap(QPixmap("./img/login_UI/play_" + str(self.png_num) + '.png'))
            self.png_num += 1

    # 编辑框不规范提醒
    def isWarning(self):
        # 当id输入框的长度大于10
        if len(self.id_lineEdit.text()) > 0:
            self.id_warn1.setVisible(False)
        elif len(self.id_lineEdit.text()) > 10:
            self.id_warn.setVisible(True)
        else:
            self.id_warn.setVisible(False)

    # 当密码错误或为空时，再次编辑密码会重新清除错误提示
    def clearWarn(self):
        self.passwd_warn.setVisible(False)
        self.passwd_warn1.setVisible(False)

    # 重写主窗口移动事件,当主窗口移动时，加载界面对应的移动
    def moveEvent(self,moveEvent):
        move_x = moveEvent.pos().x()+340
        move_y = moveEvent.pos().y()+155
        self.loading_win.move(move_x,move_y)
        # self.png.move(move_x-318,move_y-130)
    # 重写窗口关闭事件，当主窗口关闭时子窗口也会关闭
    def closeEvent(self,closeEvent):
        exit(0)

    # 登录按钮的槽函数
    def login(self):
        if self.not_vpn.isChecked() == False:
            # 获取编辑框数据之使用vpn账号
            user_id = self.id_lineEdit.text()
            user_passwd = self.passwd_lineEdit.text()
            # 判断编辑框是否有数值，当没有时，则
            if user_id:         # 输入账号时
                if user_passwd: # 输入密码时
                    guet_vpn = Guet_VPN(username=user_id,password=user_passwd)
                    # 登录失败时
                    if guet_vpn.login_result == 'false':
                        self.loading_win.close()
                        self.id_lineEdit.clear()    # 清除账号框
                        self.passwd_lineEdit.clear()    # 清空密码框
                        self.passwd_warn.setVisible(True)   # 设置密码错误提示
                        self.id_lineEdit.setFocus(True) # 设置密码框为选中状态
                    # 登录成功
                    else:
                        # 加载动画页面
                        self.loading_win.show()
                        self.setWindowOpacity(0.9)
                # 无密码时提示输入密码
                else:
                    self.passwd_lineEdit.setFocus(True)  # 设置密码框为选中状态
                    self.passwd_warn1.setVisible(True)
            else:   # 当不输入任何值时使用默认账号
                res = QMessageBox.information(self,'提醒','您正在使用软件内置的账号，请文明使用该账号!!!',QMessageBox.Ok|QMessageBox.Cancel)
                if res == QMessageBox.Ok:
                    # 登录加载动画
                    guet_vpn = Guet_VPN()
                    if guet_vpn.login_result == 'false':
                        self.id_lineEdit.clear()
                        self.passwd_lineEdit.clear()
                        QMessageBox.information(self,'错误','默认账号出错，联系作者修改账号信息！',QMessageBox.Ok)
                    else:
                        self.loading_win.show()
                        self.setWindowOpacity(0.9)
        # 不使用vpn登录
        else:
            # self.setWindowModality(Qt.WindowModal) # 设置登录界面不可选中
            # if self.mainWindow.show():
            pass
