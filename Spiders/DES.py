# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/11/4--18:41
__author__ = 'Henry'


import base64
import pyDes


class DES(object):
    # IV必须是 8 字节长度的十六进制数
    # key加密密钥长度，24字节

    def __init__(self, iv, key):
        self.iv = iv  # 偏移量
        self.key = key  # 密钥

    def encrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)  # DES
        d = k.encrypt(data)
        d = base64.encodestring(d)
        return d

    def decrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = base64.decodestring(data)
        d = k.decrypt(data)
        return d


def DES_decrypt(decrypted_text):
    '''DES解密'''
    encryptdata = decrypted_text.encode()
    des = DES('9ff4453b', '863f30c7f96c96fb')
    decryptdata = des.decrypt(encryptdata)
    return decryptdata


def DES_decrypt_history(decrypted_text):
    '''DES解密(history接口)'''
    encryptdata = decrypted_text.encode()
    des = DES('1bbb415a', '41d96dd9ee1dc0db') # iv,key
    decryptdata = des.decrypt(encryptdata)
    return decryptdata