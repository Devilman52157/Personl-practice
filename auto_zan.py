import pyautogui
import time
import subprocess
import sys
import os  # [新增] 用于执行系统命令（检测进程和关闭QQ）

# ---------------- 配置区 ----------------
# 请将这里的路径替换为你电脑上 QQ 程序的实际真实路径
QQ_PATH = r"E:\QQ\QQ.exe"

# 图像识别的置信度 (0.8表示80%相似即可，需要安装 opencv-python)
CONFIDENCE = 0.8
# ----------------------------------------

def click_image(image_path, wait_time=2, max_retries=10):
    """
    寻找屏幕上的图片并点击。
    带有重试机制，防止界面加载慢导致找不到。
    """
    print(f"正在寻找: {image_path}...")
    for i in range(max_retries):
        try:
            # locateCenterOnScreen 会返回找到的图片的中心坐标
            location = pyautogui.locateCenterOnScreen(image_path, confidence=CONFIDENCE)
            if location is not None:
                pyautogui.click(location)
                print(f"成功点击: {image_path}")
                time.sleep(wait_time) # 点击后等待一下
                return True
        except pyautogui.ImageNotFoundException:
            pass # 捕获找不到异常，继续重试
        
        time.sleep(1) # 找不到就等1秒再找
    
    print(f"超时未找到: {image_path}，程序终止。")
    sys.exit()

def main():
    # [修改] 步骤 1：检测QQ运行状态
    print("步骤 1：正在检查 QQ 运行状态...")
    # 通过系统的 tasklist 命令获取当前正在运行的所有程序名单
    process_list = subprocess.Popen('tasklist', stdout=subprocess.PIPE, shell=True).communicate()[0].decode('gbk', errors='ignore')
    
    if 'QQ.exe' in process_list:
        print("-> 检测到 QQ 已经在运行！尝试使用快捷键 Ctrl+Alt+Z 呼出主界面...")
        # 模拟按下组合键 Ctrl + Alt + Z
        pyautogui.hotkey('ctrl', 'alt', 'z')
        time.sleep(3) # 给它 3 秒钟时间弹出界面
    else:
        print("-> QQ 未运行，准备从路径启动程序...")
        try:
            subprocess.Popen(QQ_PATH)
        except FileNotFoundError:
            print("错误：找不到 QQ.exe，请检查配置区的 QQ_PATH 是否正确。")
            sys.exit()
        print("-> 等待 10 秒，让 QQ 主窗口完全弹出...")
        time.sleep(10) 

    # 步骤 2：点击联系人图标
    print("步骤 2：点击联系人图标...")
    click_image('contact_icon.png')

    # 步骤 3 & 4：找到分组名为“特别关心”的一栏并点击
    print("步骤 3 & 4：点击“特别关心”分组...")
    click_image('special_care.png')

    # 步骤 5：点击“杨万琴”，并等待个人资料界面出现
    print("步骤 5：点击联系人“杨万琴”...")
    location = pyautogui.locateCenterOnScreen('yangwanqin.png', confidence=CONFIDENCE)
    if location:
        pyautogui.click(location) # 单击展开或者进入
        time.sleep(3) # 等待资料卡弹出
    else:
        print("找不到杨万琴，程序终止。")
        sys.exit()

    # 步骤 6：点击个人资料界面里的点赞按钮，要点击10次
    print("步骤 6：疯狂点赞 10 次...")
    like_location = pyautogui.locateCenterOnScreen('like_button.png', confidence=CONFIDENCE)
    
    if like_location:
        for i in range(10):
            pyautogui.click(like_location)
            time.sleep(0.1) 
        print("✅ 点赞任务完成！")
    else:
        print("找不到点赞按钮。请确认个人资料界面已打开，且截图无误。")
        
    # [新增] 步骤 7：任务完成后关闭 QQ
    print("步骤 7：正在关闭 QQ 程序...")
    # 执行系统命令，强制关闭 QQ.exe 进程树
    os.system("taskkill /F /IM QQ.exe /T >nul 2>nul")
    print("✅ QQ 已成功关闭，自动化运行结束！")

if __name__ == "__main__":
    print("程序将在 3 秒后开始运行，请不要移动鼠标...")
    time.sleep(3)
    main()