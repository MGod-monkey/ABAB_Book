from json import dumps,loads
from requests import session,get
from re import findall,sub
from os import path,mkdir
from time import sleep

# 各类错误代码和提示信息
error = {
    'playlistId_error':'歌单ID错误：请检查歌单链接！',
    'playlistNot_error':'歌单ID错误: 歌单不存在！',
    'playlistCont_error':'歌单内容错误：歌单内容为空！',
    'download_error':'下载错误：请检查网络或歌曲ID！',
}

# 解析分享链接
def get_id(share_url):
    result = findall(r'playlist/(.*?)/', share_url)  # 手机分享歌单形式
    if not result:
        result = findall(r'id=(.*?)&', share_url)  # pc分享歌单形式
        if not result:
            return None
        else:
            id = result[0]
    else:
        id = result[0]
    return id

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
    json_path = main_path+ '/json'
    if not path.exists(json_path):
        mkdir(json_path)
    new_name = sub(r'[/:?*"<>|]]+', '_', f'{json_name}')  # 规范名字
    return json_path + '/' + json_name + '.json'

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
    if path.exists(get_json_path(main_path,playlist['name'])):     # 歌单返回存在信息
        with open(get_json_path(main_path,playlist['name']),'r',encoding='utf-8') as fp:
            return loads(fp.read())
    # 歌曲信息
    songs = list()
    for i in main_dict['playlist']['trackIds']:
        song = dict()
        song['id'] = str(i['id'])
        song['download_url'] = download_url + str(i['id']) + '.mp3'
        # 直接调用https://api.imjad.cn/提供的查询歌曲信息接口，在此由衷的感谢这个接口给我这个菜鸡提供了一个可行的方法，网易云的js代码真心看不懂
        datail_song_url = 'https://api.imjad.cn/cloudmusic?type=detail&id=' + song['id']
        datail_songs = loads(get(url=datail_song_url).text)
        song['name'] = datail_songs['songs'][0]['name']
        song['author_name'] = datail_songs['songs'][0]['name']
        song['author_url'] = artist_url + str(datail_songs['songs'][0]['ar'][0]['id'])
        song['album_name'] = datail_songs['songs'][0]['al']['name']
        song['album_url'] = alubum_url + str(datail_songs['songs'][0]['al']['id'])
        # print(song)
        songs.append(song)

    # 往字典里添加字典
    result['author'] = author
    result['songs'] = songs
    result['playlist'] = playlist

    with open(get_json_path(main_path,playlist['name']), 'w', encoding='utf-8') as fp:         # 将歌单信息存储在json数据中
        fp.write(dumps(result))
    return result



class Could_Music(object):
    def __init__(self):
        self.headers = {
            'use-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                         '/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'referer': 'http://music.163.com/'
        }
        # 官网接口只放几条数据，瞎弄很久无果放弃了，直接调用某大佬接口
        #self.wy_music_url = 'http://music.163.com/api/playlist/detail?id=1234344'  # 网易云音乐歌单url
        self.wy_music_url = 'https://api.imjad.cn/cloudmusic?type=playlist&id=' # 文档：https://api.imjad.cn/
        self.qq_music_url = ''                                               # qq音乐歌单url
        self.kg_music_url = ''                                              # 酷狗音乐歌单url

        self.main_path = './Music/'                                      # 音乐下载路径
        if not path.exists(self.main_path):
            mkdir(self.main_path)

    """
    获取歌单信息
    """
    def get_songs(self,share_url=None,music_type=None):
        id = get_id(share_url)
        if id:
            songs_url = self.wy_music_url + id
            response = get(songs_url,headers=self.headers)
            if response.status_code == 200:
                main_dict = loads(response.text)
                result = get_message(self.main_path,main_dict)
                return result
            return error['playlistNot_error']
        else:
            return error['playlistId_error']

    """
    下载歌曲
    """
    def download_song(self,song_name,song_author,download_url):
        download_path = r'{}'.format(get_download_path(song_name, song_author, self.main_path))
        try:
            print(download_url)
            if  download_path != 'None':
                print(download_path + '下载中...',end='\t\t')
                mp3 = get(download_url, headers=self.headers)
                sleep(4)    # 暂停3s防止被封
                with open(download_path,'wb') as fp:
                    fp.write(mp3.content)
                    fp.flush()  # 刷新
            else:
                print('歌曲已存在！')
        except Exception:
            return error['download_error']
    def download_songs(self,songs_dict):
        if songs_dict:
            for song in songs_dict:
                self.download_song(song['name'],song['author_name'],song['download_url'])
            return True
        else:
            return error['playlist_error']
        # print('已全部下载完成')



music = Could_Music()
songs_dict = music.get_songs('https://music.163.com/playlist?id=887324290&userid=402819261')
# print(songs_dict)
music.download_songs(songs_dict['songs'])
