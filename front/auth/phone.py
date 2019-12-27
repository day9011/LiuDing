#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random
from lib.Redis import RedisCli
import json
import re
import os, sys


class PhoneVerify:
    def __init__(self, logger, timeout=600):
        self.key_id = os.environ['PHONE_KEY']
        self.secret = os.environ['PHONE_SECRET']
        self.client = AcsClient(self.key_id, self.secret, "cn-hangzhou")
        self.cli = RedisCli()
        self.redis_cli = self.cli.get_redis()
        self.timeout = timeout
        self.logger = logger

    def init(self):
        self.client = AcsClient(self.key_id, self.secret, "cn-hangzhou")

    def send_code(self, phone_number):
        try:
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('https') # https | http
            request.set_version('2017-05-25')
            request.set_action_name('QuerySendDetails')
            verify_code = self.make_verify_code()
            self.redis_cli.set('PhoneVerify_{}'.format(phone_number), verify_code, ex=self.timeout)
            welcome_str = "欢迎使用柳丁教育系统电话验证，您这次的验证码为: {}".format(verify_code)
            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('PhoneNumber', phone_number)
            request.add_query_param('SendDate', welcome_str)
            request.add_query_param('PageSize', "1")
            request.add_query_param('CurrentPage', "1")
            response = self.client.do_action(request)
            self.logger.info(str(response, encoding = 'utf-8'))
            response = json.loads(str(response, encoding = 'utf-8'))
            if response['Code'].strip() != 'OK':
                raise Exception(response['Message'])
            return True
        except Exception as e:
            info_dict = {'interface': 'PhoneVerify send_code', 'error': str(e)}
            info_str = json.dumps(info_dict, ensure_ascii=False)
            self.logger.error(info_str)
            self.init()
            return False

    def make_verify_code(self):
        return str(random.randint(0, 999999)).zfill(6)
    
    def verify_code(self, phone_number, code):
        true_code = self.redis_cli.get('PhoneVerify_{}'.format(phone_number))
        if true_code != code:
            return False
        else:
            return True
