# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/11/4--18:18
__author__ = 'Henry'


from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def add_to_16(text):
    # str不是16的倍数那就补足为16的倍数
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)  # 返回bytes


def pkcs7padding(data):
    bs = AES.block_size
    padding = bs - len(data) % bs
    padding_text = chr(padding) * padding
    return data + padding_text


def AES_encrypt(text):
    '''AES加密'''
    # text:待加密文本
    text = pkcs7padding(text)
    key = 'd0936268a554ed2a'  # 密钥key
    iv = b'2441e23aca5285a8'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    # print('AES加密值:', encrypted_text)
    return encrypted_text


def AES_decrypt(encrypted_text):
    '''AES解密'''
    # text:待解密文本
    encrypted_text = pkcs7padding(encrypted_text)
    key = '6faf4a2fa46ac1cb'  # 密钥key
    iv = b'4d6c56abc669f198'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    decrypted_text = str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
    # print('解密值：', decrypted_text)
    return decrypted_text


def AES_encrypt_history(text):
    '''AES加密(history接口)'''
    # text:待加密文本
    text = pkcs7padding(text)
    key = '2e1bc1e3ca65a4cb'  # 密钥key
    iv = b'c7054589723df4a7'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    # print('AES加密值:', encrypted_text)
    return encrypted_text


def AES_decrypt_history(encrypted_text):
    '''AES解密(history接口)'''
    # text:待解密文本
    encrypted_text = pkcs7padding(encrypted_text)
    key = 'd1119693b6a33af8'  # 密钥key
    iv = b'7aba45824f51431a'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    decrypted_text = str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
    # print('解密值：', decrypted_text)
    return decrypted_text