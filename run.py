'''
Author: xiaomin
Date: 2020-12-17 14:11:08
'''
import time
import unittest
from BeautifulReport import BeautifulReport
from common.read_excel import InitData
from common import read_excel
from common import base_run
from common.log import MyLog
from config import file_path
import os
import sys
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == "__main__":
    # 读取测试用例
    datafile = read_excel.read_xlrd(file_path.test_data)
    case_numbers = len(datafile)

    # 临时字典存储需要关联的数据
    temporary_data = {}

    # 获取当前时间
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    # 定义报告存放路径
    filename = file_path.report_file+now+'result.html'
    # 创建unittest套件
    testsuit = unittest.TestSuite()

    with open(filename, 'wb') as fp:
        # 遍历所有用例
        MyLog.info('************开始测试************')
        for case_num in range(case_numbers):
            data = InitData(datafile, case_num)
            data.get_data()
            # 创建测试类
            newTestCase = type(data.case_module, (unittest.TestCase,), {
                               'data': data, 'title': data.case_name, 'temporary_data': temporary_data, 'tearDown': base_run.teardown, 'setUp': base_run.setup, data.case_id: base_run.test_case},)
            # 测试类加入unittest套件
            testsuit.addTest(unittest.TestLoader(
            ).loadTestsFromTestCase(newTestCase))

        run = BeautifulReport(testsuit)
        run.report(filename=filename, description='autoapi测试报告')
        MyLog.info('************完成测试************')
