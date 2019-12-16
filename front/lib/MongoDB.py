#coding=utf-8

from utils.Log import get_log
import pymongo
import os
import datetime


logger = get_log()

class MongoDB(object):
    def init(self, dbname, collection):
        try:
            self.__mongohost = os.environ['MONGO_URI'].strip()
            self.__dbname = dbname
            self.__collection = collection
            self._time_format = '%Y-%m-%d %H:%M:%S'
            return self.__connect()
        except Exception as e:
            print(str(e))
            return False

    def __connect(self):
        self.__conn = pymongo.MongoClient(self.__mongohost.rstrip('/') + '/' + self.__dbname)
        self.__db = self.__conn[self.__dbname]
        self.__col = self.__db[self.__collection]
        return self.__check_connected()


    def __check_connected(self):
        try:
            if self.__conn:
                col_list = self.__db.list_collection_names()
                if len(col_list) > 0:
                    return True
                else:
                    return False
            else:
                col_list = self.__db.list_collection_names()
                if len(col_list) > 0:
                    return True
                else:
                    return False
        except Exception as e:
            logger.error(str(e))
            return False

    def get_col(self):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            return self.__col
        except Exception as e:
            return False, str(e)

    def insert_one(self, data):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            ret_id = self.__col.insert_one(data).inserted_id
            if ret_id:
                return True, ret_id
        except Exception as e:
            return False, str(e)

    def find_one(self, data):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            ret_dict = self.__col.find_one(data)
            if ret_dict:
                return True, ret_dict
            else:
                raise Exception("get record error")
        except Exception as e:
            return False, str(e)

    def datetime2str(d_time):
        return datetime.datetime.strftime(d_time, self._time_format)

    def str2datetime(string):
        if string == '':
            return datetime.datetime(2019, 1, 1, 1, 1)
        return datetime.datetime.strptime(string, self._time_format)

    def find_latest(self):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            results = list(self.__col.find().sort('time', -1).limit(1))
            if len(results) > 0:
                return True, results
            else:
                raise Exception("get record error")
        except Exception as e:
            return False, str(e)

    def find_n_data(self, num_data, project, exclude=None):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            if project:
                results = [x for x in self.__col.find({'error': False, 'service_name': project}).sort('_id', -1).limit(num_data)]
            else:
                results = [x for x in self.__col.find({'error': False, 'service_name': {'$nin': [exclude, 'test']}, 'time': {'$gte': datetime.datetime.now() - datetime.timedelta(seconds=30)}}).sort('_id', -1).limit(num_data)]
            if len(results) > 0:
                return True, results
            else:
                raise Exception("get record error")
        except Exception as e:
            return False, str(e)

    def count_by_data(self, data):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            num_data = self.__col.find(data).count()
            if num_data > 0:
                return True, num_data
            else:
                raise Exception("cant find data")
        except Exception as e:
            return False, str(e)



