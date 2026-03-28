import pyautogui
import time
import subprocess
import sys

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
    # 步骤 1：打开QQ，等待主窗口弹出
    print("步骤 1：正在打开 QQ...")
    try:
        subprocess.Popen(QQ_PATH)
    except FileNotFoundError:
        print("错误：找不到 QQ.exe，请检查配置区的 QQ_PATH 是否正确。")
        sys.exit()
    
    # 给予足够的时间让QQ启动并登录（根据你电脑的速度调整）
    print("等待 10 秒，让 QQ 主窗口完全弹出...")
    time.sleep(10) 

    # 步骤 2：点击联系人图标
    print("步骤 2：点击联系人图标...")
    click_image('contact_icon.png')

    # 步骤 3 & 4：找到分组名为“特别关心”的一栏并点击
    print("步骤 3 & 4：点击“特别关心”分组...")
    click_image('special_care.png')

    # 步骤 5：点击“杨万琴”，并等待个人资料界面出现
    print("步骤 5：点击联系人“杨万琴”...")
    # 这里需要双击才能打开资料/聊天窗口（根据你的QQ设置可能是单击或双击头像）
    # 如果单击就能打开个人资料，可以继续用 click_image。如果是双击，需要稍微改写：
    location = pyautogui.locateCenterOnScreen('yangwanqin.png', confidence=CONFIDENCE)
    if location:
        pyautogui.click(location) # 单击展开或者进入
        time.sleep(3) # 等待资料卡弹出
    else:
        print("找不到杨万琴，程序终止。")
        sys.exit()

    # 步骤 6：点击个人资料界面里的点赞按钮，要点击10次
    print("步骤 6：疯狂点赞 10 次...")
    # 先找到点赞按钮的位置
    like_location = pyautogui.locateCenterOnScreen('like_button.png', confidence=CONFIDENCE)
    
    if like_location:
        for i in range(10):
            pyautogui.click(like_location)
            # 每次点击间隔0.1秒，模拟真人连续点击，防止被系统识别为恶意脚本
            time.sleep(0.1) 
        print("✅ 任务完成！已成功点赞 10 次。")
    else:
        print("找不到点赞按钮。请确认个人资料界面已打开，且截图无误。")

if __name__ == "__main__":
    # 运行前留给你3秒钟切回桌面或者准备
    print("程序将在 3 秒后开始运行，请不要移动鼠标...")
    time.sleep(3)
    main()