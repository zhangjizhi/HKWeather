# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 18:28
# @Author  : zjz
import allure

from framework.public_functions.device_driver import getWidget, getViewStrByConfig, swipeDown, swipeUp
from framework.pulbic_helper import DoStepAction, findListByIndex, findDupList


@allure.step('执行获取所有子元素text')
@DoStepAction(action_description='查找所有子元素text')
def getChildrenText(parentView, view, parentIndex=None, index=None):
    widget = getWidget(parentView, parentIndex)
    if widget is not None:
        viewStr = getViewStrByConfig(view)
        if ':id/' in viewStr:
            children = [x.get_text() for x in widget.child(resourceId=viewStr)]
        else:
            children = [x.get_text() for x in widget.child(text=viewStr)]
        if index is not None:
            return findListByIndex(children, index)
        else:
            return children


@allure.step('执行检查列表有指定内容')
@DoStepAction(action_description='检测列表text')
def checkListContent(view, text, listView, falseText=None):
    widget = getChildrenText(listView, text)
    if widget:
        return {'result': True, 'errMsg': ''}
    if falseText:
        widget = getChildrenText(listView, view, falseText)
        if widget:
            return {'result': False, 'errMsg': f'出现{falseText}'}
    repeat = 3
    last_text = getWidget(view, index='last').get_text()
    while repeat > 0:
        swipeUp(listView)
        widget = getChildrenText(listView,text)
        if widget:
            return {'result': True, 'errmsg': ''}
        current_text_last = getWidget(view=view, index='last').get_text()
        if current_text_last != last_text:
            last_text = current_text_last
            repeat = 3
        else:
            repeat -= 1
    return {'result': False, 'errMsg': f'未出现{text}'}


@allure.step('执行通过元素特定值获取列表中的文字')
@DoStepAction(action_description='检测列表text')
def getListTextsByViewValue(view, value, brothers, listview):
    repeat = 3
    last_text = getWidget(view, index='last').get_text()
    while repeat > 0:
        texts = getChildrenText(listview, view)
        index = list(texts).index(value) if value in texts else None
        if index is not None:
            result = {}
            for brother in brothers:
                result[brother] = getChildrenText(listview, brother, 0, index)
            return {value: result}
        swipeUp(listview)
        current_text_last = getWidget(view=view, index='last').get_text()
        if current_text_last != last_text:
            last_text = current_text_last
            repeat = 3
        else:
            repeat -= 1
    return {'result': False, 'errMsg': f'未出现{value}'}


@allure.step('执行获取列表所有内容')
@DoStepAction(action_description='获取列表所有内容')
def getAllListContent(view, listView):
    texts = []
    swipNumber = 0
    while True:
        currentTextList = getChildrenText(listView, view)
        if currentTextList:
            if swipNumber == 0:
                swipNumber = len(currentTextList) / 2
            if texts:
                text = '#@'.join(texts)
                currentText = '#@'.join(currentTextList)
                if text.endswith(currentText):
                    break
                else:
                    needAdd = [currentTextList.pop()]
                    count = len(currentTextList)
                    while count > swipNumber:
                        currentText = '#@'.join(currentTextList)
                        if text.endswith(currentText):
                            break
                        else:
                            needAdd.insert(0, currentTextList.pop())
                        count = len(currentTextList)
                    texts.extend(needAdd)
            else:
                texts.extend(currentTextList)
            swipeDown(listView)
        else:
            raise {'result': True, 'errMsg': f'没有对应的元素{view}'}
    return {'result': True, 'text': texts}


if __name__ == '__main__':
    pass
