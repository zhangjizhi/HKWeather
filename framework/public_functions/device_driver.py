# _*_ coding: utf-8 _*
import cv2
import uiautomator2 as u2
import os
import datetime
import allure
import time
from uiautomator2.xpath import XPathSelector

from config.pytest_config import Const
from framework.pulbic_helper import DoStepAction, findListByIndex
from framework.util.UiUtil import SwipeUp, SwipeDown, SwipeRight, SwipeLeft
from framework.util.YamlUtil import load_yml
from framework.util.logger import printf

intfurl = "http://127.0.0.1:9006/"
header = {"Accept-Language": "zh-CN,zh;", "Connection": "close", "Content-Type": "application/json; charset=UTF-8"}
device = u2.connect()
views = {}


def getViewStrByConfig(view_str):
    find_views = []
    for activity, view_list in views.items():
        for view_key, view_value in view_list.items():
            key_list = view_key.split('/')
            if view_str in key_list:
                find_views.append((activity, view_value))
    if find_views:
        if len(find_views) == 1:
            return find_views[0][1]
        else:
            currentActivity = device.app_current().get("activity")
            find_views = [x[1] for x in find_views if x[0] == currentActivity]
            if find_views:
                return find_views[0][1]
    else:
        return view_str


def InitViews(view_config_yml):
    view_ymls = view_config_yml.split(',')
    view_ymls = [x for x in view_ymls if str(x).endswith('.yml')]
    for yml in view_ymls:
        result = load_yml(yml)
        views.update(result)


def getSwipeCoordinate(view):
    if view:
        widget = getWidget(view)
    else:
        widget = None
    if widget is not None:
        x = widget.info['bounds']['left']
        width = widget.info['bounds']['right'] - widget.info['bounds']['left']
        y = widget.info['bounds']['top']
        height = widget.info['bounds']['bottom'] - widget.info['bounds']['top']
    else:
        width, height = device.window_size()
        x = 0
        y = 0
    return x, y, width, height


@allure.step('执行截屏')
@DoStepAction(action_description='执行截屏')
def takeScreen(display_name='HU'):
    screenshot_dir = Const.SCREENSHOT_PATH
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    if display_name == 'HU':
        picname = timestamp + ".png"
        picpath = os.path.join(screenshot_dir, picname)
        device.screenshot(picpath)
        printf(f"截图 {display_name}: {picpath}")
    else:
        raise Exception('不支持的 display name：%s' % display_name)
    with open(picpath, "rb") as f:
        pic_read = f.read()
        allure.attach(pic_read, picname, allure.attachment_type.PNG)
    return picname, picpath


# 按Home键
@allure.step('执行按home键')
@DoStepAction(action_description='执行press home')
def home():
    device.press("home")


# 按back键
@allure.step('执行按back键')
@DoStepAction(action_description='执行press back')
def back():
    device.press("back")


# 点击坐标
@allure.step('执行点击坐标')
@DoStepAction(action_description='点击坐标')
def tap(x, y):
    device.click(int(x), int(y))


@allure.step('执行获取所有子元素')
@DoStepAction(action_description='查找所有子元素')
def getChildren(parentView, view, parentIndex=None, index=None):
    widget = getWidget(parentView, parentIndex)
    if widget is not None:
        viewStr = getViewStrByConfig(view)
        if ':id/' in viewStr:
            children = [x for x in widget.child(resourceId=viewStr)]
        else:
            children = [x for x in widget.child(text=viewStr)]
        return findListByIndex(children, index)


# 从指定坐标滑动到另一个指定坐标
@allure.step('滑动直到出现某个控制')
@DoStepAction(action_description='滑动直到出现某个控件')
def swipeUpUntil(text):
    """
    上下滑动屏幕直到出现某个text
    params为字典类型 必须有text key
    """
    device(scrollable=True).scroll.to(text=text)
    return True


# 启动APP
@allure.step('执行启动APP')
@DoStepAction(action_description='执行启动app')
def appStart(package_name):
    if package_name:
        device.app_start(package_name)
        time.sleep(1)
    else:
        return {'result': False, 'errMsg': '没有执行参数package_name'}

        # 停止APP


@allure.step('执行停止APP')
@DoStepAction(action_description='appStop')
def appStop(package_name):
    device.app_stop(package_name)


# 获取当前界面activity
@allure.step('执行获取当前界面activity')
@DoStepAction(action_description='获取当前activity')
def appCurrentActivity():
    currentActivity = device.app_current().get("activity")
    return currentActivity

    # 根据设置获取控件


@allure.step('执行获取控件')
@DoStepAction(action_description='获取控件')
def getWidget(view, index=None):
    view_str = getViewStrByConfig(view)
    if not view_str:
        raise Exception(f"资源配置找不到对应的的{view}")
    if '//*[@' in view_str:
        widget = device.xpath(view_str)
    elif ':id/' in view_str:
        widget = device(resourceId=view_str)
    else:
        widget = device(text=view_str)
    if widget.wait(timeout=20):
        if isinstance(widget, XPathSelector):
            widget = widget.all()
        return findListByIndex(widget, index)


