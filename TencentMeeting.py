import subprocess
from tokenize import Name
import uiautomation as uia

# 打开系统自带的某个程序
# subprocess.Popen('wemeetapp.exe')
# 打开其他程序
def open_tencent_meeting():
    subprocess.Popen('C:\Program Files (x86)\Tencent\WeMeet\wemeetapp.exe')  # 可执行文件的具体地址信息
    ClientArea = uia.PaneControl(Name='ClientArea')
    LoadingViewContainerFrame = ClientArea.PaneControl(Name='LoadingViewContainerFrame')
    MainFrame = LoadingViewContainerFrame.PaneControl(Name='MainFrame')
    NarrowPanel = MainFrame.PaneControl(Name='NarrowPanel')
    HomeNavigationFrame = NarrowPanel.PaneControl(Name='HomeNavigationFrame"')
    HomeNavigationStackPanel = HomeNavigationFrame.PaneControl(Name='HomeNavigationStackPanel')
    JoinBtnFrame = HomeNavigationStackPanel.PaneControl(Name='JoinBtnFrame')
    # JoinBtnFrame.fin
    JoinButton = JoinBtnFrame.ButtonControl(Name='加入会议')
    JoinButton.Click()
    print("————")
# client_area = tencent_window.WindowControl()

# open_tencent_meeting()
# join_Btn = window.ButtonControl(AutomationId='')