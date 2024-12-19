import pyautogui
import time
 
def Jietugongju():
    # 等待1秒，确保鼠标悬停在想要截图的位置
    time.sleep(1)
 
    # 获取当前屏幕的截图，并将其保存为png文件
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

def Jietugongju_width_height(x,y,width,height):
    region_screenshot = pyautogui.screenshot(region=(x,y,width,height))
    region_screenshot.save('region_screenshot.png')
