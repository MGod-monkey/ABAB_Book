from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from Spider.music_Spider import Could_Music,handle_text,load_local_json,parse_lrc             # 为了该模块的整洁，部分函数转到了music_Spider库
from sys import exit, argv
import player_IMG   # 导入图片资源
from cgitb import enable

enable(format='text')   # 解决pyqt5异常就进去事件处理


"""
重写QLabel，让其支持点击事件
QLabel_1:单状态按钮
QLabel_2:双状态按钮
QLabel_3:多状态按钮
"""
class Play_Button_1(QLabel):
    cliecked = pyqtSignal()
    def __init__(self,parent=None,init_ico=None,init_status=None):
        super(Play_Button_1, self).__init__(parent)
        self.init_ico = init_ico
        self.status = init_status
        self.setPixmap(QPixmap(init_ico))
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.status = not self.status
            self.cliecked.emit()
class Play_Button_2(QLabel):
    cliecked = pyqtSignal()
    def __init__(self, parent=None, true_ico=None, false_ico=None,init_status=None):
        super(Play_Button_2, self).__init__(parent)
        self.true_ico = true_ico
        self.false_ico = false_ico
        self.status = init_status
        self.setScaledContents(True)
        self.changeStatus()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.cliecked.emit()
    def changeStatus(self):
        if self.status:
            self.setPixmap(QPixmap(self.true_ico))
        else:
            self.setPixmap(QPixmap(self.false_ico))

class Play_Button_3(QLabel):
    cliecked = pyqtSignal()
    def __init__(self,parent=None,play_mode_1=None,play_mode_2=None,play_mode_3=None,play_mode_4=None,init_mode=None):
        super(Play_Button_3, self).__init__(parent)
        self.play_mode_ico = [play_mode_1,play_mode_2,play_mode_3,play_mode_4]  # 顺序播放,随机播放，循环播放，单曲循环播放
        self.play_mode = init_mode
        self.setPixmap(QPixmap(self.play_mode_ico[self.play_mode]))
        self.setScaledContents(True)
    def mousePressEvent(self, event):
        self.play_mode = (self.play_mode+1) % 4
        self.setPixmap(QPixmap(self.play_mode_ico[self.play_mode]))
        self.cliecked.emit()

"""
重写QSlider，让其能够支持鼠标点击到指定位置和滚轮事件，并返回进度条对应值
"""
class My_Slider(QSlider):
    cliecked = pyqtSignal(int)
    def __init__(self,orientation=None,parent=None):
        super(My_Slider, self).__init__(orientation,parent)

    # 鼠标单击事件，点哪指哪
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mousePressEvent(event)      # 调用父级的单击事件，听说这样能不影响进度条原来的拖动
            val_por = event.pos().x() / self.width()    # 获取鼠标在进度条的相对位置
            self.setValue(int(val_por * self.maximum()))
            self.cliecked.emit(self.value())

    # 滚轮事件，当滚轮转过120度角时进度条对应的值对应的增或减5个百分点
    def wheelEvent(self, event):
        max = self.maximum()
        min = self.minimum()
        if event.angleDelta().y() >= 120:
            new_val = self.value() + max * 0.05
            if new_val >= max:
                new_val = max
            self.setValue(int(new_val))
        elif event.angleDelta().y() <= -120:
            new_val = self.value() - max * 0.05
            if new_val <= min:
                new_val = min
            self.setValue(int(new_val))
