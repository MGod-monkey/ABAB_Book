from json import dumps,loads
from requests import get
from re import findall,sub
from os import path,mkdir
from random import choice
from User_Agent import user_agent

# 各类错误代码和提示信息
error = {
    'network_error':'网络异常：请检查网络是否正常！',
    'overfreq_error':'操作错误：操作过于频繁，请稍后再试',
    'playlistId_error':'歌单ID错误：请检查歌单链接！',
    'playlistNot_error':'歌单ID错误: 歌单不存在！',
    'playlistCont_error':'歌单内容错误：歌单内容为空！',
    'download_error':'下载错误：请检查网络或歌曲ID！',
    'filehaved_error':'文件错误：文件已存在！',
    'jsontype_error':'Json格式错误：请检查本地json格式！',
}

# 解析分享链接
def get_id(share_url):
    result = findall(r'playlist/(.*?)/', share_url)  # 手机分享歌单形式
    if not result:
        result = findall(r'id=(.*?)\&userid=', share_url)  # pc分享歌单形式
        if not result:
            return None
        else:
            return result
    else:
        return result

# 对歌手，专辑作过长处理
def handle_text(author_name,arl_name):
    if len(author_name) > 3:
        author_name = author_name[:3] + '.'
    if len(arl_name) > 3:
        arl_name = arl_name[:3] + '.'
    return author_name,arl_name

# 拼凑歌名和演唱者，获取文件路径名
def get_download_path(song_name,author,main_path):
    download_path = main_path + '/download'
    if not path.exists(download_path):
        mkdir(download_path)
    new_name = sub(r'[/:?*"<>|]]+','_',f'{song_name}--{author}')    # 规范名字
    if not path.exists(download_path + '/' + new_name + '.mp3'):    # 判断歌曲是否存在
        return download_path + '/' + new_name + '.mp3'
    else:
        return None

# 返回json数据路径
def get_json_path(main_path,json_name):
    json_path = main_path + '/json'
    if not path.exists(json_path):
        mkdir(json_path)
    new_name = sub(r'[/:?*"<>|]]+', '_', f'{json_name}')  # 规范名字
    return json_path + '/' + json_name + '.json'

# 从本地导入json数据
def load_local_json(json_path):
    if path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as fp:
            result = loads(fp.read())
        if 'author' in result and 'playlist' in result and 'songs' in result:   # 对本地json作简单的判断
            return True,result
        else:
            return False,error['jsontype_error']
    else:
        return False,error['jsontype_error']


# 解析歌词，返回{'time':'歌词'}字典
def parse_lrc(id=None,lcy_path=None):
    if lcy_path:
        with open(lcy_path, 'r', encoding='utf-8') as fp:
            lcy = fp.read()
    else:
        lcy_url = 'http://music.163.com/api/song/media?id=' + id
        response = get(url=lcy_url)
        response = loads(response.text)
        try:
            lcy = response['lyric']
        except Exception:
            return False,'' # 纯音乐
    if lcy: # 如果歌词不为空
        result_dir = {}
        lcy_dir = {}
        depart_lcy = lcy.split('\n')    # ['[00:01.000] 作词 : 孙艺', '[00:02.000] 作曲 : 程振兴', '[00:33.538] 沉默着走了有 多遥远']
        try:
            for lcy in depart_lcy:
                l = lcy.replace('[',']').split(']') # ['', '00:01.000', ' 作词 : 孙艺']
                for i in range(len(l)-1):
                    if l[i]:
                        result_dir[l[i]] = l[-1]    # {'00:01.000': ' 作词 : 孙艺', '00:02.000': ' 作曲 : 程振兴', }
            # result.clear()  # 清理列表以备用
            for time in sorted(result_dir.keys()):
                ms_time = str(int(time.split(':')[0]) * 60 * 1000 + int(time.split(':')[1].split('.')[0]) * 1000 + int(
                    time.split(':')[1].split('.')[1]))  # 对时间进行处理转换为ms
                lcy_dir[ms_time] = result_dir[time]
        except Exception:
            return False,''     # 部分歌曲不合规范，这我无解啊（如前几句歌词没有时间）
        # lcy_dir{'0': ' 作词 : 易家扬', '1000': ' 作曲 : 颜子', '15110': '拿命干杯 云飞向天',}
        return True,lcy_dir
    else:
        return False,'加载错误'


