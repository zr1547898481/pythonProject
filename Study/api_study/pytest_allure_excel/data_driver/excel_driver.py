# coding=utf-8
import openpyxl
from Study.api_study.pytest_allure_excel.VAR.var import *

def load_excel():
    # 打开excel文件
    wb = openpyxl.load_workbook(EXCEL_PATH4)
    # 获取页签
    sheet = wb['Sheet1']
    list = []
    # 按行循环读取文件,sheet.values为对应的文件内容
    for value in sheet.values:
        # 判断每一行开头内容是否为int类型数字编号,过滤掉表头
        if type(value[0]) is int :
            list.append(value)
    return list

if __name__ == '__main__':
    # 此时的值为字典格式的字符串
    print(load_excel())