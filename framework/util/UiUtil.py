import os
import cv2

import numpy as np

from config.pytest_config import Const


def SwipeUp(driver, size, n=1):
    """向上屏幕滑动"""
    x = size['x']
    y = size['y']
    x1 = size["width"] * 0.5 + x  # x坐标
    y1 = size["height"] * 0.8 + y  # 起点 y坐标
    y2 = size["height"] * 0.2 + y  # 终点 y 坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2)


def SwipeUpWheel(driver, size, t=100, n=1):
    """向上屏幕滑动"""
    x = size['x']
    y = size['y']
    x1 = size["width"] * 0.5 + x  # x坐标
    y1 = size["height"] * 0.6 + y  # 起点 y坐标
    y2 = size["height"] * 0.4 + y  # 终点 y 坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t / 10000)


def SwipeDown(driver, size, n=1):
    """向下屏幕滑动"""
    x = size['x']
    y = size['y']
    x1 = size["width"] * 0.5 + x  # x1 坐标
    y1 = size["height"] * 0.2 + y  # 起点y1坐标
    y2 = size["height"] * 0.8 + y  # 终点y2坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2)


def SwipeDownWheel(driver, size, t=100, n=1):
    """向下屏幕滑动"""
    x = size['x']
    y = size['y']
    x1 = size["width"] * 0.5 + x  # x1 坐标
    y1 = size["height"] * 0.5 + y  # 起点y1坐标
    y2 = size["height"] * 0.7 + y  # 终点y2坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t / 1000)


def SwipeLeft(driver, size, t=100, n=1):
    """向左屏幕滑动"""
    x = size['x']
    y = size['y']
    x1 = size["width"] * 0.8 + x  # 起点x1坐标
    y1 = size["height"] * 0.5 + y  # y1 坐标
    x2 = size["width"] * 0.2 + x  # 终点x2坐标
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t / 1000)


def SwipeRight(driver, size, t=100, n=1):
    """向右屏幕滑动"""
    x = size['x']
    y = size['y']
    x1 = size["width"] * 0.2 + x  # 起点x1坐标
    y1 = size["height"] * 0.5 + y  # y1坐标
    x2 = size["width"] * 0.8 + x  # 终点x2坐标
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t / 1000)
