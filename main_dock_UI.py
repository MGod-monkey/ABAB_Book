from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sys import exit, argv


# 重写QLabel，让其能够支持点击事件
class QLabel_Item(QLabel):
    cliecked = pyqtSignal()
    def __init__(self,index,QIcon_no,QIcon_on,text=None,parent=None):
        super(QLabel_Item, self).__init__(parent)
        self.icon_no = QIcon_no # 关闭时的图标
        self.icon_on = QIcon_on # 打开时的图标
        self.is_clieck = True   # 默认鼠标单击为单击事件
        if index != 1:
            self.is_open = False    # 默认为关闭状态
            self.setScaledContents(True)  # 设置图标铺满
            self.setPixmap(QPixmap(QIcon_no))  # 设置默认图标
        else:
            self.is_open = True     # 默认第一个图标为打开状态
            self.setScaledContents(True)  # 设置图标铺满
            self.setPixmap(QPixmap(QIcon_on))  # 设置默认图标
        if index != 3:
            if index > 3:
                _plus = 26
            else:
                _plus = 0
            self.setGeometry(36*index+46*(index-1)+_plus, 26, 46, 46)
            self.bottom_text = QLabel(text, parent)
            self.bottom_text.setFont(QFont('华文新魏', 10))
            self.bottom_text.setAlignment(Qt.AlignCenter)
            self.bottom_text.setGeometry(36*index+46*(index-1)+_plus, 74, 46, 16)
        else:
            self.setScaledContents(True)  # 设置图标铺满
            self.setPixmap(QPixmap(QIcon_no))  # 设置默认图标
            self.setGeometry(200, 20, 72, 72)
            self.setObjectName('play')
            self.setToolTip('点击播放')

    def set_no(self):   # 设置关闭状态
        self.setPixmap(QPixmap(self.icon_no))  # 设置默认图标
        # self.setStyleSheet('background-color:blue')
        self.bottom_text.setStyleSheet('text-decoration:normal;')   # 设置正常

    def set_on(self):   # 设置打开状态
        self.setPixmap(QPixmap(self.icon_on))  # 设置默认图标
        # self.setStyleSheet(f'background-color:red')
        self.bottom_text.setStyleSheet('text-decoration:underline;')    # 设置下滑线

    # 正常情况下鼠标单击为触发事件，点击并移动为移动事件

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_clieck = True
            self.move_xy = event.globalPos() - self.pos()  # 获取鼠标的移动事件
            self.parent_rect = self.parent().pos()

    def mouseMoveEvent(self, event):
        self.is_clieck = False
        # 移动dock栏（dock栏的坐标位置+鼠标的偏移量-控件本身坐标）
        self.parent().move(self.parent_rect + event.globalPos() - self.move_xy - self.pos())
        self.setCursor(QCursor(Qt.OpenHandCursor))  # 设置鼠标为抓手
        self.moved = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(QCursor(Qt.ArrowCursor))  # 设置鼠标为正常
            if self.is_clieck and not self.is_open:
                self.is_open = True
                self.cliecked.emit()
            elif self.is_clieck:
                self.is_open = False
                self.cliecked.emit()
    # 鼠标进入和离开触发图标移动
    def enterEvent(self, event):
        if not self.objectName():
            self.move(self.pos()-QPoint(0,8))
            self.bottom_text.setStyleSheet('font-weight:bold;')
    def leaveEvent(self, event):
        if not self.objectName():
            self.move(self.pos()+QPoint(0,8))
            self.bottom_text.setStyleSheet('font-weight:normal')


