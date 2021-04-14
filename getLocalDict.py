import requests
import json

dictionarys = {}


def loadDict():
    response = requests.get(url='http://words.mjclouds.com/getDict.php')
    strData = response.content.decode('UTF-8')  # 对返回的数据进行解码
    dictData = json.loads(strData)  # 转换为字典
    # print(dictData)
    dictionarys = []
    try:
        if dictData['status'] == 'true':
            for key in dictData:
                if key == 'status':
                    continue
                for ikey in dictData[key]:
                    temp = {
                        'EN': dictData[key]['english'],
                        'ZH': dictData[key]['chinese']
                    }
                    # print(temp)
                    dictionarys.append(temp)
                    break
    except IndexError:
        dictionarys = []
    return dictionarys


def init():
    global dictionarys
    dictionarys = loadDict()
    return dictionarys


if __name__ == "__main__":
    init()
    print(dictionarys)
