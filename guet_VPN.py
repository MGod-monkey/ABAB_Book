# 登录桂电VPN
from requests import post, get, session
from re import search

class Guet_VPN(object):
    def __init__(self,username='1900200327',password='155237'):
        self.login_url = 'https://v.guet.edu.cn/do-login'
        self.main_url = 'https://v.guet.edu.cn/'
        self.username = username
        self.password = password
        # 表头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        }
        self.init_para()    # 初始化表单数据
        self.login_result = self.init_cookie()  # 初始化cookie并得到登录结果


    def init_para(self):
        # 表单
        self.datas = {'auth_type': 'local', 'username': self.username, 'sms_code': '', 'password': '', 'captcha': '',
                      'needCaptcha': 'false', 'captcha_id': '5UK7b0RAfOL9R6O'}
        # 加密获取表单password数据
        passwd_len = len(self.password)
        passwordBytes = list(self.password)
        passwdBytes_len = len(passwordBytes)
        if passwdBytes_len < 16:
            for i in range(16 - passwdBytes_len):
                passwordBytes.append('0')
        for i in range(16):
            passwordBytes[i] = ord(passwordBytes[i])
        # 密匙编码
        key = list('wrdvpnisawesome!')
        keyBytes = []
        for i in range(len(key)):
            keyBytes.append(ord(key[i]))
        # print(keyBytes)
        keyBytes_un = [134, 8, 187, 0, 251, 59, 238, 74, 176, 180, 24, 67, 227, 252, 205, 80]
        # 运算
        encryptBytes = []
        for i in range(16):
            encryptBytes.append(keyBytes_un[i] ^ passwordBytes[i])
        # print(encryptBytes)
        # 加密
        def encrypt(bytes):
            Hex = list('0123456789abcdef')
            result = []
            for i in range(len(bytes)):
                v = bytes[i]
                result.append(Hex[(v & 0xf0) >> 4] + Hex[v & 0x0f])
            return result
        result_1 = str()
        result_2 = str()
        for i in encrypt(keyBytes):
            result_1 += i
        for i in encrypt(encryptBytes):
            result_2 += i
        result_2 = result_2[0:passwd_len * 2]
        self.datas['password'] = result_1 + result_2
        # print(self.datas)

    def init_cookie(self):
        # 通过修改请求头方式使用cookie
        response = post(url=self.login_url, headers=self.headers, data=self.datas)
        self.headers['cookie'] = 'wengine_vpn_ticket' + '=' + response.cookies.get_dict()['wengine_vpn_ticket']
        return search(r'"success": ([a-z]*).*',response.text).group(1)
        # 天府欧session类使用cookie
        # session1 = session()  # 实例化session对象
        # response = session1.post(url=login_url, headers=headers, data=datas)  # 使用session对象发送get请求 就能获取服务端设置的session对象
        # response_2 = session1.get(url='https://v.guet.edu.cn/', headers=headers)
        # with open('use_session.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response_2.text)

# print(datas)
# def count_time(fn):
#     def inner():
#         start = time()
#         fn()
#         end = time()
#         print(end - start)
#
#     return inner
#
# @count_time
# def zc():



# @count_time
# def use_session():