#
"""
实现唱片'动'起来的小窗口
"""
"""唱片"""
class Cp_Comp_1(QObject):
    def __init__(self):
        super(Cp_Comp_1, self).__init__()
        # 加载图片资源
        pixmap_1 = QPixmap(':/img/cp/play_cp_comp1.png')
        # 按比例设置图片大小
        scaledPixmap_1 = pixmap_1.scaled(150,150)
        # 初始化动作
        self.animation()
        # 定义QGraphicsPixmapItem
        self.pixmap_item_1 = QGraphicsPixmapItem(scaledPixmap_1)
        # 设置item旋转的中心点
        self.pixmap_item_1.setTransformOriginPoint(75,75)   # 中心
        # 设置图片的初始位置
        self.pixmap_item_1.setPos(0,30)

    def _set_rotation(self,degree):
        self.pixmap_item_1.setRotation(degree)    # 自身改变角度
    def animation(self):
        # 创建唱片360°无死角转动
        self.anim = QPropertyAnimation(self, b'rotation')   # 动画类型('rotation':转动,'pos':位置移动)
        self.anim.setDuration(40000)     # 运行的秒速(经测试，网易云用户每播放40s的歌曲，世界上就会有一张无辜唱片被转动一周)
        self.anim.setStartValue(0)  # 起始角度
        self.anim.setEndValue(360)  # 结束角度
        self.anim.setLoopCount(-1)  # 设置循环次数
    rotation = pyqtProperty(int, fset=_set_rotation)    # 属性动画改变自身数值(传递信号？？)

"""把柄"""
class Cp_Comp_2(QObject):
    def __init__(self):
        super(Cp_Comp_2, self).__init__()
        # 加载图片资源
        pixmap_2 = QPixmap(':/img/cp/play_cp_comp2.png')
        # 按比例设置图片大小
        scaledPixmap_2 = pixmap_2.scaled(85,50)
        # 初始化动作
        self.animation()
        # 定义QGraphicsPixmapItem
        self.pixmap_item_2 = QGraphicsPixmapItem(scaledPixmap_2)
        # 设置item旋转的中心点
        self.pixmap_item_2.setTransformOriginPoint(0,0) # 左上角
        # 设置图片的初始位置
        self.pixmap_item_2.setPos(70,-12)

    def _set_rotation(self,degree):
        self.pixmap_item_2.setRotation(degree)    # 自身改变角度
    def animation(self):
        # 转轴转动的动画之开和关
        self.anim_1 = QPropertyAnimation(self, b'rotation')
        self.anim_1.setStartValue(0)  # 起始角度
        self.anim_1.setEndValue(25)  # 结束角度
        self.anim_1.setLoopCount(1)  # 设置循环次数
        self.anim_2 = QPropertyAnimation(self, b'rotation')
        self.anim_2.setStartValue(25)  # 起始角度
        self.anim_2.setEndValue(0)  # 结束角度
        self.anim_2.setLoopCount(1)  # 设置循环次数

    rotation = pyqtProperty(int, fset=_set_rotation)    # 属性动画改变自身数值(传递信号？？)

"""呈现动画的界面"""
"""因为QWeidget之类的是静态的，所以不能用来作为动画的呈现界面(是这样子理解的吧)"""
class Cp_Win(QGraphicsView):
    def __init__(self,parent=None):
        super(Cp_Win, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setStyleSheet('background-color:rgba(111,249,193,240);border-radius:4px;')
        self.initView()
    def initView(self):
        self.cp_comp_1 = Cp_Comp_1()
        self.cp_comp_2 = Cp_Comp_2()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-10,0,170,200)    # 设置动画区域，在此区域内的控件会被动态刷新
        self.scene.addItem(self.cp_comp_1.pixmap_item_1)   # 往容器里面添加item
        self.scene.addItem(self.cp_comp_2.pixmap_item_2)   # 往容器里面添加item
        self.setScene(self.scene)       # 英文翻译:设置场景？？

    def start(self):
        self.cp_comp_1.anim.start()
        self.cp_comp_2.anim_1.start()

    def stop(self):
        self.cp_comp_1.anim.pause()
        self.cp_comp_2.anim_2.start()



