'''
Author: xiaomin
Date: 2020-12-16 17:06:22
'''
from pytest import param
from common.log import MyLog
from common.read_ini import GetIni
from common import trans_json
import jsonpath
import requests
import os
import sys
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def set_headers(headers, access_token):
    # 设置header
    try:
        # if headers != '' and 'Authorization' not in headers:
        #     # headers转换成dict，添加token，url拼接
        #     headers = trans_json.json_loads(headers)
        #     headers['Authorization'] = token_type+' '+access_token
        headers = trans_json.json_loads(headers)
        headers['token'] = access_token
        # MyLog.info(print(headers))
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return headers


def set_urls(api_type, url):
    # 拼接完整url
    try:
        login_url = GetIni('login_url', 'login_url').get_ini()
        http_url = GetIni('http_url', 'http_url').get_ini()
        if api_type == 'oauth':
            # 如果是ouath接口
            url = login_url+url
        else:
            url = http_url+url
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return url


def print_log(method, url, params):
    print('url:[{}] {}'.format(method, url))
    print('request: {}'.format(params))
    MyLog.info('url:[{}] {}'.format(method, url))
    MyLog.info('request: {}'.format(params))


def request_post(url, headers, params, api_type):
    # post方法
    try:
        access_token = GetIni('http_token', 'access_token').get_ini()
        url = set_urls(api_type, url)
        print_log('POST', url, params)
        headers = set_headers(headers,access_token)
        response = requests.post(url=url, headers=headers, data=params)
        MyLog.info(response.text)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return response


def request_get(url, headers, api_type, params=None):
    # get方法
    try:
        access_token = GetIni('http_token', 'access_token').get_ini()
        url = set_urls(api_type, url)
        print_log('GET', url, params)
        headers = set_headers(headers, access_token)

        if params:
            params = trans_json.json_loads(params)
            response = requests.get(url=url, headers=headers, params=params)
        else:
            response = requests.get(url=url, headers=headers)
        MyLog.info(response.text)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return response

def request_delete(url, headers, api_type, params=None):
    # delete方法
    try:
        access_token = GetIni('http_token', 'access_token').get_ini()
        url = set_urls(api_type, url)
        print_log('DELETE', url, params)
        headers = set_headers(headers, access_token)

        if params:
            params = trans_json.json_loads(params)
            response = requests.delete(url=url, headers=headers, params=params)
        else:
            response = requests.delete(url=url, headers=headers)
        # MyLog.info(response.text)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return response


def save_response(res, save_id, save_key, temporary_data):
    # 请求响应保存字典
    res = trans_json.json_loads(res)
    key = save_id
    res_value = jsonpath.jsonpath(res,save_key)
    temporary_data[key] = str(res_value[0])
    return temporary_data


def trans_usedata(origin_data, use_data, temporary_data):
    # 替换body中关联字段
    new_data = origin_data.replace(use_data, temporary_data[use_data])
    return new_data


if __name__ == '__main__':
    pass
    # print(request_post('/user2/app/app','{"Content-Type":"application/json"}','{"appKey":"aaaaa","description":"hhhh","name":"autotest_","status":false}','json'))
