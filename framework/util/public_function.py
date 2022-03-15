# coding = utf-8
import random
import re


def FindAfterDotNumber(text):
    patter = re.compile(r'[\d]+[\.]([\d]*)')
    result = re.findall(patter, str(text))
    if result and len(result) > 0:
        return result[0]
    else:
        return None


def CheckContainsHanzi(text):
    patter_hanzi = re.compile(u'[\u4e00-\u9fa5]')
    if patter_hanzi.search(text):
        return True
    else:
        return False


def CheckContainsNumber(text):
    patter_number = re.compile(r'(^[1-9]+[\d]*\.\d+)|(^[1-9]+\d*)|(0\.\d+)|(0)')
    if patter_number.fullmatch(text):
        return True
    else:
        return False


def CheckContainsTimeText(text):
    patter_number = re.compile(r'[\d\s\-:\\]+')
    if patter_number.fullmatch(text):
        return True
    else:
        return False


def CheckContainsLetter(text):
    patter_letter = re.compile(r'[a-zA-Z]')
    if patter_letter.search(text):
        return True
    else:
        return False


def GetRandom(list_):
    if isinstance(list_, list):
        length = len(list_)
        if length == 1:
            index = 0
        else:
            index = random.randrange(0, length)
        return list_[index]


def ConvertTime(used_time):
    '''
    将毫秒转换成XX天XX小时XX分钟XX秒函数
    :return:
    '''
    nd = 24 * 60 * 60
    nh = 60 * 60
    nm = 60
    ns = 1
    diff = used_time
    # 计算差多少天
    day = int(diff // nd)
    # 计算差多少小时
    hour = int(diff % nd // nh)
    # 计算差多少分钟
    min = int(diff % nd % nh // nm)
    # 计算差多少秒 // 输出结果
    sec = int(diff % nd % nh % nm / ns)
    result = str(day) + "天" + str(hour) + "小时" + str(min) + "分钟" + str(sec) + "秒"
    return result



