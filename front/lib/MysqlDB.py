#coding=utf-8

from utils.Log import get_log
import pymysql
import os
import datetime
import json


logger = get_log()

class MysqlDB(object):
    def __init__(self):
        self.__host = os.environ['MYSQL_HOST'].strip()
        self.__port = os.environ['MYSQL_PORT'].strip()
        self.__username = os.environ['MYSQL_USER'].strip()
        self.__password = os.environ['MYSQL_PASS'].strip()
        self.__database = os.environ['MYSQL_DB'].strip()
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
            self.db = pymysql.connect(host=self.__host, 
                                port=int(self.__port),
                                user=self.__username,
                                passwd=self.__password,
                                db=self.__database, charset="utf8") 
            self.cursor = self.db.cursor()
            num = self.cursor.execute("show tables")
            if num > 0:
                logger.info("connect sucessfully")
            else:
                raise Exception("connect mysql error")
        except Exception as e:
            info = {'interface': "MysqlConnect", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)            

    def execute(self, sql):
        # double check connect
        # self.check_command(sql)
        try:
            info = {'interface': "MysqlExecute", 'command': sql}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)   
            # 执行sql语句
            ret = self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return ret
        except Exception as e:
            logger.error(str(e))
            self.connect()
            try:
                ret = self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
                return ret
            except Exception as e:
                logger.error(str(e))
                return -1

    def verify_student_account(self, account):
        try:
            sql_command = "SELECT account.id,student.id,account.account FROM student,account WHERE \
                student.id = account.id and account.account ='{}'".format(account)
            return self.execute(sql_command)
        except Exception as e:
            logger.error(str(e))
            return -2000
    
    def query_course(self, grade):
        try:
            sql_command = "SELECT account.id,student.id,account.account FROM student,account WHERE \
                student.id = account.id and account.account ='{}'".format(grade)
            return self.execute(sql_command)
        except Exception as e:
            logger.error(str(e))
            return -2000

    def query(self, sql):
        try:
            info = {'interface': "MysqlQuery", 'command': sql}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)   
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logger.error(str(e))
            self.connect()
            try:
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                return results
            except Exception as e:
                logger.error(str(e))
                return -1