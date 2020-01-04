import pip
import os
import re
import sys

if __name__ == '__main__':
    print("Python版本：[%s]  Pip版本：[%s]" % (sys.version, pip.__version__))
    print('开始获取更新列表')
    # 通过执行命令获取有更新的模块列表
    r = os.popen("pip list --outdated")
    # 获取命令返回的列表
    infos = r.readlines()
    # 定义一个数组存放要更新的模块名称
    modulesName = []
    # 循环遍历返回的列表
    i = 0
    for line in infos:
        print(line, end='')
        # 为什么要大于等于2的是时候才更新呢？你猜猜
        if i >= 2:
            # 通过正则把空格符号替换成"|"，然后按照"|"分割字符串得到一个数组
            # 数组的下标为0的元素就是模块名称
            modulesName.append(re.sub('\s+', '|', line).split('|')[0])
        i += 1
    # 遍历模块名称，挨个更新
    errorModulesName = []
    for name in modulesName:
        print("更新模块：%s" % name)
        # 执行更新命令
        exitCode = os.system("pip install --upgrade " + name)
        print("状态：%d" % exitCode)
        if exitCode != 0:
            errorModulesName.append(name)
    print("总共数量：[%d]" % modulesName.__len__())
    print("成功数量：[%d]" % (modulesName.__len__() - errorModulesName.__len__()))
    print("失败数量：[%d]" % errorModulesName.__len__())
    print("失败的模块：[%s]" % errorModulesName)
