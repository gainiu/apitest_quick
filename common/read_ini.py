'''
Author: xiaomin
Date: 2020-12-16 17:35:08
'''
import configparser
from common.log import MyLog
from config import file_path
import os
import sys
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def read_inifile():
    # 读取配置
    try:
        config = configparser.ConfigParser()
        config.read(file_path.config_file)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return config


class GetIni:
    def __init__(self, inikey, inivalue, newvalue=None):
        self.inikey = inikey
        self.inivalue = inivalue
        self.newvalue = newvalue
        self.config = read_inifile()

    def get_ini(self):
        # 返回配置文件的某项参数值
        try:
            convalues = self.config.get(self.inikey, self.inivalue)
        except Exception as e:
            MyLog.error('\033[31m {} \033[0m'.format(e))
            raise

        return convalues

    def write_ini(self):
        # 修改配置文件的某项参数值
        try:
            self.config.set(self.inikey, self.inivalue, self.newvalue)
            self.config.write(open(file_path.config_file, 'w'))
        except Exception as e:
            MyLog.error('\033[31m {} \033[0m'.format(e))
            raise


if __name__ == '__main__':
    # print(get_ini('login_token','Authorization'))
    # write_ini('http_token','access_token','aaa')
    pass
