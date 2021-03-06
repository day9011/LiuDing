#coding=utf-8

import json
import uuid
import os
from utils.Config import get_config
from utils.Log import get_log
from utils.Tools import *
from flask import request, session, redirect, render_template, url_for, make_response
from api import server
import random

import time
from multiprocessing import Process
import requests
import urllib
from lib.MongoDB import MongoDB
import base64
import numpy as np
from lib.MysqlDB import *
from auth.user import User

logger = get_log()
config = get_config()
mongo = MongoDB()
debug = config['server']['debug']

mysqldb = MysqlDB()
__MAX_AGE = int(config['auth']['max_age'])
user_handler = User(logger, __MAX_AGE)

course_dict = {
    0: "数学",
    1: "语文",
    2: "英语"
}

time_dict = {
    0: "上午",
    1: "下午",
    2: "晚上"
}

def parse_course(course):
    course_info = {
        'subject' : course_dict[course[1]],
        'fee'     : course[2],
        'term'    : course[3],
        'time'    : time_dict[course[4]],
        'class'   : course[5],
        'classroom': course[6],
        'grade'   : course[8],
        'date'    : course[9].strip().split(','),
        'teacher' : course[11].strip()
    }
    return course_info

def sort_courses(courses):
    courses = sorted(courses, key=lambda x: x['grade'])
    courses = sorted(courses, key=lambda x: x['term'])
    return courses


@server.route('/course', methods=['GET'])
def CourseIndex():
    if request.method == 'GET':
        status = 1
        try:
            account = request.cookies.get('account')
            status, mes = user_handler.check_user(account)
            info = {'username': account, 
                    'status': status, 
                    'message': mes, 
                    'interface': 'check_user'}
            info_str = json.dumps(info, ensure_ascii=False)
            if status:
                logger.info(info_str)
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseIndex"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                main_js = url_for('static', filename='js/main.js')
                course_js = url_for('static', filename='js/course.js')
                content = render_template('course.html', main=main_js, course=course_js)
                resp = make_response(content)
            else:
                logger.error(info_str)
                content = redirect('/')
                resp = make_response(content)
                resp.delete_cookie('account')
                resp.delete_cookie('token')
                resp.delete_cookie('name')
            return resp
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "CourseIndex", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})

@server.route('/course/signup', methods=['POST'])
def CourseSignup():
    if request.method == 'POST':
        status = 1
        try:
            account = request.cookies.get('account')
            status, mes = user_handler.check_user(account)
            info = {'username': account, 
                    'status': status, 
                    'message': mes, 
                    'interface': 'check_user'}
            info_str = json.dumps(info, ensure_ascii=False)
            if status:
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseSignup"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                _id = request.values.get('id', None)
                subject = request.values.get('subject', None)
                term = request.values.get('term', None)
                time = request.values.get('time', None)
                grade = request.values.get('grade', None)
                insert_dict = {
                    '_id': int(_id),
                    'subject': subject,
                    'term': term,
                    'time': time,
                    'grade': int(grade),
                    'signup_time': datetime.datetime.now()
                }
                col = mongo.get_col('front', 'course_signup')
                col.insert_one(insert_dict)
                content = json.dumps({'status': status, 'mes': 'OK'})
                resp = make_response(content)
            else:
                logger.error(info_str)
                content = redirect(json.dumps({'status': status, 'mes': 'not login'}))
                resp = make_response(content)
                resp.delete_cookie('account')
                resp.delete_cookie('token')
                resp.delete_cookie('name')
            return resp
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "CourseSignup", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})


@server.route('/course/query', methods=['GET'])
def CourseQuery():
    if request.method == 'GET':
        status = 1
        try:
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseQuery"}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            account = request.cookies.get('account')
            status, mes = user_handler.check_user(account)
            info = {'username': account, 
                    'status': status, 
                    'message': mes, 
                    'interface': 'check_user'}
            info_str = json.dumps(info, ensure_ascii=False)
            if debug:
                status = True
            if status:
                sql_command = "SELECT * FROM course, teacher WHERE course.tid=teacher.id"
                courses = mysqldb.query(sql_command)
                courses = [parse_course(x) for x in courses]
                courses = sort_courses(courses)
                content = json.dumps({'status': status, 'courses': courses}, ensure_ascii=False)
                resp = make_response(content)
            else:
                logger.error(info_str)
                content = redirect(json.dumps({'status': status, 'mes': 'not login'}))
                resp = make_response(content)
                resp.delete_cookie('account')
                resp.delete_cookie('token')
                resp.delete_cookie('name')
            return resp
        except Exception as e:
            if status == 1:
                status = -10001
            info = {'interface': "CourseQuery", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})


