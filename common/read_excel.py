'''
Author: xiaomin
Date: 2020-12-16 15:44:03
'''
from common.log import MyLog
import time
import xlrd
import os
import sys
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def read_xlrd(excel_file):
    '''读取excel所有数据'''
    try:
        data = xlrd.open_workbook(excel_file)
        # table=data.sheet_by_index(0)
        sheets = data.sheet_names()
        datafile = []
        now = int(round(time.time() * 1000))
        for sheet in sheets:
            table = data.sheet_by_name(sheet)
            for rowNum in range(table.nrows):
                # 去掉表头,替换时间戳标志
                if rowNum > 0:
                    rowdata = table.row_values(rowNum)
                    rowData = [str(i).replace('<time_stamp>', str(now))
                               for i in rowdata]
                    datafile.append(rowData)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return datafile


class InitData():
    '''初始化excel数据'''

    def __init__(self, datafile, case_no):
        # case_no用例编号索引
        # self.datafile=
        self.datafile = datafile
        self.case_id = ''
        self.case_module = ''
        self.case_name = ''
        self.username = ''
        self.password = ''
        self.method = ''
        self.url_path = ''
        self.api_type = ''
        self.headers = ''
        self.request_body = ''
        self.status_code = ''
        self.resp_expect = ''
        self.save_data = ''
        self.use_data = ''
        self.case_no = case_no

    def get_data(self):
        self.case_id = self.datafile[self.case_no][0]
        self.case_module = self.datafile[self.case_no][1]
        self.case_name = self.datafile[self.case_no][2]
        self.username = self.datafile[self.case_no][3]
        self.password = self.datafile[self.case_no][4]
        self.method = self.datafile[self.case_no][5]
        self.url_path = self.datafile[self.case_no][6]
        self.api_type = self.datafile[self.case_no][7]
        self.headers = self.datafile[self.case_no][8]
        self.request_body = self.datafile[self.case_no][9]
        self.status_code = self.datafile[self.case_no][10]
        self.resp_expect = self.datafile[self.case_no][11]
        self.save_data = self.datafile[self.case_no][12]
        self.use_data = self.datafile[self.case_no][13]


if __name__ == "__main__":
    excel_file = '../test_case_data.xlsx'
    # testcase=read_xlrd(excel_file)
    # print(testcase[1][1])
    a = InitData(excel_file, 2)
    a.get_data()
    print(a.case_id)
    # print(a.case_name)
    # eval(a.headers)
    # print(a.headers)
