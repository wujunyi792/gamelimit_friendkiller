import psutil
from easygui import *
import random
import json
import getLocalDict
import requests
import time
import win32api

banList = ['launcher.exe', 'wegame.exe', 'Client.exe']


def loadSetting():
    _dic = {}
    try:
        f = open('setting.txt', 'r')
        _dic = eval(f.read())
        f.close()
    except:
        f = open('setting.txt', 'w')
        f.close()
    return _dic


def saveSetting(dic):
    f = open('setting.txt', 'w')
    f.write(str(dic))
    f.close()


def getRandom(A, B, COUNT):
    resultList = random.sample(range(A, B + 1), COUNT)
    return resultList


def vaf():
    version = "20210414"
    response = requests.get(url='http://words.mjclouds.com/tmp.php?version=' + version)
    strData = response.content.decode('UTF-8')  # 对返回的数据进行解码
    dictData = json.loads(strData)  # 转换为字典
    if dictData['status'] == 'false':
        print(dictData['msg'])
        vaf()

    dictss = getLocalDict.init()
    dicts = random.sample(dictss, int(dictData['count']))
    msgbox(dictData['count'] + f"道题, 做对{int(int(dictData['count']) * 0.8)}道题，你就可以开始游戏!", "提示")
    msgbox("判断翻译是否准确，正确则选择y，错误则选择n\n游戏开始", "游戏规则")
    count = 0
    right = 0
    wrongList = []
    liist = getRandom(1, len(dicts), random.randint(1, int(len(dicts) / 2)))
    msgbox(f"总共有{len(liist)}道选 n 的题目！！！", "温馨提示")
    for dic in dicts:
        count += 1
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if count in liist:
            opt = boolbox(title=f"第{count}题", msg=dic['EN'] + "   " + dictss[random.randint(0, 5000)]['ZH'])
            if not opt:
                right += 1
                # print("\033[32mbingo\033[0m")
                continue
            # print("\033[31m还不背英语去?\033[0m")
            wrongList.append(dic['EN'] + "   " + dic['ZH'])
            continue

        opt = boolbox(title=f"第{count}题", msg=dic['EN'] + "   " + dic['ZH'])
        if opt:
            right += 1
            # print("\033[32mbingo\033[0m")
            continue
        # print("\033[31m还不背英语去?\033[0m")
        wrongList.append(dic['EN'] + "   " + dic['ZH'])
        continue

    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++\n标答；")
    msgbox(title="结果", msg=f"你一共做了{dictData['count']}道题，做对了{right}道,正确率{right / int(dictData['count'])}")
    for msg in wrongList:
        # tkinter.messagebox.showinfo("你做错的题, 请过目", dic['EN'] + "   " + dic['ZH'])
        msgbox(title="你做错的题, 请过目", msg=msg)
    if right >= int(dictData['count']) * 0.8:
        msgbox(title="恭喜", msg="恭喜你，可以快乐游戏")
        return True
    else:
        msgbox(title="警告", msg="还不滚去学习?")
        return False


def run():
    pidlist = psutil.process_iter()
    for proc in pidlist:
        if proc.name() in banList:
            # print("catch!")
            pid = proc.pid
            location = psutil.Process(pid).exe()
            proc.kill()
            if vaf():
                try:
                    msgbox(title="提示", msg="一小时后会准时关闭游戏，无论你是否正在游戏中！")
                    setting['time'] = time.time()
                    saveSetting(setting)
                    win32api.ShellExecute(0, 'open', location, '', '', 1)
                    return True
                except:
                    msgbox(title="警告", msg="启动失败，请联系作者")
            else:
                break
    return False


if __name__ == "__main__":
    loadSetting()
    while True:
        setting = loadSetting()
        if 'time' in setting:
            now = time.time()
            # print(float(now) - setting['time'])
            if float(now) - setting['time'] < 3600:
                continue
        run()