# 解析歌曲字典获取有用信息
def get_message(main_path,main_dict):
    artist_url = 'https://music.163.com/#/artist?id='   # 演唱者主页外链
    alubum_url = 'https://music.163.com/#/album?id='    # 专辑外链
    download_url = 'https://music.163.com/song/media/outer/url?id=' # 下载外链
    result = {
        'author':'',
        'playlist':'',
        'songs':''
    }
    # 用户者信息包含：用户id，用户名，用户头像
    author = {
        'id':'',
        'name':'',
        'avatar_img':''
    }
    # 歌单信息包含：歌单id，歌单名
    playlist = {
        'id':'',
        'name':''
    }
    # 歌曲信息包含：歌曲id，歌曲名，歌曲下载链接，演唱者，演唱者url，专辑名，专辑url
    song = {
        'id':'',
        'name':'',
        'download_url':'',
        'author_name':'',
        'author_url':'',
        'album_name':'',
        'album_url':''
    }
    # 用户信息
    author['id'] = str(main_dict['playlist']['creator']['userId'])
    author['name'] = main_dict['playlist']['creator']['nickname']
    author['avatar_img'] = main_dict['playlist']['creator']['avatarUrl']
    # 歌单信息
    playlist['id'] = str(main_dict['playlist']['id'])
    playlist['name'] = main_dict['playlist']['name']

    """
    判断同名歌单是否存在，若存在则返回本地信息
    """
    if path.exists(get_json_path(main_path,playlist['name'])):
        with open(get_json_path(main_path,playlist['name']),'r',encoding='utf-8') as fp:
            return loads(fp.read())

    """
    同名歌单不存在，从网络中获取信息
    """
    songs = list()
    for i in main_dict['playlist']['trackIds']:
        song = dict()
        song['id'] = str(i['id'])
        song['download_url'] = download_url + str(i['id']) + '.mp3'
        # 直接调用https://api.imjad.cn/提供的查询歌曲信息接口，在此由衷的感谢这个接口给我这个菜鸡提供了一个可行的方法，网易云的js代码真心看不懂
        datail_song_url = 'https://api.imjad.cn/cloudmusic?type=detail&id=' + song['id']
        datail_songs = loads(get(url=datail_song_url).text)
        song['name'] = datail_songs['songs'][0]['name']
        song['author_name'] = datail_songs['songs'][0]['ar'][0]['name']
        song['author_url'] = artist_url + str(datail_songs['songs'][0]['ar'][0]['id'])
        song['album_name'] = datail_songs['songs'][0]['al']['name']
        song['album_url'] = alubum_url + str(datail_songs['songs'][0]['al']['id'])
        print(song)
        songs.append(song)

    # 往字典里添加字典
    result['author'] = author
    result['songs'] = songs
    result['playlist'] = playlist

    with open(get_json_path(main_path,playlist['name']), 'w', encoding='utf-8') as fp:         # 将歌单信息存储在json数据中
        fp.write(dumps(result))
    return result



class Could_Music(object):
    def __init__(self,main_path=None):
        self.headers = {
            'use-agent': choice(user_agent),
        }
        self.main_path = main_path
        # 官网接口只放几条数据，瞎弄很久无果放弃了，直接调用某大佬接口
        #self.wy_music_url = 'http://music.163.com/api/playlist/detail?id=123123123131231'  # 网易云音乐歌单url
        self.wy_music_url = 'https://api.imjad.cn/cloudmusic?type=playlist&id=' # 文档：https://api.imjad.cn/
        self.qq_music_url = ''                                               # qq音乐歌单url
        self.kg_music_url = ''                                              # 酷狗音乐歌单url
        self.init_main_Dir()    # 初始化音乐的主目录

    """
    初始化音乐主目录
    """
    def init_main_Dir(self):
        if not path.exists(self.main_path):
            mkdir(self.main_path)

    """
    获取歌单信息
    """
    def get_songs_mess(self,share_url=None,music_type=None):
        id = get_id(share_url)
        result = []
        if id:          # 成功获取id
            for i in id:
                songs_url = self.wy_music_url + str(i)
                response = get(songs_url,headers=self.headers)
                if response.status_code == 200:         # 网络正常
                    main_dict = loads(response.text)
                    if main_dict['code'] == 200:    # 歌单正常
                        result_1 = get_message(self.main_path,main_dict)
                        result.append(result_1)
                    elif main_dict['code'] == 405:  # 操作过于频繁
                        return False,error['overfreq_error']
                    else:
                        return False, error['playlistNot_error']
                else:
                    return False, error['network_error']
            return True,result
        else:
            return False,error['playlistId_error']


    """
    下载歌曲
    """
    def download_song(self,song_name,song_author,download_url):
        download_path = r'{}'.format(get_download_path(song_name, song_author, self.main_path))
        try:
            if  download_path != 'None':
                mp3_file = get(download_url, headers=self.headers)
                with open(download_path,'wb') as fp:
                    fp.write(mp3_file.content)
                    fp.flush()  # 刷新
                    return True
            else:
                return False,error['filehaved_error']
        except Exception:
            return False,error['download_error']
    def download_songs(self,songs_dict):
        if songs_dict:
            for song in songs_dict:
                self.download_song(song['name'],song['author_name'],song['download_url'])
            return True
        else:
            return False,error['playlist_error']



# music = Could_Music()
# songs_dict = music.get_songs('https://music.163.com/playlist?id=887324290&userid=402819261')
# # print(songs_dict)
# music.download_songs(songs_dict['songs'])
