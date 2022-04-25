import socket
from volume1 import vl_set,vl_edit
import subprocess
from tokenize import Name
import uiautomation as uia

s = socket.socket()
#s =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
#定义socket类型，网络通信，TCP
host = socket.gethostname()

print(host)  
sysinfo = socket.gethostbyname_ex(host)
#ip_addr = sysinfo[2]
#ip_addr1 = ip_addr[0]
#ip_addr2 = ip_addr[1]
#print("IP Address: %s" %ip_addr1,ip_addr2)
#LAPTOP-1O20G0A6
#IP Address: 172.18.160.1 183.173.101.251  若有虚拟机，则更多

port = 8888
s.bind((host, port))
#绑定地址（host,port）到套接字
#在 AF_INET下，以元组（host,port）的形式表示地址

s.listen()  #开始TCP监听连接
c, addr = s.accept()  #进入循环，不断接受客户端的连接请求
print("connected")

def open_tencent_meeting(): 
    subprocess.Popen('C:\Program Files (x86)\Tencent\WeMeet\wemeetapp.exe')  # 可执行文件的具体地址信息
    ClientArea = uia.PaneControl(Name='ClientArea')
    LoadingViewContainerFrame = ClientArea.PaneControl(Name='LoadingViewContainerFrame')
    MainFrame = LoadingViewContainerFrame.PaneControl(Name='MainFrame')
    NarrowPanel = MainFrame.PaneControl(Name='NarrowPanel')
    HomeNavigationFrame = NarrowPanel.PaneControl(Name='HomeNavigationFrame"')
    HomeNavigationStackPanel = HomeNavigationFrame.PaneControl(Name='HomeNavigationStackPanel')
    JoinBtnFrame = HomeNavigationStackPanel.PaneControl(Name='JoinBtnFrame')
    JoinBtnFrame.fin
    JoinButton = JoinBtnFrame.ButtonControl(Name='加入会议')
    JoinButton.Click()


def modify_volume(data):
    # volume
    listdata = data.decode()[:-1].split(",")  #转为列表
    print(listdata)
    if(len(listdata)==3):
        vl_edit(listdata[2])
    if(len(listdata)==2):
        if(listdata[1]=='1'):
            vl_set(100.0)
            print("左键，音量100%")
        if(listdata[1]=='2'):
            vl_set(0.0)
            print("右键，已静音")

    c.send(b"echo\n")  #要加换行
    #发送 TCP 数据，将 string 中的数据发送到连接的套接字
    #返回值是要发送的字节数量，该数量可能小于 string 的字节大小

in_area = False
remote_control = False
camera = 0

while True:
    # 接收摄像头信息
    data = c.recv(1024)
    #接收 TCP 数据，数据以字符串形式返回，bufsize 指定要接收的最大数据量
    print("receive", data.decode())


    # camera
    if in_area:
        # 腾讯会议连接
        in_area = False
        open_tencent_meeting()

    if remote_control:
        # 手机作为遥控器
        modify_volume(data)
    
    if camera_data == 1:
        # 键盘连接手机
        camera_data = 1
    elif camera_data == 2: 
        # 键盘连接平板
        camera_data = 2
    elif camera_data == 3: 
        # 键盘连接电脑
        camera_data = 3

    

        


    

c.close()  #传输完毕后，关闭套接字