# 发送key
@allure.step('执行发送key')
@DoStepAction(action_description='发送key')
def press(key):
    device.press(key)


@allure.step('执行shell命令')
@DoStepAction(action_description='执行shell')
def shell(cmd):
    device.shell(cmd)


@allure.step('执行多次启动app')
@DoStepAction(action_description='多次启动app')
def startAppTimes(appName, times=1):
    result = []
    for i in range(times):
        device.app_start(appName)
        time.sleep(1)
        activity = device.app_current().get("activity")
        result.append(activity)
        time.sleep(1)
    return result


# 清空app配置信息
@allure.step('执行清空app缓存')
@DoStepAction(action_description='执行清空app缓存')
def appClear(appName):
    device.app_clear(appName)


@allure.step('执行获取系统当前时间')
@DoStepAction(action_description='获取系统时间')
def getCurrentTime(timeFormat=None):
    current_time = device.shell('date').output
    current_time = str(current_time).strip().replace('\n', '').replace('\r', '')
    last_position = current_time.rindex(' ')
    last_position_pre = current_time.rindex(' ', 0, last_position)
    b = current_time[last_position_pre:last_position]
    current_time = current_time.replace(b, '')
    current_time = time.mktime(time.strptime(current_time, "%a %b %d %H:%M:%S %Y"))
    setTime = int(current_time)
    if timeFormat:
        setTime = time.localtime(setTime)
        set_time_str = time.strftime(timeFormat, setTime)
        return {'当前时间': set_time_str}
    else:
        return {'当前时间': setTime}


# @allure.step('执行黑屏检查')
# def check_blackscreen(self):
#     result = True
#     errmsg = ""
#     errDict = {}
#     pic, picpath = self.takescreen()
#     pic = cv2.imread(picpath)
#     gray_image = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
#     number = cv2.countNonZero(gray_image)
#     if number > 10:
#         result = False
#         errmsg = "不为全黑图像"
#     errDict["result"] = result
#     errDict["errmsg"] = errmsg
#     return errDict


# 从指定坐标拖动到另一个指定坐标
@allure.step('执行从指定坐标拖动到另一个指定坐标')
@DoStepAction(action_description='拖动')
def drag(fx, fy, dx, dy, times=1, duration=0.2):
    for i in range(times):
        print("Drag from %s %s to %s %s " % (fx, fy, dx, dy))
        # device.swipe(fx, fy, dx, dy, duration)
        device.drag(fx, fy, dx, dy, duration)
        time.sleep(0.5)


# 从指定坐标滑动到另一个指定坐标
@allure.step('执行从指定坐标滑动到另一个指定坐标')
@DoStepAction(action_description='滑动')
def swipe(fx, fy, dx, dy, times=1, duration=0.2):
    for i in range(times):
        print("Swipe from %s %s to %s %s " % (fx, fy, dx, dy))
        device.swipe(fx, fy, dx, dy, duration)
        # device.drag(fx, fy, dx, dy, duration)
        time.sleep(0.5)


@allure.step('执行滑动到end')
@DoStepAction(action_description='滑动到底')
def swipeEnd(self):
    device(scrollable=True).scroll.toEnd()
    return True


@allure.step('执行向左滑动')
@DoStepAction(action_description='向左滑动元素')
def swipeLeft(view=None, times=1):
    """
    :param times: 次数
    :param view: 元素
    :return:
    """
    x, y, width, height = getSwipeCoordinate(view)
    SwipeLeft(driver=device, size={'x': x, 'y': y, "width": width, "height": height}, n=times)


@allure.step('执行向右滑动')
@DoStepAction(action_description='向右滑动元素')
def swipeRight(view=None, times=1):
    """
    :param times: 次数
    :param view: 元素
    :return:
    """
    x, y, width, height = getSwipeCoordinate(view)
    SwipeRight(driver=device, size={'x': x, 'y': y, "width": width, "height": height}, n=times)
    return True,


@allure.step('执行向上滑动')
@DoStepAction(action_description='向上滑动元素')
def swipeUp(view=None, times=1):
    """
    :param times: 次数
    :param view: 元素
    :return:
    """
    x, y, width, height = getSwipeCoordinate(view)

    SwipeUp(driver=device, size={'x': x, 'y': y, "width": width, "height": height}, n=times)


@allure.step('执行向下滑动')
@DoStepAction(action_description='向下滑动元素')
def swipeDown(view=None, times=1):
    """
    :param times: 次数
    :param view: 元素
    :return:
    """
    x, y, width, height = getSwipeCoordinate(view)
    SwipeDown(driver=device, size={'x': x, 'y': y, "width": width, "height": height}, n=times)

# if __name__ == '__main__':
#     pic = takeViewImage(view='com.ecarx.multimedia:id/image_button_play', index=1)
#     print(pic)
