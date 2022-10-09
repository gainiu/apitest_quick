'''
Author: xiaomin
Date: 2020-12-16 17:28:43
'''
import requests
from common.log import MyLog
from common.base_assert import Assertions
from common import request_func
from common import trans_json
from common.read_ini import GetIni
from common.read_excel import InitData
import os
import sys
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def setup(self):
    # 每个用例执行前调用,判断是否需要登录新账号
    try:
        if self.data.username and self.data.username != '/':
            # 用例需要切换账号登录时，获取用户名密码登录，返回token写入config.ini
            param = {
                'username': self.data.username,
                'password': self.data.password
            }
            param = trans_json.json_dumps(param)
            # 获取登录url
            login = GetIni('login_url', 'login').get_ini()
            # 登录headers
            headers = {'Content-Type': 'application/json'}
            headers = trans_json.json_dumps(headers)
            # 登录requests
            response = request_func.request_post(
                login, headers, param,'web')
            # 返参json解析
            response_data = trans_json.json_loads(response.text)
            # 新用户token写入配置
            GetIni('http_token', 'access_token',
                   response_data['data']['Token']).write_ini()
            # read_ini.write_ini('http_token','access_token',response_data['access_token'])
        else:
            pass
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise


def teardown(self):
    pass


def test_case(self):
    # 测试函数
    try:
        MyLog.info('------[正在执行：{}]------'.format(self.data.case_id))

        # 如果use_data有值，则把request_body和resp_expect进行替换
        if self.data.use_data:
            self.data.request_body = request_func.trans_usedata(
                self.data.request_body, self.data.use_data, self.temporary_data)
            self.data.resp_expect = request_func.trans_usedata(
                self.data.resp_expect, self.data.use_data, self.temporary_data)
            self.data.url_path = request_func.trans_usedata(
                self.data.url_path, self.data.use_data, self.temporary_data)

        if self.data.method == 'POST':
            # post请求
            res = request_func.request_post(
                self.data.url_path, self.data.headers, self.data.request_body, self.data.api_type)
        elif self.data.method == 'GET':
            # get请求
            res = request_func.request_get(
                self.data.url_path, self.data.headers, self.data.api_type, self.data.request_body)
        elif self.data.method == 'DELETE':
            # delete请求
            res = request_func.request_delete(
                self.data.url_path, self.data.headers, self.data.api_type, self.data.request_body)

        # 打印信息至报告
        print_report(res.status_code, res.text, int(
            float(self.data.status_code)), self.data.resp_expect)

        # 如果save_data有值，则对response进行保存到临时字典temporary_data
        # 保存格式为{"testcase001id":xxx}
        if self.data.save_data:
            request_func.save_response(
                res.text, self.data.case_id, self.data.save_data, self.temporary_data)

    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    # 实例化断言
    assertion = Assertions()
    # 状态码断言
    assertion.assert_code(self.data.case_id, res.status_code,
                          int(float(self.data.status_code)))
    # 返参断言
    if '(.*?)' in self.data.resp_expect:
        assertion.re_compile(self.data.case_id, res.text,
                             self.data.resp_expect)
    else:
        assertion.assert_in_text(
            self.data.case_id, res.text, self.data.resp_expect)


def print_report(status_code, text, assert_code, resp_expect):
    # 打印code,response,expectcode,expectres
    print('status code: {}'.format(status_code))
    print('response: {}'.format(text))
    print('assert code: {}'.format(assert_code))
    print('assert response: {}'.format(resp_expect))


if __name__ == '__main__':
    # test_case()
    pass
