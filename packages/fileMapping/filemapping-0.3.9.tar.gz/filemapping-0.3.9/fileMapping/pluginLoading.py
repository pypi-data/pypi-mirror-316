"""
这个文件用于加载插件
plugIns
"""
import os
import ast
import importlib
# import importlib.util
import sys
from typing import Any
import inspect as inspectKB
import copy

from rich import inspect

from . import empty as Empty
from . import config


"""
empty 一个空 函数/方法
    - 当导入错误时，触发空函数，为了防止调用错误

method 公共方法

packageMethod(method)  包类
    
fileMethod(method)  文件类

f 调用函数
"""
class blacklist: ...


class empty:
    # 一个空函数/方法
    class main:
        def __init__(self): ...

    def run(self, **kwargs): ...

    def __init__(self):
        self.main = self.main()


class method:
    def __init__(self, path):
        self.pointer = None
        self.pack: Any| empty
        self.magicParameters: dict[str: Any] = {}
        # 调用对象
        self.path: str = path
        self.absolutePath = self.path if os.path.isabs(self.path) == True else os.path.realpath(self.path)
        # 相对路径 & 绝对路径
        self.importThePackage()
        # 导入包

    def run(self, **kwargs):
        """
        运行包
        :return:
        """
        try:
            sig = inspectKB.signature(self.pointer)
            parameterFilling = self.parameterFilling(list(sig.parameters.keys()), kwargs)

            return self.pointer(**parameterFilling)

        except config.error_list_a2 as e:
            return e

    def parameterFilling(self, parameter: list, kwargs: dict):
        """
        填充参数
        :param parameter: 参数列表
        :param kwargs: 关键字参数
        :return:
        """
        return {
            key: value for key, value in kwargs.items() if key in parameter
        }

    def get(self, func):
        return {
            value: getattr(func, value) if value in dir(func) else config.functions[value]
            for value, data in config.functionsName.items()
        }

    def importThePackage(self):
        """
        导入包
        :return:
        """
        try:
            self.pack = impo(
                os.path.dirname(self.absolutePath), os.path.basename(self.path)
            )  # 导入包
            if isinstance(self.pack, config.error_list_a2):
                raise self.pack

            builtInParameters = self.get(self.pack)
            # 获取包内的内定参数 & 没有就向config.functions中获取

        except config.error_list_a2 as e:
            printlog(f"file: {self.path}\n导入错误 log: {e}", printLog=config.log['printLog'], color='31', printPosition=config.log['printPosition'])

            self.pack = empty()
            builtInParameters = config.functions_bad

        if builtInParameters[config.functionsName['__run__']] is False:
            # 禁止运行
            self.pointer = empty().run
            return False

        elif builtInParameters[config.functionsName['__function__']] == '':
            self.pointer = empty().run
            return True

        elif builtInParameters[config.functionsName['__function__']] in dir(self.pack):
            self.pointer = getattr(self.pack, builtInParameters[config.functionsName['__function__']])

        if self.pointer is None:
            # 无 main
            printlog(f"file: {self.path}\n导入错误 main函数: 包没有main函数", printLog=config.log['printLog'], color='31', printPosition=config.log['printPosition'])


class packageMethod(method):
    """包方法"""
    __name__ = 'packageMethod'


class fileMethod(method):
    """文件方法"""
    __name__ = 'fileMethod'


def f(path: os.path) -> packageMethod | fileMethod | bool:
    """
    计划弃用

    判断 path 是否为 包/文件
    :return: 包 packageMethod 文件 fileMethod
    """
    def package(path: os.path, ) -> bool:
        """
        判断是否为包
        __init__.py & main.py
        :return: bool
        """
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, "__init__.py")):
            # 判断函数是否是为包
            return True

        return False

    def file(path: os.path) -> bool:
        """
        判断是否 是一个可调用文件
        :return: bool
        """
        # if os.path.isfile(path) and path.split('.')[-1] == 'py':
        #     with open(path, encoding='utf-8') as f:
        #         tree = ast.parse(f.read())
        #
        #     functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        #     # 获取类型和函数
        #     if 'main' in functions:
        #         return True
        #
        # printlog(f"file: {path}\n导入错误 main函数: py文件没有main函数", printLog=config.log['printLog'], color='31', printPosition=config.log['printPosition'])
        # return False
        return True

    if os.path.isdir(path) and package(path):
        return packageMethod(path)

    elif os.path.isfile(path) and file(path):
        return fileMethod(path)

    else:
        return False


def impo(file_path: os.path, callObject: str):
    """
    :param callObject: 'main'
    :param file_path: 绝对路径
    :return:

    """
    path = copy.copy(sys.path)
    callObject = callObject.split('.')[0]  # 去除 .py
    try:
        sys.path = config.path+[file_path]
        the_api = importlib.import_module(callObject)

    except config.error_list_a2 as e:
        sys.path = path
        return e

    else:
        sys.path = path
        return the_api


def printlog(log: str, printPosition: sys.stdout = sys.stdout, color: str = '32', printLog: bool = True):
    """
    打印日志
    :param log: 日志
    :param printPosition: 打印位置
    :param color: 颜色 31红色 32绿色 33黄色 34蓝色 35紫色 36青色 37白色
    :return:
    """
    if printLog is True:
        print(f"\033[1;{color}m{log}\033[0m", file=printPosition)
        return True

    else:
        return True



