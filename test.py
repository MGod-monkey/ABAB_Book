# 登录桂电VPN
from requests import post

url = 'https://v.guet.edu.cn/do-login'

# 表头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',

}

# 表单
datas = {'auth_type': 'local', 'username': input('请输入用户名：'), 'sms_code': '', 'password': '', 'captcha': '',
         'needCaptcha': 'false', 'captcha_id': '5UK7b0RAfOL9R6O'}

password = list(input('请输入密码：'))
text_len = len(password)

# 加密过程
# 密码Unicode编码
passwordBytes = password
if len(passwordBytes) < 16:
    for i in range(16-len(passwordBytes)):
        passwordBytes.append('0')
# print(passwordBytes)

for i in range(len(passwordBytes)):
    passwordBytes[i] = ord(passwordBytes[i])
# print(passwordBytes)

# 密匙编码
key = list('wrdvpnisawesome!')
keyBytes = []
for i in range(len(key)):
    keyBytes.append(ord(key[i]))
# print(keyBytes)

keyBytes_un = [134,8,187,0,251,59,238,74,176,180,24,67,227,252,205,80]
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
        result.append(Hex[(v & 0xf0)>>4] + Hex[v & 0x0f])
    return result
result_1 = str()
result_2 = str()
for i in encrypt(keyBytes):
    result_1 += i
for i in encrypt(encryptBytes):
    result_2 += i
result_2 = result_2[0:text_len*2]
datas['password'] = result_1+result_2
# print(datas)

response = post(url=url,headers=headers,data=datas)
print(response.text)