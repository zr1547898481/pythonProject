#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import allure
import jsonpath
import pymysql
import requests
import rsa
from Crypto.Cipher import AES


class Apikey():

    @allure.step('发送get请求')
    def get(self,url,params=None, **kwargs):
        return requests.get(url= url,params=params,**kwargs)

    @allure.step('发送post请求')
    def post(self,url,data=None,json=None,**kwargs):
        return requests.post(url= url,data=data,json=json,**kwargs)

    # 基于jsonpath关键字，提取需要的内容
    @allure.step('获取返回结果字典值')
    def get_text(self,res,key):
        data = json.loads(res)
        value = jsonpath.jsonpath(data,key)
        return value[0]

    @allure.step('数据库检查')
    def check_sqldb(self,sql):
        # 1.建立连接
        conn = pymysql.connect(
            host='shop-xo.hctestedu.com',
            port=3306,
            user ='api_test',
            passwd='Aa9999!',
            db ='shopxo_hctested',
            charset='utf8'
            )
        # 2.创建游标
        cur =conn.cursor()
        # 3.执行sql
        cur.execute(query=sql)
        # 4.获取第一行查询结果，取元组第一个值
        result = cur.fetchone()[0]
        # 5.关闭连接
        cur.close()
        return result

    @allure.step('md5加密')
    def hash_md5(self,md5_str):
        return hashlib.md5(md5_str.encode('utf8')).hexdigest()

    @allure.step('AES初始化')
    def initAES(self,key):
        global aes,length
        key = key.encode()  # 初始化秘钥
        length = AES.block_size  # 初始化数据块大小
        aes = AES.new(key,AES.MODE_ECB)  # 初始化aes对象

    @allure.step('填充函数')
    def pad(self,text):
        count = len(text.encode())
        add = length - (count % length)
        entext = text + chr(add) * add
        return entext

    @allure.step('AES加密')
    def encrypt(self,encryData):
        res = aes.encrypt(self.pad(encryData).encode())
        msg = base64.b64encode(res).decode()
        return msg

    @allure.step('AES解密')
    def decrypt(self,decryData):
        unpad = lambda date: date[0:-ord(date[-1])]  # 截取函数
        res = base64.b64decode(decryData.encode())
        msg = aes.decrypt(res).decode()
        return unpad(msg)

    @allure.step('RSA初始化')
    def initRSA(self,num):
        pubkey,privkey = rsa.newkeys(num)
        # 生成公钥、私钥保存到文件中
        pub = pubkey.save_pkcs1()
        priv = privkey.save_pkcs1()
        with open('../test_data/pubkey.pem','wb') as f,open('../test_data/privkey.pem','wb') as f1:
            f.write(pub)
            f1.write(priv)

    @allure.step('公钥加密')
    def enRSA(self,entext):
        f = open('../test_data/pubkey.pem','rb').read()
        print(f.decode())
        # 导入公钥
        pub = rsa.PublicKey.load_pkcs1(f)
        en_text = rsa.encrypt(entext.encode(),pub)
        str_text = base64.b64encode(en_text).decode()
        return str_text

    @allure.step('私钥解密')
    def deRSA(self, deData):
        f = open('../test_data/privkey.pem','rb').read()
        print(f.decode())
        # 导入私钥
        priv= rsa.PrivateKey.load_pkcs1(f)
        de_text = base64.b64decode(deData.encode())
        str_text = rsa.decrypt(de_text,priv).decode()
        return str_text


if __name__ == '__main__':
    ak =Apikey()
    # MD5加密
    print(ak.hash_md5('hello world'))
    # 初始化
    ak.initAES('12345678qwerasdf')
    text = 'hello world'
    # 填充
    print(ak.pad(text))
    # 加密
    en_text = ak.encrypt(text)
    print('AES加密：',en_text)
    # 解密
    de_text = (ak.decrypt(en_text))
    print('AES解密：',de_text)
    # 生成公钥、私钥
    ak.initRSA(256)
    enmsg = ak.enRSA('测试RSA加密')
    print('RSA加密:',enmsg)
    demsg = ak.deRSA(enmsg)
    print('RSA解密:',demsg)




