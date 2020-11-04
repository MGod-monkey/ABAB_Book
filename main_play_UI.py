from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget, QColorDialog,QMenu,QAction,QSlider
from PyQt5.QtGui import QFont, QPainterPath, QPainter, QBrush, QColor, QCursor, QPixmap
from PyQt5.QtCore import Qt, QRectF, pyqtSignal,QPoint
from sys import exit, argv


class Play_Button_1(QLabel):
    cliecked = pyqtSignal()
    def __init__(self,parent=None,status_no=None):
        super(Play_Button_1, self).__init__(parent)
        self.status_no = status_no
        self.setPixmap(QPixmap(status_no))
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.cliecked.emit()




class Play_Button_2(QLabel):
    cliecked = pyqtSignal(str)

    def __init__(self, parent=None, start_ico=None, pause_ico=None):
        super(Play_Button_2, self).__init__(parent)
        self.start_ico = start_ico
        self.pause_ico = pause_ico
        self.setPixmap(QPixmap(start_ico))
        self.setScaledContents(True)
        self.status = 'play'

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.status == 'play':
                self.setPixmap(QPixmap(self.pause_ico))
                self.cliecked.emit(self.status)        # 发送一个开始播放的信号
                self.status = 'pause'
            else:
                self.setPixmap(QPixmap(self.start_ico))
                self.cliecked.emit(self.status)     # 否则发送暂停信号
                self.status = 'play'

class Play_Button_3(QLabel):
    cliecked = pyqtSignal(int)
    def __init__(self,parent=None,play_mode_1=None,play_mode_2=None,play_mode_3=None,play_mode_4=None):
        super(Play_Button_3, self).__init__(parent)
        self.play_mode_ico = [play_mode_1,play_mode_2,play_mode_3,play_mode_4]  # 顺序播放,随机播放，循环播放，单曲播放
        self.play_mode = 0  # 当前播放模式
        self.setPixmap(QPixmap(self.play_mode_ico[self.play_mode]))
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        self.play_mode = (self.play_mode+1) % 4
        self.setPixmap(QPixmap(self.play_mode_ico[self.play_mode]))
        self.cliecked.emit(self.play_mode)


