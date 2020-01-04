import os
import re

if __name__ == '__main__':
    readLines = os.popen('netsh wlan show profiles')
    print('********************')
    wifiNameList = []
    for line in readLines:
        arr = re.sub(r'\s+', '', line, count=3).split(':', 1)
        if arr.__len__() > 1 and arr[1].__len__() != 0:
            wifiNameList.append(re.sub(r'[\r\n]', '', arr[1]))
    i = 0
    for wifiName in wifiNameList:
        i += 1
        print('(%d): %s' % (i, wifiName))
    print('好多WiFi，挑一个吧，输入前面的序号', end='：')
    num = input()
    wlanLines = os.popen('netsh wlan show profile name=' + wifiNameList[int(num) - 1] + ' key=clear')
    for wlan in wlanLines:
        arr = re.sub(r'\s+', '', wlan).split(':')
        if arr[0] == '关键内容':
            print('密码：%s' % arr[1])
