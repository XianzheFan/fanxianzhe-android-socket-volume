# 以QQ音乐为例，音乐播放时的快捷键：

from re import U
  # 模拟键盘所使用的包
import pykeyboard  
# import time   # 连续进行两个动作可能太快而效果不明显，因此加入暂停时间

k = pykeyboard.PyKeyboard()   # 键盘的实例k

def before_():
    k.press_key(k.alt_key)  # 按住alt键
    k.tap_key(k.function_keys[6])  
    k.release_key(k.alt_key)  # 松开alt键

def next_():
    k.press_key(k.alt_key)  # 按住alt键
    k.tap_key(k.function_keys[3])  # 点击F3键
    k.release_key(k.alt_key)  # 松开alt键

def begin_over():
    k.press_key(k.alt_key)  # 按住alt键
    k.tap_key(k.function_keys[5])  # 点击F5键
    k.release_key(k.alt_key)  # 松开alt键

def likes():
    k.press_key(k.alt_key)  # 按住alt键
    k.tap_key(k.function_keys[2])  # 点击F2键
    k.release_key(k.alt_key)  # 松开alt键

def click_option(data):
    if data==['1','1','3','3','3']:   # 11333 播放/暂停 单指单击 
        # 有个问题：单指滑动结束后会有单击的通信？？？
        begin_over()  
    if data==['1','3','3','3']:  # 我喜欢，双指单击
        likes()
    if len(data)==4 and data[3]=='1':
        if float(data[1])<-40 :  # 左滑，上一首
            before_()
        if float(data[1])>40:  # 右滑，下一首
            next_()


