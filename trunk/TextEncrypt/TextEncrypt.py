#!/usr/bin/env python
# -*- coding: utf-8 -*-
#TextEncrypt.py
#Direction:
#2012-08-12 14:24:33 by zw zwholdu@gmail.com

import ctypes
import sys
import hashlib

from PyQt4 import QtGui,QtCore

Version = '0.1'

p = lambda s:ctypes.c_char_p(s)

#bytes转化为hex格式
def bytesToViewable(b):
    print('unviewable bytes len = %d'%len(b))
    print(b)

    viewableStr = ''
    count = 0
    for byte in b:
        #print(byte)
        s = hex(byte)[2:].upper()
        if len(s) == 1:
            viewableStr += '0' + s
        else:
            viewableStr += s

    print('viewable str len = %d'%len(viewableStr))
    
    return viewableStr 

def viewableToBytes(viewableStr):
    print('viewable str len = %d'%len(viewableStr))

    if len(viewableStr)%2 != 0:
        raise Exception("数据长度不为2的整数倍")

    count = 0
    b = bytearray(int(len(viewableStr)/2))
    
    for count in range(int(len(viewableStr)/2)):
        #print(viewableStr[count:count+2])
        b[count] = int(viewableStr[count*2:count*2+2] ,base = 16)

    print('unviewable bytes len = %d'%len(b))
    print(b)
    
    return bytes(b)


#加密长度为8整数倍的bytes
#msg_b,key 为 bytes类型
#返回相同长度加密之后的bytes
def encrypt_bytes(msg_b,key):
    global Objdll

    if len(msg_b)%8 !=0:#需要填充为8字节的整数倍
        raise Exception("数据长度不为8的整数倍") 
    
    print('before encrypt bytes,len = ',len(msg_b))
    tmp_raw = ctypes.create_string_buffer(len(msg_b))

    ret = Objdll.DES_Encrypt_Data(p(msg_b),p(key),tmp_raw,ctypes.c_int(len(msg_b)))
    
    print('after encrypt bytes,len = ',len(tmp_raw.raw))
    print(tmp_raw.raw)
    
    #print('ret = ',ret)
    
    return tmp_raw.raw

#解密长度为8整数倍的bytes
#msg_b,key 为 bytes类型
#返回相同长度解密之后的bytes
def decrypt_bytes(msg_b,key):
    global Objdll

    if len(msg_b)%8 !=0:#需要填充为8字节的整数倍
        raise Exception("数据长度不为8的整数倍") 
    
    print('before decrypt bytes,len = ',len(msg_b))
    tmp_raw = ctypes.create_string_buffer(len(msg_b))

    ret = Objdll.DES_Decrypt_Data(p(msg_b),p(key),tmp_raw,ctypes.c_int(len(msg_b)))
    
    print('after decrypt bytes,len = ',len(tmp_raw.raw))
    print(tmp_raw.raw)
    
    #print('ret = ',ret)
    return tmp_raw.raw

#根据传入的key来加密str_plain
#返回加密之后的str_plain
#处理str_plain编码,长度补全,并计算key的md5作为密钥
#在尾部附加 补全长度 标记和校验信息
#返回加密之后的str_plain
def encrypt_string(str_plain,key):
    print('before encrypt string,str len = ',len(str_plain))
    text_bytes = str_plain.encode('utf-8')
    
    key_bytes = key.encode('utf-8')
    key_md5 = hashlib.new('md5',key_bytes).digest()
    print('key_md5 = ',key_md5)
    print('before encrypt string,bytes len = ',len(text_bytes))
    
    #补全长度为8的整数倍
    if len(text_bytes)%8 !=0:#需要填充为8字节的整数倍
        tail_len = 8 - len(text_bytes)%8
        text_bytes += b' ' * tail_len
    else:
        tail_len = 0

    ret = encrypt_bytes(text_bytes,key_md5)
    
    print('after encrypt string,bytes len = ',len(ret))

    #在加密数据的尾部附加填充长度信息
    tmp = bytearray(1)
    tmp[0] = tail_len
    ret += bytes(tmp)

    #尾部附加md5的后四位作为校验信息
    ret += hashlib.new('md5',ret).digest()[-4:]
    
    return bytesToViewable(ret)


