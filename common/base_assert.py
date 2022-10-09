'''
Author: xiaomin
Date: 2020-12-17 15:51:37
'''
from common.log import MyLog
import re
import unittest
import colorama
colorama.init()

class Assertions:
    def __init__(self):
        self.log = MyLog()

    def assert_code(self,case_id,code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code==expected_code
            self.log.info("assert code--Success , status_code：[{}] == expected_code: [{}]".format(code,expected_code))
        except:
            self.log.error("\033[31m {}--statuscode error , status_code：[{}] != expected_code: [{}] \033[0m".format(case_id,code,expected_code))
            raise

    def re_compile(self,case_id,body,expected_msg):
        """
        正则匹配response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            pattern = re.compile(expected_msg)
            result = pattern.findall(body)
            #如果正则匹配不为空、None、0
            if result:
                self.log.info("assert response--Success ,expected_msg: [{}] in body: [{}]".format(expected_msg,body))
                self.log.info('执行成功')
            else:
                self.log.error("\033[31m {}--error ,expected_msg: [{}] not in body: [{}] \033[0m".format(case_id,expected_msg,body))
                raise Exception("{}--error ,expected_msg: [{}] not in body: [{}]".format(case_id,expected_msg,body))
                self.log.info('执行成功')

        except Exception as e:
            self.log.error("\033[31m {} \033[0m".format(e))
            self.log.info('执行失败')
            raise

    def assert_in_text(self,case_id,body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            # text = json.dumps(body, ensure_ascii=False)
            # # print(text)
            assert expected_msg in body
            self.log.info("assert response--Success ,expected_msg: [{}] in body: [{}]".format(expected_msg,body))
            self.log.info('执行成功')
        except:
            self.log.error("\033[31m {}--error ,expected_msg: [{}] not in body: [{}] \033[0m".format(case_id,expected_msg,body))
            self.log.info('执行失败')
            raise

    # def assert_notin_text(self,case_id,body, expected_msg):
    #     """
    #     验证response body中是否不包含预期字符串
    #     :param body:
    #     :param expected_msg:
    #     :return:
    #     """
    #     try:        
    #         assert expected_msg not in body
    #         self.log.info("assert no in--Success ,body：[{}] not in expected_msg: [{}]".format(body,expected_msg))
    #     except:
    #         self.log.error("\033[31m {}--error ,body：[{}] not in expected_msg: [{}] \033[0m".format(case_id,body,expected_msg))
    #         raise
    # def assert_text(self, body, expected_msg):
    #     """
    #     验证response body中是否等于预期字符串
    #     :param body:
    #     :param expected_msg:
    #     :return:
    #     """
    #     try:
    #         assert body == expected_msg
    #         self.log.info("--Success ,body：[{}] == expected_msg: [{}]".format(body,expected_msg))
    #     except:
    #         self.log.error("\033[31m --error ,body：[{}] != expected_msg: [{}] \033[0m".format(body,expected_msg))
    #         raise
    # def assert_body(self, body, body_msg, expected_msg):
    #     """
    #     验证response body中任意属性的值
    #     :param body:
    #     :param body_msg:
    #     :param expected_msg:
    #     :return:
    #     """
    #     try:
    #         msg = body[body_msg]
    #         assert msg == expected_msg
    #         self.log.info("--Success ,Response body msg == expected_msg, expected_msg is [{}], body_msg is [{}]".format(expected_msg, body_msg))
    #     except:
    #         self.log.error("Response body msg != expected_msg, expected_msg is [{}], body_msg is [{}]".format(expected_msg, body_msg))
    #         raise