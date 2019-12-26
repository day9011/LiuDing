#coding=utf-8

from utils.Log import get_log
import pymysql
import os
import datetime
import json
import redis


logger = get_log()

class RedisCli(object):
    def __init__(self, timeout=None):
        self.__host = os.environ['REDIS_HOST'].strip()
        self.__port = os.environ['REDIS_PORT'].strip()
        self.__password = os.environ['REDIS_PASS'].strip()
        self.__timeout = timeout
        self.__pool = None
        self.__client = None
        self.connect()

    # def __init__(self, host, username, password, database):
    #     try:
    #         self.__host = host
    #         self.__username = username
    #         self.__password = password
    #         self.__database = database
    #     except Exception as e:
    #         print(str(e))



    def check_command(self, sql):
        return True

    def connect(self): 
        try:
            self.__pool = redis.ConnectionPool(host=self.__host,
                                            password=self.__password,
                                            port=self.__port,
                                            db=0,
                                            socket_connect_timeout=self.__timeout)
            self.__client = redis.Redis(self.__pool)
            self.__client.get("username")
            return True
        except Exception as e:
            info = {'interface': "RedisConnect", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)  
            return False          

    def check_alive(self):
        try:
            if self.__client is not None:
                self.__client.get("username")
                return True
            else:
                return False
        except Exception as e:
            info = {'interface': "RedisCheck", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)  
            return False
        
    def get_redis(self):
        if self.check_alive():
            return self.__client
        else:
            if self.connect():
                return self.__client
            else:
                return False
            