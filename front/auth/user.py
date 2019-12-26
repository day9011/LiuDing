#coding=utf-8

from lib.Redis import RedisCli
import time
import datetime
import json


class User:
    def __init__(self, timeout=None):
        self.redis_cli = RedisCli(timeout)
        self.timeout = timeout


    def check_user(self, username):
        try:
            user_redis = self.redis_cli.get_redis()
            redis_r = user_redis.get(username)
            if redis_r:
                status, mes = keep_user_alive(username, self.timeout)
                if status:
                    return True, mes
                else:
                    return False, mes
            else:
                return False, '{} timeout'.format(username)
        except Exception as e:
            return False, str(e)

    def insert_user_info(username, user_dict):
        try:
            user_redis = self.redis_cli.get_redis()
            user_dict['time'] = time.time()
            user_str = json.dumps(user_dict, ensure_ascii=False)
            if user_redis.set(username, user_dict, ex=self.timeout):
                ret_str = '{} insert info successfully'.format(username)
                return True, ret_str
            else:
                ret_str = '{} insert failed'.format(username)
                return False, ret_str
        except Exception as e:
            return False, str(e)

    def keep_user_alive(username, timeout=None):
        try:
            user_redis = self.redis_cli.get_redis()
            redis_r = user_redis.get(username)
            if redis_r:
                try:
                    user_str = redis_r.decode('utf-8')
                except:
                    user_str = redis_r.decode('utf-8')
                user_dict = json.loads(user_str)
                user_dict['time'] = datetime.datetime.now()
                insert_str = json.dumps(user_dict, ensure_ascii=False)
                user_redis.set(username, insert_str, ex=timeout)
                return True, 'OK'
            else:
                return False, '{} timeout'.format(username)
        except Exception as e:
            return False, str(e)