#coding=utf-8


import json
import uuid
import os
from utils.Config import get_config
from utils.Log import get_log
from api import server
from hashlib import md5
import datetime
import time
from urllib import parse
import json
import requests
from flask import request, session, redirect, render_template, url_for, make_response
from lib.MysqlDB import *
from utils.MakeToken import gen_token
from auth.user import User


logger = get_log()
config = get_config()
mysqldb = MysqlDB()
__MAX_AGE = int(config['auth']['max_age'])
user_handler = User(logger, __MAX_AGE)

@server.route('/login', methods=['GET', 'POST'])
def Login():
    status = 1
    try:
        if request.method == 'GET':
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "Login", 'method': 'GET'}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            account = request.cookies.get('account')
            status, mes = user_handler.check_user(account)
            info = {'username': account, 
                    'status': status, 
                    'message': mes, 
                    'interface': 'check_user'}
            info_str = json.dumps(info, ensure_ascii=False)
            if status:
                logger.info(info_str)
                content = redirect('/')
                resp = make_response(content)
                resp.set_cookie('account', account, max_age=__MAX_AGE)
                resp.set_cookie('token', token, max_age=__MAX_AGE)
                resp.set_cookie('name', name, max_age=__MAX_AGE)
                return resp
            else:
                logger.error(info_str)
            main_js = url_for('static', filename='js/main.js')
            auth_js = url_for('static', filename='js/auth.js')
            return render_template('login.html', main=main_js, auth=auth_js)
        elif request.method == 'POST':
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "Login", 'method': 'POST'}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            account = request.values.get('account', None)
            password = request.values.get('password', None)
            params = {
                'account': account,
                'password': password
            }
            info = {'interface': "Login", 'params': params}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)

            # get the password
            sql_command = 'SELECT password FROM account WHERE account.account="{}"'.format(account)
            results = mysqldb.query(sql_command)
            if results:
                sql_password = results[0][0]
            else:
                status = -11
                raise Exception("Authentication failed!")
            if sql_password != password:
                status = -11
                raise Exception("Authentication failed!")

            # get the name
            sql_command = "SELECT student.name, account.role FROM account,student WHERE account.account='{}' and student.id=account.id".format(account)
            results = mysqldb.query(sql_command)
            name = results[0][0]
            role = results[0][1]
            token = gen_token()
            user_info = {
                'time': datetime.datetime.now(),
                'token': token,
                'role': role
            }
            user_handler.insert_user_info(account, user_info)
            resp = make_response(json.dumps({'status': status, 'mes': 'login successfully'}))
            resp.set_cookie('account', account, max_age=__MAX_AGE)
            resp.set_cookie('token', token, max_age=__MAX_AGE)
            resp.set_cookie('name', name, max_age=__MAX_AGE)
            return resp
        else:
            try:
                resp = make_response(redirect('/'))
                resp.delete_cookie('account')
                resp.delete_cookie('token')
                resp.delete_cookie('name')
            except:
                pass
            return resp
    except Exception as e:
        if status == 1:
            status = -10000
        info = {'interface': "Login", 'message': str(e)}
        info_str = json.dumps(info, ensure_ascii=False)
        logger.error(info_str)
        return json.dumps({'status': status, 'mes': str(e)})

