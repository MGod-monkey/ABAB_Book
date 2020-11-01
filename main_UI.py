from PyQt5.QtWidgets import QApplication,QDockWidget,QMainWindow,QListView,QGridLayout,QHBoxLayout,QApplication,QAbstractItemView,QMainWindow, QDesktopWidget,QListWidget,QListWidgetItem,QLabel,QStackedWidget, QLineEdit, QWidget,QPushButton,QMessageBox,QCheckBox,QDialog
from PyQt5.QtGui import QIcon,QFont,QBitmap,QPainterPath,QPainter,QBrush,QColor,QCursor,QMouseEvent,QPixmap
from PyQt5.QtCore import Qt,QSize,QAbstractItemModel,QRectF,QPoint
from sys import argv
from time import sleep

# 底部悬浮窗口
class Dock_Win(QWidget):
    def __init__(self):
        super(Dock_Win, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口透明，无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        # # # 获取窗口坐标并居中
        # screen_size = QDesktopWidget().geometry()
        # win_size = self.geometry()
        # self.win_x = int(screen_size.width() / 2 - win_size.width() / 2)
        # self.win_y = int(screen_size.height() / 2 - win_size.height() / 2)
        # self.move(int(screen_size.width() / 2 - win_size.width() / 2),
        #           int(screen_size.height() / 2 - win_size.height() / 2))
        # 设置窗口的大小
        self.resize(462,100)

        self.new_label()
        # self.item_search = (self,'./img/main_UI/search_no.png',(64,64),'调查')
        # self.setStyleSheet('QLabel{background-color: rgba(70,248,248,240)}')

    def new_label(self):
        label_search_icon = QLabel(self)
        label_search_icon.setPixmap(QPixmap('./img/main_UI/dock/search_no.png'))
        label_search_icon.setScaledContents(True)
        label_search_icon.setGeometry(36,20,46,46)
        label_search_text = QLabel('调查',self)
        label_search_text.setFont(QFont('华文新魏', 10))
        label_search_text.setGeometry(36,68,46,16)
        label_search_text.setAlignment(Qt.AlignCenter)
        label_libaray_icon = QLabel(self)
        label_libaray_icon.setPixmap(QPixmap('./img/main_UI/dock/libaray_no.png'))
        label_libaray_icon.setScaledContents(True)
        label_libaray_icon.setGeometry(118, 20, 46, 46)
        label_libaray_text = QLabel('图书馆',self)
        label_libaray_text.setFont(QFont('华文新魏', 10))
        label_libaray_text.setGeometry(118,68,46,16)
        label_libaray_text.setAlignment(Qt.AlignCenter)
        label_play = QLabel(self)
        label_play.setPixmap(QPixmap('./img/main_UI/dock/start_play.png'))
        label_play.setScaledContents(True)
        label_play.setGeometry(200,20,62,62)
        label_play.setToolTip('点击播放')
        label_book_icon = QLabel(self)
        label_book_icon.setPixmap(QPixmap('./img/main_UI/dock/book_no.png'))
        label_book_icon.setScaledContents(True)
        label_book_icon.setGeometry(298, 20, 46, 46)
        label_book_text = QLabel('小说',self)
        label_book_text.setFont(QFont('华文新魏', 10))
        label_book_text.setGeometry(298,68,46,16)
        label_book_text.setAlignment(Qt.AlignCenter)
        label_magazine_icon = QLabel(self)
        label_magazine_icon.setPixmap(QPixmap('./img/main_UI/dock/magazine_no.png'))
        label_magazine_icon.setScaledContents(True)
        label_magazine_icon.setGeometry(380,20,46,46)
        label_magazine_text = QLabel('杂志',self)
        label_magazine_text.setFont(QFont('华文新魏', 10))
        label_magazine_text.setGeometry(380, 68, 46, 16)
        label_magazine_text.setAlignment(Qt.AlignCenter)



    # 设置窗口圆角+边框阴影
    def paintEvent(self,event):
        # 设置阴影
        painter_path = QPainterPath()
        painter_path.setFillRule(Qt.WindingFill)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(painter_path,QBrush(Qt.white))
        # 阴影颜色
        color = QColor(0,250,255,50)
        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10-i,10-i,self.width()-(10-i)*2,self.height()-(10-i)*2)
            i_path.addRoundedRect(ref,20,20)
            color.setAlpha(150-i**0.5*50.0)
            painter.setPen(color)
            painter.drawPath(i_path)

        # 圆角
        painter_rect = QPainter(self)
        painter_rect.setRenderHint(QPainter.Antialiasing)   # 抗锯齿
        color_bg = QColor(170,248,248,240)  # 设置背警色
        painter_rect.setBrush(color_bg)
        painter_rect.setPen(Qt.transparent)

        self._rect = self.rect()
        self._rect.setLeft(15)
        self._rect.setTop(15)
        self._rect.setWidth(self._rect.width()-15)
        self._rect.setHeight(self._rect.height()-15)
        painter_rect.drawRoundedRect(self._rect,15,15)

    # 设置窗口移动事件
    # 当鼠标左击并且移动时触发窗口移动事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_move = True
            self.move_xy = event.globalPos() - self.pos()  # 获取鼠标的移动事件
            # self.parent_rect = self.parent().pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 设置鼠标为抓手

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_move:
            # 移动dock栏（dock栏的坐标位置+鼠标的偏移量-dock栏的边框位置）
            self.move(event.globalPos() - self.move_xy)

    def mouseReleaseEvent(self, event):
        self.is_move = False
        self.setCursor(QCursor(Qt.ArrowCursor))  # 设置鼠标为正常


class Main_UI(QMainWindow):
    def __init__(self):
        super(Main_UI,self).__init__()

        self.init_UI()
        # 创建登录界面的UI实例
    def init_UI(self):
        self.setWindowTitle('ABAB阅读器')
        self.resize(900,600)
        # 获取窗口坐标并居中
        screen_size = QDesktopWidget().geometry()
        win_size = self.geometry()
        self.win_x = int(screen_size.width() / 2 - win_size.width() / 2)
        self.win_y = int(screen_size.height() / 2 - win_size.height() / 2)
        self.move(int(screen_size.width() / 2 - win_size.width() / 2),
                  int(screen_size.height() / 2 - win_size.height() / 2))




app = QApplication(argv)
# test_win = Main_UI()
# test_win.show()
dock_win = Dock_Win()
dock_win.show()
exit(app.exec_())

