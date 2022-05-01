import os
# import datetime
# import time
import psutil


# "E:\studyfxz\scrcpy-win64-v1.24\scrcpy.exe"
# 运行exe文件
def run():
    # kill()
    # os.chdir(r"C:\Users\Desktop\\")
    os.chdir(r"E:\studyfxz\scrcpy-win64-v1.24\\")
    # 改变当前工作目录到指定的路径r
    path = "scrcpy.exe"
    print("运行scrcpy.exe进程")
    os.system("scrcpy --turn-screen-off")  # 息屏开启
    # os.system(path) 

# 杀掉进程
def kill():
    pids = psutil.pids()  # 返回当前运行的PID列表，PID为数字
    for pid in pids:
        p = psutil.Process(pid)  # 创建指定进程号的对象
        if p.name() == 'scrcpy.exe':  # 进程名
            print("杀死scrcpy.exe进程")
            cmd = 'taskkill /F /IM scrcpy.exe'
            os.system(cmd)
    # 执行command命令时需要打开一个终端，并且无法保存command命令的执行结果

run()
# def main(h1=5,h2=12):
#     run()
#     while True:
#         now = datetime.datetime.now()
#         print(now)
#         if now.hour == h1:
#             run()
#         # 每隔60分检测一次
#         if now.hour == h2:
#             run()
#         time.sleep(3600)