"""
音量调节小窗口
"""
class Volume_Win(QWidget):
    def __init__(self,parent=None):
        super(Volume_Win, self).__init__(parent)
        self.hide()             # 设置隐藏窗口，点击控件师弹出
        self.setGeometry(332,156,30,80)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.vol_slider = My_Slider(Qt.Vertical, self)
        self.vol_slider.setGeometry(0,0,20,78)
        self.vol_slider.setRange(0,100)
        self.vol_slider.setValue(30)
        self.vol_slider.setObjectName('Vol_Slider')
        self.setStyleSheet('My_Slider#Vol_Slider{background-color:rgba(255,255,255,0.4);border-radius:6px;padding-top:6px;padding-bottom:6px;}'
                           'My_Slider#Vol_Slider::handle:vertical{height:10px;background-color:rgb(255,255,255);border-radius:4px;margin:0px -2px 0px -2px;}'
                           'My_Slider#Vol_Slider::groove:vertical{width:6px;background-color:rgb(255,255,255)};margin-left:2px;margin-right:4px;}'
                           'My_Slider#Vol_Slider::groove:vertical:hover{width:8px;background-color:rgb(219,219,219);}'
                           'My_Slider#Vol_Slider::sub-page:vertical{background-color:rgb(219,219,219);}'
                           'My_Slider#Vol_Slider::add-page:vertical{background-color:rgb(236,65,65);}')

