import screen_brightness_control as sbc 
import numpy as np

# 2. 设置屏幕亮度​​​​​​​ 50%
# sbc.set_brightness(50) 
# print(sbc.get_brightness())


def light_control(data):
    # 获取当前屏幕亮度值
    current_brightness = sbc.get_brightness() 
    print(current_brightness)
    brightt=np.float_(current_brightness[0])
    if float(float(data[2])<0):  #双指向上滑，提高亮度
        if(brightt<90):
            brightt=brightt+10
        else:
            brightt=100
    else:  #向下滑，调低亮度
        if(brightt>10):
            brightt=brightt-10
        else:
            brightt=0
    
    sbc.fade_brightness(brightt, increment = 10)
    # 渐进式设置屏幕亮度​​​​​​​
    # 以步长10的速度将屏幕亮度从当前值调整到100%

    print(f'已设置亮度为{sbc.get_brightness()[0]}%')   