# 底部悬浮窗口
class Dock_Win(QWidget):
    def __init__(self, parent=None):
        super(Dock_Win, self).__init__(parent)
        # self.bg_color = QColor(170, 248, 248, 230)  # 设置背警色
        # self.fill_color = QColor(0,250,255,50) # 阴影颜色
        # 获取窗口坐标
        screen_size = QDesktopWidget().geometry()
        win_size = self.geometry()
        self.win_x = int(screen_size.width() / 2 - win_size.width() / 2)
        self.win_y = int(screen_size.height() / 2 - win_size.height() / 2)
        self.move(int(screen_size.width() / 2 - win_size.width() / 2),
                  int(screen_size.height() / 2 - win_size.height() / 2))
        self.initUI()

    def initUI(self):
        # 设置窗口透明，无边框
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        pl = QPalette(QColor(55,255,255,30))
        self.setPalette(pl)
        # 设置窗口的大小
        self.resize(462, 110)
        # 添加item
        self.new_label()
        # 设置提示图标样式
        # self.setStyleSheet('QToolTip {font-family: "华文新魏";font-size: 15px;'
        #                    'color: #BDC8E2;font-style: italic;padding-right: 2px;padding-top: 2px;font-widget: bold;'
        #                    'padding-bottom: 2px;border-style: solid;border-width: 1px;border-color: aqua;border-radius: 13px;'
        #                    'background-color: #2E3648;background-position: left center;}'
        #                    'QLabel_Item {border-radius:10px} #play{border-radius:20px}')

    def new_label(self):
        self.label_search = QLabel_Item(1,'./img/main_UI/dock/search_no.png','./img/main_UI/dock/search_on.png','搜索',parent=self)
        self.label_libaray = QLabel_Item(2,'./img/main_UI/dock/libaray_no.png','./img/main_UI/dock/libaray_on.png','图书馆',parent=self)
        self.label_play = QLabel_Item(3,'./img/main_UI/dock/start_play.png','./img/main_UI/dock/pause_play.png',parent=self)
        self.label_book = QLabel_Item(4,'./img/main_UI/dock/book_no.png','./img/main_UI/dock/book_on.png','小说',parent=self)
        self.label_magazine = QLabel_Item(5,'./img/main_UI/dock/magazine_no.png','./img/main_UI/dock/magazine_on.png','杂志',parent=self)
        self.label_search.cliecked.connect(lambda :self.changeIconStatus(self.label_search))
        self.label_libaray.cliecked.connect(lambda :self.changeIconStatus(self.label_libaray))
        # self.label_play.cliecked.connect(lambda :self.changeIconStatus(self.label_play))
        self.label_book.cliecked.connect(lambda :self.changeIconStatus(self.label_book))
        self.label_magazine.cliecked.connect(lambda :self.changeIconStatus(self.label_magazine))

    def changeIconStatus(self,label):
        label.set_on()
        for i in [self.label_search,self.label_libaray,self.label_book,self.label_magazine]:
            if i != label:
                i.set_no()
    #
    # def changeBgColor(self,text=None):       # 修改背景颜色
    #     # if text == '天空蓝':
    #     #     color = QColor(74,158,255,240)
    #     # elif text == '基佬紫':
    #     #     color = QColor(214,33,255,240)
    #     # elif text == '深林绿':
    #     #     color = QColor(0,255,0,240)
    #     # elif text == '烈焰红':
    #     #     color = QColor(252,0,0,240)
    #     # elif text == '柠檬黄':
    #     #     color = QColor(255,245,36,240)
    #     # else:
    #     color = QColorDialog(self).getColor()
    #     color.setAlpha(230)
    #     self.bg_color = color
    # def changeGhColor(self,text=None):       # 修改光圈颜色
    #     # if text == '天空蓝':
    #     #     color = QColor(74,158,255,240)
    #     # elif text == '烈焰红':
    #     #     color = QColor(255,0,0,240)
    #     # elif text == '柠檬黄':
    #     #     color = QColor(255,245,36,240)
    #     # elif text == '基佬紫':
    #     #     color = QColor(214,33,255,240)
    #     # elif text == '深林绿':
    #     #     color = QColor(0,255,0,240)
    #     # else:
    #     color = QColorDialog(self).getColor()
    #     self.fill_color = color
    # #
    # def contextMenuEvent(self, event):  # 连接菜单事件
    #     # 设置右击菜单
    #     right_menu = QMenu(self)
    #     set_bg_color = QAction('背景色')
    #     right_menu.addAction(set_bg_color)
    #     # tkl_bg_color = QAction('天空蓝')
    #     # lyh_bg_color = QAction('烈焰红')
    #     # mmh_bg_color = QAction('柠檬黄')
    #     # sll_bg_color = QAction('深林绿')
    #     # jlz_bg_color = QAction('基佬紫')
    #     # other_bg_color = QAction('自定义颜色')
    #     # set_bg_color.addAction(tkl_bg_color)
    #     # set_bg_color.addAction(lyh_bg_color)
    #     # set_bg_color.addAction(mmh_bg_color)
    #     # set_bg_color.addAction(sll_bg_color)
    #     # set_bg_color.addAction(jlz_bg_color)
    #     # set_bg_color.addSeparator()  # 添加分隔线
    #     # set_bg_color.addAction(set_bg_color)
    #
    #     # tkl_bg_color.triggered.connect(lambda: self.changeBgColor(tkl_bg_color.text()))
    #     # lyh_bg_color.triggered.connect(lambda: self.changeBgColor(lyh_bg_color.text()))
    #     # mmh_bg_color.triggered.connect(lambda: self.changeBgColor(mmh_bg_color.text()))
    #     # jlz_bg_color.triggered.connect(lambda: self.changeBgColor(jlz_bg_color.text()))
    #     # sll_bg_color.triggered.connect(lambda: self.changeBgColor(sll_bg_color.text()))
    #     set_bg_color.triggered.connect(lambda: self.changeBgColor(''))
    #
    #     set_gh_color = QAction('光圈色')
    #     right_menu.addAction(set_gh_color)
    #     # right_menu.addMenu(set_gh_color)
    #     # tkl_gh_color = QAction('天空蓝')
    #     # lyh_gh_color = QAction('烈焰红')
    #     # mmh_gh_color = QAction('柠檬黄')
    #     # sll_gh_color = QAction('深林绿')
    #     # jlz_gh_color = QAction('基佬紫')
    #     # other_gh_color = QAction('自定义颜色')
    #     # set_gh_color.addAction(tkl_gh_color)
    #     # set_gh_color.addAction(lyh_gh_color)
    #     # set_gh_color.addAction(mmh_gh_color)
    #     # set_gh_color.addAction(sll_gh_color)
    #     # set_gh_color.addAction(jlz_gh_color)
    #     # set_gh_color.addSeparator()  # 添加分隔线
    #     # set_gh_color.addAction(other_gh_color)
    #     #
    #     # tkl_gh_color.triggered.connect(lambda: self.changeGhColor(tkl_gh_color.text()))
    #     # lyh_gh_color.triggered.connect(lambda: self.changeGhColor(lyh_gh_color.text()))
    #     # mmh_gh_color.triggered.connect(lambda: self.changeGhColor(mmh_gh_color.text()))
    #     # jlz_gh_color.triggered.coonnect(lambda: self.changeGhColor(jlz_gh_color.text()))
    #     # sll_gh_color.triggered.connect(lambda: self.changeGhColor(sll_gh_color.text()))
    #     set_gh_color.triggered.connect(lambda: self.changeGhColor(''))
    #     #
    #
    #     exit_menu = QAction('退 出',right_menu)
    #     exit_menu.triggered.connect(right_menu.close)
    #     auto_hide = QAction('自动隐藏')
    #     right_menu.addAction(auto_hide)
    #     right_menu.addSeparator()   # 添加分割符
    #     right_menu.addAction(exit_menu)
    #     if not self.childAt(event.globalPos()-self.pos()):
    #         right_menu.exec_(event.globalPos())


   # # 设置窗口圆角+边框阴影
   #  def paintEvent(self, event):
   #      # # 设置阴影
   #      # painter_path = QPainterPath()
   #      # painter_path.setFillRule(Qt.WindingFill)
   #      #
   #      # painter = QPainter(self)
   #      # painter.setRenderHint(QPainter.Antialiasing)
   #      # painter.fillPath(painter_path, QBrush(Qt.white))
   #      # for i in range(10):
   #      #     i_path = QPainterPath()
   #      #     i_path.setFillRule(Qt.WindingFill)
   #      #     ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
   #      #     i_path.addRoundedRect(ref, 20, 20)
   #      #     self.fill_color.setAlpha(int(150 - i ** 0.5 * 50))
   #      #     painter.setPen(self.fill_color)
   #      #     painter.drawPath(i_path)
   #
   #      # 圆角
   #      painter_rect = QPainter()
   #      painter_rect.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
   #      painter_rect.setBrush(QColor(255,255,255,200))
   #      painter_rect.setOpacity(0.5)
   #      painter_rect.setPen(Qt.transparent)
   #
   #      _rect = self.rect()
   #      # _rect.setLeft(15)
   #      # _rect.setTop(15)
   #      _rect.setWidth(_rect.width() - 15)
   #      _rect.setHeight(_rect.height() - 15)
   #      painter_rect.begin(self)
   #      painter_rect.drawRoundedRect(_rect, 15, 15)
   #      painter_rect.end()

    # 设置窗口移动事件
    # 当鼠标左击并且移动时触发窗口移动事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_move = True
            self.move_xy = event.globalPos() - self.pos()  # 获取鼠标的移动事件
            # self.parent_rect = self.parent().pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 设置鼠标为抓手

    def mouseMoveEvent(self, event):
        if self.is_move:
            # 移动dock栏（dock栏的坐标位置+鼠标的偏移量-dock栏的边框位置）
            self.move(event.globalPos() - self.move_xy)

    def mouseReleaseEvent(self, event):
        self.is_move = False
        self.setCursor(QCursor(Qt.ArrowCursor))  # 设置鼠标为正常


app = QApplication(argv)
dock = Dock_Win()
dock.show()
exit(app.exec_())