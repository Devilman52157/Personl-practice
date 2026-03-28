import pyautogui
import time
import subprocess
import sys
import pyperclip 
import os 
import keyboard

# ---------------- 配置区 ----------------
# 这是你电脑上 MuMu 模拟器的真实路径
MUMU_PATH = r"E:\MuMu\MuMuPlayerGlobal\nx_main\MuMuNxMain.exe"

# 图像识别置信度
CONFIDENCE = 0.8
# ----------------------------------------

# =========================================================
# ⬇️ 核心功能函数区 ⬇️
# =========================================================

def click_image(image_path, wait_time=2):
    """
    【死等版】基础点击：只要没找到图片，就永远在原地等，绝不报错退出！
    """
    print(f"正在死死盯住屏幕，等待出现: {image_path}...")
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=CONFIDENCE)
            if location is not None:
                pyautogui.click(location)
                print(f"✅ 终于等到并成功点击: {image_path}")
                time.sleep(wait_time)
                return True # 点击成功，放行到下一步
        except pyautogui.ImageNotFoundException:
            pass # 没找到，当做无事发生
        time.sleep(1) # 休息1秒钟，然后继续瞪大眼睛找


def click_relative(anchor_image, offset_x, offset_y, wait_time=2):
    """
    【死等版】万能偏移点击：永远等待参照物出现，出现后再偏移点击！
    """
    print(f"正在死死盯住参照物: {anchor_image} 并准备偏移点击...")
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(anchor_image, confidence=CONFIDENCE)
            if location is not None:
                target_x = location.x + offset_x
                target_y = location.y + offset_y
                pyautogui.click(target_x, target_y)
                print(f"✅ 终于等到 {anchor_image}！成功点击偏移坐标: ({target_x}, {target_y})")
                time.sleep(wait_time)
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)


def close_all_popups(x_image_path):
    """
    【顺其自然版】关弹窗：只点当前屏幕上有的叉叉，没有就立刻进行下一步，绝不死等！
    """
    print(f"正在检查是否有活动弹窗 ({x_image_path})...")
    close_count = 0
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(x_image_path, confidence=CONFIDENCE)
            if location is not None:
                pyautogui.click(location)
                close_count += 1
                print(f"   -> 发现弹窗！已关闭 (累计 {close_count} 个)。")
                time.sleep(2) # 关掉一个后，停顿2秒看有没有下一个弹出来
            else:
                break # 没找到叉叉，立刻打破循环！
        except pyautogui.ImageNotFoundException:
            break # 报错没找到，也立刻打破循环！
    print("✅ 弹窗检查完毕，继续执行任务！")


def paste_text(text):
    """
    【降维打击版】使用底层硬件级驱动发送按键，无视模拟器拦截！
    """
    pyperclip.copy(text)
    print("-> 文本已复制到剪贴板，等待 1.5 秒...")
    time.sleep(1.5) 
    
    # 【关键防断触】在原地再点一下左键，强制把 Windows 的键盘焦点抢到模拟器输入框上
    pyautogui.click()
    time.sleep(0.5)

    print("-> 正在发送物理级 Ctrl+V ...")
    # 直接发送底层快捷键
    keyboard.send('ctrl+v')
    
    print("-> 粘贴动作执行完毕！")
    time.sleep(1)

def main():
    # 步骤 1：打开mumu模拟器
    print("步骤 1：启动 MuMu 模拟器...")
    try:
        subprocess.Popen(MUMU_PATH)
    except FileNotFoundError:
        print("错误：找不到 MuMu 模拟器，请检查路径。")
        sys.exit()
    print("等待 15 秒，让模拟器主界面初步加载...")
    time.sleep(15)

    # 步骤 2：点击运行 Android 设备
    print("步骤 2：启动安卓引擎...")
    click_image('run_device.png', wait_time=2) 

    # 步骤 3：找到王者荣耀并打开
    print("步骤 3：等待安卓开机并打开王者荣耀...")
    click_image('wzry_icon.png', wait_time=10)

    # 步骤 4：点击开始游戏，并清理弹窗
    print("步骤 4：点击开始游戏...")
    click_image('start_game.png', wait_time=2) 
    
    # 🌟 让子弹飞一会儿：强制等大厅加载 🌟
    print("-> 强制等待游戏大厅加载 (约 15 秒)...")
    time.sleep(30) 
    close_all_popups('close_x.png')

    # 步骤 5：查找好友
    print("步骤 5：搜索好友 杨万琴...")
    click_image('friend_btn.png', wait_time=2)
    click_image('search_box.png', wait_time=3) # 点击搜索框后等3秒，确保光标闪烁
    paste_text("杨万琴")
    click_image('search_btn.png', wait_time=2)

    # 步骤 6：赠送金币并点击下一次
    print("步骤 6：等待列表刷新并赠送金币...")
    click_image('gift_gold.png', wait_time=2)
    click_image('next_time.png', wait_time=2)

    # 步骤 7：点击头像并点赞
    print("步骤 7：使用偏移绝招点击头像并点赞...")
    click_relative('search_btn.png', offset_x=-1464, offset_y=130, wait_time=3) 
    click_image('like_btn.png', wait_time=2) 

    print("🎉 游戏内自动化步骤圆满完成！")

    # ---------------- 终极清理与休眠操作 ----------------
    
    # 步骤 8：关闭 MuMu 模拟器
    print("步骤 8：正在强制关闭 MuMu 模拟器...")
    os.system("taskkill /F /IM MuMuNxMain.exe /T >nul 2>nul")
    os.system("taskkill /F /IM NemuHeadless.exe /T >nul 2>nul")
    time.sleep(3) 

    # 步骤 9：执行电脑休眠
    print("步骤 9：任务全部结束，准备进入休眠状态...")
    print("⚠️ 电脑将在 60 秒后休眠！如果想取消，请直接关闭这个黑色的运行窗口！")
    time.sleep(60) 
    os.system("shutdown /h")

if __name__ == "__main__":
    print("程序将在 3 秒后运行，请松开鼠标...")
    time.sleep(3)
    main()