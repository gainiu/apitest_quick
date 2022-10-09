'''
Author: xiaomin
Date: 2020-12-18 09:34:07
'''
import json
from common.log import MyLog

def json_dumps(data):
    try:
        newdata=json.dumps(data)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

    return newdata

def json_loads(data):
    try:
        newdata=json.loads(data)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    
    return newdata