#根据传入的key来解密string
#返回解密之后的string
#处理string编码,并计算key的md5作为密钥
#读取尾部附加的 补全长度 标记,去掉加密过程中添加到尾部的无用字符
#返回解密之后的string
def decrypt_string(str_encrypted,key):
    print('before decrypt string,str len = ',len(str_encrypted))
    
    key_bytes = key.encode('utf-8')
    key_md5 = hashlib.new('md5',key_bytes).digest()
    print('key_md5 = ',key_md5)
    
    encrypt_bytes = viewableToBytes(str_encrypted)

    #去除尾部的md5信息
    encrypt_bytes = encrypt_bytes[:-4]

    tail_len = ord(encrypt_bytes[-1:])
    encrypt_bytes = encrypt_bytes[:-1]#尾部长度信息
    print('tail len = ',tail_len)

    print('before encrypt string,bytes len = ',len(encrypt_bytes))

    ret = decrypt_bytes(encrypt_bytes,key_md5)
    
    print('after encrypt string,bytes len = ',len(ret))
    
    #如果加密时在尾部填充了字符,那就在这里移除
    if tail_len > 0:
        ret = ret[:-tail_len]

    try:
        ret = ret.decode('utf-8')
    except:#解码错误,保持原字符不变
        global user_text
        print('解码错误')
        QtGui.QMessageBox.warning(None,'Error','解码错误,请检查口令是否正确')
        ret = user_text.toPlainText()
        
    return ret
        




#判断当前文本是否经过加密
def judge_encrypted( msg_str ):
    msg_str = user_text.toPlainText()
    
    try:
        encrypt_bytes = viewableToBytes(msg_str)
    except:
        return False
    
    #是否达到最小长度
    if len(encrypt_bytes) < 8 + 1 + 4:
        return False
        
    md5_tail = encrypt_bytes[-4:]
    encrypt_bytes = encrypt_bytes[:-4]
    
    if hashlib.new('md5',encrypt_bytes).digest()[-4:] == md5_tail:
        return True
    else:
        return False


def refresh_gui():
    global trans_button,encrypted_flag 
    
    encrypted_flag = False
    msg_str = user_text.toPlainText()
    
    if judge_encrypted(msg_str) == True:
        encrypted_flag = True
        print('12')
        trans_button.setText('解密')
    else:
        print('34')
        encrypted_flag = False
        trans_button.setText('加密')

def trans():
    global key,user_text,encrypted_flag
    print('*'*50)

    text_str = user_text.toPlainText()
    print('len = %d,text = %s'%(len(text_str),text_str))

    key_str = key.text()
    print('key = ',key_str)

    if encrypted_flag:
        ret = decrypt_string(text_str,key_str)
    else:    
        ret = encrypt_string(text_str,key_str)

    user_text.setPlainText(ret)

    

def main():
    global Version,Objdll

    Objdll = ctypes.cdll.LoadLibrary("des_X2")

    app = QtGui.QApplication(sys.argv)
    windows_main = QtGui.QWidget()#主窗口
    windows_main.setWindowTitle("文本加密工具 V" + Version + "   By AW")
    windows_main.resize(500,250)

    icon = QtGui.QIcon("img\\TextEncrypt.ico")
    windows_main.setWindowIcon(icon)

    layout_main = QtGui.QVBoxLayout()
    layout_up = QtGui.QHBoxLayout()

    global key,user_text,trans_button
    key_label = QtGui.QLabel("口令")
    key = QtGui.QLineEdit()
    trans_button = QtGui.QPushButton("加密")

    user_text = QtGui.QTextEdit()
    
    layout_up.addWidget(key_label)
    layout_up.addWidget(key)
    #layout_up.addStretch(1)
    layout_up.addWidget(trans_button)
    
    layout_main.addLayout(layout_up)
    layout_main.addWidget(user_text)
    windows_main.setLayout(layout_main)
    
    trans_button.clicked.connect(trans)
    
    user_text.textChanged.connect(refresh_gui)
    
    windows_main.show()
    sys.exit(app.exec_())
    
    input('Press Enter to exit')

if __name__ == '__main__':
    main()
else:
    print ('TextEncrypt.py had been imported as a module')