"""
歌单显示界面
"""
class Playlist_Win(QWidget):
    send_index = pyqtSignal(int)
    def __init__(self,parent,playlist,music_path):
        super(Playlist_Win,self).__init__(parent)
        self.setGeometry(420,0,280,300)
        self.songs_mess = list()
        self.playlist = playlist
        self.initUI()
        self.could_music = Could_Music(music_path)
        # self.songs_mess = could_music.get_songs_mess()

    def initUI(self):
        # 搜索框
        search_eidt = QLineEdit(self)
        search_eidt.setGeometry(10,15,260,25)
        search_eidt.setPlaceholderText('搜索歌曲(支持歌名/歌手/专辑)')
        search_eidt.editingFinished.connect(lambda :self.search(search_eidt.text()))
        # 歌单的Qtable
        self.playlist_t = QTableWidget(self)  # 表格歌单
        self.playlist_t.setGeometry(10,50,260,224)
        self.playlist_t.setColumnCount(4) # 设置表格为4列
        self.playlist_t.setShowGrid(False)  # 设置无格子线
        self.playlist_t.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中
        self.playlist_t.setFrameShape(QFrame.NoFrame)   # 设置无边框
        self.playlist_t.itemDoubleClicked.connect(self.double_play) # 双击播放
        self.playlist_t.itemClicked.connect(self.cliecked)   # 单击事件
        self.playlist_t.setStyleSheet('background:rgb(111,249,193);selection-background-color:#059058;')
        # 获取垂直表头并设置
        playlist_v = self.playlist_t.verticalHeader()
        playlist_v.setVisible(False)    # 隐藏行数
        # 获取表格水平表头并对列宽进行设置
        playlist_h = self.playlist_t.horizontalHeader()
        playlist_h.setSectionResizeMode(0,QHeaderView.ResizeToContents) # 设置第二列固定,其他列均自适应
        playlist_h.setSectionResizeMode(1,QHeaderView.Fixed)
        playlist_h.setSectionResizeMode(2,QHeaderView.Fixed)
        playlist_h.setSectionResizeMode(3,QHeaderView.Fixed)
        playlist_h.resizeSection(0,20)      # 设置初始列宽
        playlist_h.resizeSection(1,110)
        playlist_h.resizeSection(2,60)
        playlist_h.resizeSection(3,60)
        playlist_h.setStretchLastSection(True)  # 设置充满表头
        playlist_h.setStyleSheet("QHeaderView::section{background:rgb(111,249,193);}")
        # 获取滚动条并设置
        playlist_vs = self.playlist_t.verticalScrollBar()
        playlist_vs.setStyleSheet('border-redius:3px;width:5px;background:rgb(111,249,193);')
        playlist_hs = self.playlist_t.horizontalScrollBar()
        playlist_hs.setStyleSheet('height:5px;background:rgb(111,249,193);border-redius:3px;')

        # playlist_v.set
        # self.playlist_h.resizeSection()
        self.playlist_t.setHorizontalHeaderLabels(['','音乐标题', '歌手','专辑'])   # 设置标题
        self.playlist_t.setEditTriggers(QAbstractItemView.NoEditTriggers) # 禁止编辑


        # 添加按钮
        local_load_button = QPushButton('本地导入',self)
        local_load_button.clicked.connect(self.load_from_local)
        local_load_button.setFlat(True) # 设置按钮扁平
        web_load_button = QPushButton('网络导入',self)
        web_load_button.clicked.connect(self.load_from_web)
        web_load_button.setFlat(True)
        local_load_button.setGeometry(40,272,80,30)
        web_load_button.setGeometry(160,272,80,30)

    # 网络导入
    def load_from_web(self):
        share_url,ok = QInputDialog.getText(self,'输入框','请输入分享链接')
        if ok:
            is_ok,result = self.could_music.get_songs_mess(share_url)
            if is_ok:
                for res in result:
                    QMessageBox.information(self,'成功',f'成功从[{res["author"]["name"]}]导入歌单[{res["playlist"]["name"]}]')
                    json_path = self.parent().config.value('/playlist/json_path')
                    if res["playlist"]["name"] + '.json' not in json_path.split(';'):  # 向配置中导入信息
                        json_path = json_path + res["playlist"]["name"] + '.json' + ';'
                        self.parent().config.setValue('/playlist/json_path',json_path)
                    self.load_playlist(res['songs'])
            else:
                QMessageBox.warning(self,'发生了一些错误',f'{result}')
        else:
            QMessageBox.warning(self,'发生了一些错误','请输入至少一条分享链接！')
    # 本地导入
    def load_from_local(self):
        json_paths = QFileDialog.getOpenFileNames(self,'导入歌单','.','Json数据(*.json)')
        if json_paths[0]:          # 选择了至少一个文件
            for json_path in json_paths[0]:
                is_ok,result = load_local_json(json_path)
                if is_ok:
                    QMessageBox.information(self, '成功',
                                        f'成功从[{result["author"]["name"]}]导入歌单[{result["playlist"]["name"]}]')
                    json_path = self.parent().config.value('/playlist/json_path')
                    if result["playlist"]["name"] + '.json' not in json_path.split(';'):  # 向配置中导入信息
                        json_path = json_path + result["playlist"]["name"] + '.json' + ';'
                        self.parent().config.setValue('/playlist/json_path', json_path)
                    self.load_playlist(result['songs'])
                else:
                    QMessageBox.warning(self, '发生了一些错误', f'{result}')
        else:
            QMessageBox.warning(self,'发生了一些错误','请选择至少一个文件！')

    # 往歌单里导入数据
    def load_playlist(self,result):
        if self.songs_mess:  # 如果原有歌单列表不为空
            j = i = len(self.songs_mess)    # 在当前歌曲的末尾导入
        else:
            i = j = 0
        self.songs_mess.extend(result)  # append是插入元素，列表将会作为一个整体，extend是将新列表的每个元素插入进去
        for song in result:
            # 往QTable中添加数据
            self.playlist_t.insertRow(i)  # 动态添加行
            if i+1 < 100:
                index_item = QTableWidgetItem('{:02d}'.format(i+1))
            else:
                index_item = QTableWidgetItem(str(i+1))
            sname_item = QTableWidgetItem(song['name'])
            auname_item = QTableWidgetItem(song['author_name'])
            alname_item = QTableWidgetItem(song['album_name'])
            self.playlist_t.setItem(i, 0, index_item)
            self.playlist_t.setItem(i, 1, sname_item)
            self.playlist_t.setItem(i, 2, auname_item)
            self.playlist_t.setItem(i, 3, alname_item)
            self.playlist_t.setRowHeight(i,20)
            if i % 2:
                self.playlist_t.item(i,3).setBackground(QColor(9,220,135))
                self.playlist_t.item(i,0).setBackground(QColor(9,220,135))
                self.playlist_t.item(i,1).setBackground(QColor(9,220,135))
                self.playlist_t.item(i,2).setBackground(QColor(9,220,135))
            self.playlist_t.update()
            if not self.playlist.addMedia(QMediaContent(QUrl(song['download_url']))):
                QMessageBox.warning(self,'发生了一些错误',f'歌曲{song["name"]}导入失败，请检查链接！')
            i += 1
        self.send_index.emit(j)
        self.playlist_t.scrollToItem(self.playlist_t.item(j,0),hint=QAbstractItemView.PositionAtTop)

    # 双击播放歌曲
    def double_play(self,item):
        self.send_index.emit(item.row())
        self.parent().start_play()
    def cliecked(self,item):
        self.send_index.emit(item.row())

    # 歌单搜索功能
    def search(self,text):
        result = self.playlist_t.findItems(text,Qt.MatchContains | Qt.MatchWrap)
        if result:    # 搜索结果不为空
            search_row = result[0].row()
            self.playlist_t.scrollToItem(self.playlist_t.item(search_row,0),QAbstractItemView.PositionAtTop)    # 跳转到搜索行