class Play_Win(QWidget):
    def __init__(self,parent=None):
        super(Play_Win,self).__init__(parent)
        self.bg_color = QColor(111,249,193, 240)  # 设置背警色
        # 设置窗口透明，无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)
        # qss美化 border：边框   bored-radius:边框圆角（过大会恢复原样）
        # margin：内边距
        # QSlider：：handle：horizontal水平拖动柄
        # QSlider::groove:horizontal 进度条
        # QSlider：：add-page：未选择部分
        # QSlider：：sub-page：已选择部分
        self.setStyleSheet('Play_Button_1#sound:hover{background: #439777;border-radius:15px;}'
                           'Play_Button_1:hover{background: #439777;border-radius:25px;}'
                           'Play_Button_2:hover{background: #439777;border-radius:30px}'
                           'Play_Button_3:hover{background: #439777}'
                           'QToolTip {font-size: 15px;'
                           'color: break;font-style: italic;padding-right: 2px;padding-top: 2px;font-widget: bold;'
                           'padding-bottom: 2px;border-style: solid;border-width: 1px;border-color: aqua;border-radius: 13px;'
                           'background-color: #6ff9c1;background-position: left center;}'
                           'QSlider::handle:horizontal{width:10px;background-color:rgb(255,255,255);margin:-2px 0px -2px 0px;border-radius:4px;}'
                        'QSlider::groove:horizontal{height:4px;background-color:rgb(219,219,219)}'
                        'QSlider::groove:horizontal:hover{height:6px;background-color:rgb(219,219,219)}'
                        'QSlider::add-page:horizontal{background-color:rgb(219,219,219);}'
                         'QSlider::sub-page:horizontal{background-color:rgb(236,65,65);}')
        self.initUI()

    def initUI(self):
        self.resize(420,300)

        # 添加唱片组件
        cp_comp1 = QLabel(self)
        cp_comp1.setPixmap(QPixmap('./img/main_UI/play/play_cp_comp1.png'))
        cp_comp1.setScaledContents(True)    # 设置铺满
        cp_comp1.setGeometry(40,40,150,150)
        cp_comp2 = QLabel(self)
        cp_comp2.setPixmap(QPixmap('./img/main_UI/play/play_cp_comp2.png'))
        cp_comp2.setScaledContents(True)  # 设置铺满
        cp_comp2.setGeometry(110, 0, 80, 40)

        # 添加按钮组件
        last_button = Play_Button_1(self,'./img/main_UI/play/last_no.png')
        last_button.setToolTip('上一首')
        last_button.setGeometry(110,223,50,50)
        play_button = Play_Button_2(self,'./img/main_UI/play/start.png','./img/main_UI/play/pause.png')
        play_button.setGeometry(180,218,60,60)
        next_button = Play_Button_1(self, './img/main_UI/play/next_no.png')
        next_button.setToolTip('下一首')
        next_button.setGeometry(260, 223, 50, 50)
        play_mode = Play_Button_3(self,'./img/main_UI/play/seq_play.png','./img/main_UI/play/random_play.png',
                                  './img/main_UI/play/loop_play.png','./img/main_UI/play/only_play.png')
        play_mode.setGeometry(20,238,30,30)
        sound_eff = Play_Button_1(self, './img/main_UI/play/sound_ef.png')
        sound_eff.setGeometry(62,238,30,30)
        sound_eff.setObjectName('sound')
        volunme = Play_Button_1(self,'./img/main_UI/play/volume.png')
        volunme.setGeometry(328,238,30,30)
        song_sheet = Play_Button_1(self, './img/main_UI/play/song_sheet.png')
        song_sheet.setGeometry(370,238,30,30)

        # 歌曲信息展示区
        song_message = QLabel(self)
        song_message.setText('<style><div>text-align:center</div></style><p><font size=4><b>聆听世界的声音</b></font></p>'
                             '<pre><font size=2>歌手:</font><a href="https://www.baidu.com"><font size=2>百度</font></a>'
                             '<font size=2>  歌单:</font><a href="https://www.baidu.com"><font size=2>我的喜欢</font></a></pre>')
        song_message.setOpenExternalLinks(True)
        song_message.setGeometry(230,10,160,70)

        song_lcy = QLabel(self)
        song_lcy.setText('<font size=4>歌词功能<br>待开发中···</font>')
        song_lcy.setGeometry(245,110,120,50)

        # 进度条
        song_slider = QSlider(Qt.Horizontal,self)   # 设置水平进度条
        song_slider.setGeometry(80,280,260,18)
        alr_time = QLabel('00:00',self)     # 已播放时长
        alr_time.setGeometry(33,278,40,20)
        all_time = QLabel('00:00',self)
        all_time.setGeometry(347,278,40,20)

    # 设置窗口圆角+边框阴影
    def paintEvent(self, event):
        # 圆角
        painter_rect = QPainter(self)
        painter_rect.setRenderHint(QPainter.Antialiasing,True)  # 抗锯齿
        painter_rect.setBrush(self.bg_color)   # 设置笔刷颜色
        painter_rect.setPen(Qt.transparent)
        painter_rect.begin(self)
        painter_rect.drawRoundedRect(self.rect(),15,15)
        painter_rect.end()

        # 绘制底部样式
        play_bottom = self.rect()
        play_bottom.setTop(210)
        play_bottom.setHeight(90)
        painter_bottom = QPainter(self)
        painter_bottom.setRenderHint(QPainter.Antialiasing,True)    # 抗锯齿
        painter_bottom.setBrush(QColor(9,220,135,255))
        painter_bottom.begin(self)
        painter_bottom.drawRoundedRect(play_bottom,15,15)
        painter_bottom.end()





app = QApplication(argv)
play = Play_Win()
play.show()
exit(app.exec_())