"""
播放器主界面入口
"""
class Play_Win(QWidget):
    load_lcy = pyqtSignal(str)
    def __init__(self,parent=None):
        super(Play_Win,self).__init__(parent)

        self.initSetting()  # 初始化配置
        self.initUI()   # 界面初始化
        self.init_player_UI()   # 播放器初始化
        self.init_vol_UI()  # 音量界面初始化
        self.init_playlist_UI() # 歌单初始化

    def initSetting(self):
        self.config = QSettings('./PLAYER_CONFIG.ini',QSettings.IniFormat)  # 配置读写
        if self.config.value('/player/volume'): # 音量
            self.volume = self.config.value('/player/volume')
        else:
            self.config.setValue('/player/volume',30)
            self.volume = 30
        if self.config.value('/playlist/json_path'):    # 歌单路径
            self.json_path = self.config.value('/playlist/json_path')
        else:
            self.config.setValue('/playlist/json_path', '')
            self.json_path = ''
        if self.config.value('/playlist/last_song'):    # 上一首歌曲索引
            self.last_song = self.config.value('/playlist/last_song')
        else:
            self.config.setValue('/playlist/last_song', 0)
            self.last_song = 0
        if self.config.value('/playlist/main_path'):    # 歌曲主目录
            self.music_path = self.config.value('/playlist/root_path')
        else:
            self.config.setValue('/playlist/root_path', './Music')
            self.music_path = './Music'

    def initUI(self):
        """
        窗口界面调整
        """
        self.resize(420,300)
        self.bg_color = QColor(111,249,193)  # 设置背警色
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint) # 无边框
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
                           'My_Slider#Song_Slider::handle:horizontal{width:10px;background-color:rgb(255,255,255);margin:-2px 0px -2px 0px;border-radius:4px;}'
                           'My_Slider#Song_Slider::groove:horizontal{height:4px;background-color:rgb(219,219,219)}'
                           'My_Slider#Song_Slider::groove:horizontal:hover{height:6px;background-color:rgb(219,219,219)}'
                           'My_Slider#Song_Slider::add-page:horizontal{background-color:rgb(219,219,219);}'
                           'My_Slider#Song_Slider::sub-page:horizontal{background-color:rgb(236,65,65);}')
        """
        网易云独有唱片组件
        """
        self.cp_win = Cp_Win(self)
        self.cp_win.setGeometry(0,0,200,210)

        """
        布局一些按钮组件：上一首，播放/暂停，下一首，播放模式，音量，歌单，音效
        """
        self.last_button = Play_Button_1(self,':/img/button/last_no.png',False)
        self.play_button = Play_Button_2(self,':/img/button/pause.png',':/img/button/start.png',False)
        self.next_button = Play_Button_1(self, ':/img/button/next_no.png')
        self.playMode_button = Play_Button_3(self,':/img/button/seq_play.png',':/img/button/random_play.png',
                                  ':/img/button/loop_play.png',':/img/button/only_play.png',0)
        self.soundEff_button = Play_Button_1(self, ':./img/button/sound_ef.png',False)
        # self.soundEff_button.setObjectName('sound')
        self.volume_button = Play_Button_1(self, ':/img/button/volume.png', False)
        self.playlist_button = Play_Button_1(self, ':/img/button/song_sheet.png',False)

        # 设置按钮的提示信息
        self.last_button.setToolTip('上一首')
        self.next_button.setToolTip('下一首')
        self.play_button.setToolTip('播放/暂停')
        # 设置按钮的位置
        self.last_button.setGeometry(110, 223, 50, 50)
        self.play_button.setGeometry(180, 218, 60, 60)
        self.next_button.setGeometry(260, 223, 50, 50)
        self.playMode_button.setGeometry(20, 238, 30, 30)
        self.soundEff_button.setGeometry(62, 238, 30, 30)
        self.volume_button.setGeometry(328, 238, 30, 30)
        self.playlist_button.setGeometry(370, 238, 30, 30)
        # 按钮连接槽函数
        self.last_button.cliecked.connect(lambda: self.buttonChange(self.last_button))
        self.play_button.cliecked.connect(lambda: self.buttonChange(self.play_button))
        self.next_button.cliecked.connect(lambda: self.buttonChange(self.next_button))
        self.playMode_button.cliecked.connect(lambda :self.buttonChange(self.playMode_button))
        self.volume_button.cliecked.connect(lambda :self.buttonChange(self.volume_button))
        self.playlist_button.cliecked.connect(lambda :self.buttonChange(self.playlist_button))
        self.soundEff_button.cliecked.connect(lambda :self.buttonChange(self.soundEff_button))

        """
        歌曲信息和歌词部分
        """
        self.song_message = QLabel(self)
        self.song_message.setText('<style><div>text-align:center</div></style><p><font size=4><b>聆听世界的声音</b></font></p>'
                             '<pre><font size=2>歌手:</font><a href="https://music.163.com/#/artist?id=32725601"><font size=2>歌手</font></a>'
                             '<font size=2>  专辑:</font><a href="https://music.163.com/#/album?id=81658154"><font size=2>专辑</font></a></pre>')
        self.song_message.setOpenExternalLinks(True)
        self.song_message.setAlignment(Qt.AlignCenter)
        self.song_message.setGeometry(210,10,170,70)

        self.song_lcy = QLabel(self)
        self.song_lcy.setText('<font size=5>Love to<br>ABAB Player</font>')
        self.song_lcy.setGeometry(245,80,130,100)
        self.succ_loadlcy = False
        self.load_lcy.connect(self.loadLcy)  # 切换歌曲发送导入歌曲信息的信号

        """
        进度条以及播放时长，播放总时长组件
        """
        self.song_slider = My_Slider(Qt.Horizontal,self)   # 设置水平进度条
        self.song_slider.setObjectName('Song_Slider')
        self.alr_time = QLabel('00:00',self)     # 已播放时长标签
        self.all_time = QLabel('00:00',self)    # 总时长标签
        # 设置标签位置
        self.song_slider.setGeometry(80, 280, 260, 18)
        self.alr_time.setGeometry(33, 278, 40, 20)
        self.all_time.setGeometry(347,278,40,20)

        """
        进度条连接槽函数
        """
        self.song_slider.sliderMoved.connect(self.sliderChange)   # 滑动进度条触发
        self.song_slider.cliecked.connect(self.sliderChange)        # 点击进度条触发

    """
    播放器初始化
    """
    def init_player_UI(self):
        self.player = QMediaPlayer(self)  # 创建一个播放器
        self.player.setVolume(int(self.volume))
        self.player.positionChanged.connect(self.playing)  # 播放位置改变事件

    """
    音量调节界面初始化
    """
    def init_vol_UI(self):
        self.volume_win = Volume_Win(self)
        self.volume_win.vol_slider.valueChanged.connect(lambda :self.player.setVolume(self.volume_win.vol_slider.value()))    # 音量调节事件

    """展开与关闭动作"""
    def spread_anim(self):
        # 对当前状态进行判断
        end_rect = self.geometry()
        if end_rect.width() == 420:
            endWidth = 700
        else:
            endWidth = 420
        end_rect.setWidth(endWidth)

        self.anim = QPropertyAnimation(self,b'geometry')  # 坐标动作类型
        self.anim.setDuration(500)    # 设置动作时长
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(end_rect)
        self.anim.start()


    """
    歌单初始化
    """
    def init_playlist_UI(self):
        self.playlist = QMediaPlaylist()  # 播放列表
        self.player.setPlaylist(self.playlist)  # 设置播放器播放列表
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)  # 初始化为顺序播放
        self.playlist_win = Playlist_Win(self,self.playlist,self.music_path)    # 歌单界面初始化
        if self.json_path:  # 如果初始歌单存在
            self.load_playlist()
        if self.last_song != '0':
            self.playlist.setCurrentIndex(int(self.last_song))
        self.player.durationChanged.connect(self.durationChange)   # 播放时长改变
        self.playlist.currentIndexChanged.connect(self.switchSong)  # 歌曲改变事件
        self.playlist_win.send_index.connect(self.switchSong)


    """歌曲播放事件：进度条位置改变，进度标签改变，歌词部分改变"""
    def playing(self,time):     # time:播放位置时长，ms
        if self.succ_loadlcy:
            if time >= int(self.lcy_time[self.count+1]) and self.count < self.lcy_len: # 播放位置改变，对应的歌词计数器值改变
                self.textChange()
        if time == self.player.duration():
            self.succ_loadlcy = False
            self.update()
            self.song_lcy.show()
        arl_time = int(time / 1000)
        mm = int(arl_time / 60) # 分钟
        ss = int(arl_time % 60) # 秒钟
        self.song_slider.setValue(arl_time)
        self.alr_time.setText("{:02d}:{:02d}".format(mm,ss))    # 格式化，{:2d}->输出两位整数，{:02d}->输出两位整数，不够的以0替代
    """滑动进度条改变歌曲的播放时间"""
    def sliderChange(self,val):
        self.player.setPosition(int(val * 1000))
    """开始播放"""
    def start_play(self):
        self.player.play()
        self.cp_win.start()
        self.play_button.status = True
        self.play_button.changeStatus()
    def stop_play(self):
        self.player.pause()
        self.cp_win.stop()
        self.play_button.status = False
        self.play_button.changeStatus()
        self.play_button.setToolTip('点击播放')
    """播放时长改变"""
    def durationChange(self,time):
        all_time = int(time / 1000)
        mm = int(all_time / 60)  # 分钟时长
        ss = int(all_time % 60)  # 秒钟时长
        self.song_slider.setRange(0, all_time)
        self.all_time.setText("{:02d}:{:02d}".format(mm, ss))  # 设置总时长
    """歌词切换事件"""
    def textChange(self):
        self.count += 1
        self.update()
    """歌单导入事件"""
    def load_playlist(self):
        for path in self.json_path.split(';'):
            if path:
                path = self.music_path + '/json/' + path
                is_ok, result = load_local_json(path)
                if is_ok:
                    self.playlist_win.load_playlist(result['songs'])
                else:
                    QMessageBox.warning(self, '发生了一些错误', f'{result}')
    """歌词导入事件"""
    def loadLcy(self,id):
        is_ok,self.lcy_dir = parse_lrc(id=id)# 返回一个歌词字典:{'0232':'如果这都不算爱'}
        if is_ok:
            self.lcy_time = list(self.lcy_dir.keys())
            self.lcy_len = len(self.lcy_time)
            self.count = 0  # 初始化歌词计数器
            self.succ_loadlcy = True

    """歌曲切换事件"""
    def switchSong(self,i):
        self.playlist.setCurrentIndex(i)
        self.song_slider.setValue(0)  # 重置进度条
        self.load_lcy.emit(self.playlist_win.songs_mess[i]['id'])
        self.playlist_win.playlist_t.scrollToItem(self.playlist_win.playlist_t.item(i,0))   # 设置歌单显示到切换的歌曲
        # 规范歌曲名字，以免过长
        name_mess = handle_text(self.playlist_win.songs_mess[i]["author_name"],self.playlist_win.songs_mess[i]['album_name'])
        self.play_button.setToolTip(f'正在播放<b>{self.playlist_win.songs_mess[i]["name"]}</b>')   # 修改按钮提示信息
        self.song_message.setText(f'<style><div>text-align:center</div></style><p><font size=4><b>{self.playlist_win.songs_mess[i]["name"]}</b></font></p>'
                                  f'<pre><font size=2>歌手:<a href="{self.playlist_win.songs_mess[i]["author_url"]}">{name_mess[0]}</a></font>'
                                  f'<font size=2>  专辑:<a href="{self.playlist_win.songs_mess[i]["album_url"]}">{name_mess[1]}</a></font></pre>')

    """按钮连接的槽函数"""
    def buttonChange(self,button):
        if button == self.last_button:      # 上一首播放
            # 设置播放按钮状态
            self.start_play()
            if self.playlist.currentIndex() == 0:   # 如果当前歌曲在表头，则上一首为列表最后一首歌
                self.playlist.setCurrentIndex(self.playlist.mediaCount()-1)
            elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:  # 让单曲循环模式下也能进行上一首切换
                self.playlist.setCurrentIndex(self.playlist.currentIndex()-1)
            else:
                self.playlist.previous()
        elif button == self.next_button:    # 下一首播放
            self.start_play()
            if self.playlist.currentIndex() == self.playlist.mediaCount()-1:
                self.playlist.setCurrentIndex(0)
            elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:  # 让单曲循环模式下也能进行下一首切换
                self.playlist.setCurrentIndex(self.playlist.currentIndex() + 1)
            else:
                self.playlist.next()
        elif button == self.play_button:    # 播放/暂停
            if not self.play_button.status:
                self.start_play()
            else:
                self.stop_play()
        elif button == self.playMode_button:    # 切换歌单模式
            if self.playMode_button.play_mode == 0:
                self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            elif self.playMode_button.play_mode == 1:
                self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            elif self.playMode_button.play_mode == 2:
                self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            else:
                self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        elif button == self.volume_button:     # 音量调节
            if self.volume_button.status:
                self.playlist_button.status = False
                self.volume_win.show()
            else:
                self.volume_win.hide()
        elif button == self.playlist_button:    # 歌单界面
            if self.playlist_button.status:
                self.volume_button.status = False
                self.spread_anim()
                self.volume_win.hide()
            else:
                self.spread_anim()
        else:
            ok = QMessageBox.information(self,'提示','哎呀!该功能程序员还在熬夜制作中···')

    def closeEvent(self, event):
        self.last_song = self.playlist.currentIndex()
    """
    窗口绘制事件：绘制圆角和背景色
    """
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
        play_bottom.setTop(275)
        play_bottom.setHeight(25)
        painter_bottom = QPainter(self)
        painter_bottom.setRenderHint(QPainter.Antialiasing,True)    # 抗锯齿
        painter_bottom.setBrush(QColor(9,220,135,255))
        painter_bottom.begin(self)
        painter_bottom.drawRoundedRect(play_bottom,10,10)
        painter_bottom.end()
        if self.succ_loadlcy:   # 如果导入歌词成功，则开始描绘歌词
            self.song_lcy.hide()    # 隐藏歌词标识语
            # 描绘歌词
            if self.count == 0:
                self.text_1 = ''
                self.text_2 = self.lcy_dir[self.lcy_time[self.count]]
                self.text_3 = self.lcy_dir[self.lcy_time[self.count+1]]
            elif self.count == self.lcy_len:
                self.text_1 = self.lcy_dir[self.lcy_time[self.count-1]]
                self.text_2 = self.lcy_dir[self.lcy_time[self.count]]
                self.text_3 = ''
            else:
                self.text_1 = self.lcy_dir[self.lcy_time[self.count - 1]]
                self.text_2 = self.lcy_dir[self.lcy_time[self.count]]
                self.text_3 = self.lcy_dir[self.lcy_time[self.count + 1]]

            painter_1 = QPainter(self)
            painter_2 = QPainter(self)
            painter_3 = QPainter(self)
            font_1 = QFont('黑体', 8)
            font_2 = QFont('黑体', 10)
            font_2.setLetterSpacing(QFont.AbsoluteSpacing, 1)  # 设置字体间距
            font_2.setBold(True)
            painter_1.setFont(font_1)
            painter_2.setFont(font_2)
            painter_3.setFont(font_1)
            painter_1.drawText(QRect(180, 80, 240, 40), Qt.AlignCenter, self.text_1)
            painter_2.drawText(QRect(180, 120, 240, 40), Qt.AlignCenter, self.text_2)
            painter_3.drawText(QRect(180, 160, 240, 40), Qt.AlignCenter, self.text_3)

app = QApplication(argv)
play = Play_Win()
play.show()
exit(app.exec_())
