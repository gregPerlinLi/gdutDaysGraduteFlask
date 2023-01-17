# -*- coding: utf-8 -*-
# @Time      :2023/1/14 14:23
# @Author    :Ymir
# 本地测试文件

import flask
import re
from flask_cors import CORS
import json
from GdutUtil import GudtUtil
from flask import request, jsonify
from gevent import pywsgi

import time

app = flask.Flask(__name__)

# 防止自动转unicode
app.config['JSON_AS_ASCII'] = False
# 注册CORS, "/*" 允许访问所有api
CORS(app, resources=r'/*')


def test_json():
    json_path = "../test/test.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f, strict=False)
        return data


# 本地测试
@app.route('/api/test', methods=["POST", "GET"])
def get_kc():
    # 获取课程
    # t = time.time()
    # user = GudtUtil(acount="2112205176", password="Gdut21122")
    # ret = user.get_ck()
    #
    # end = time.time()
    # print("耗时：" + str(end - t))
    ret = {
        "code": 200,
        "Hi": "Ymri!"
    }
    return flask.jsonify(ret)


@app.route('/api/gdutLogin', methods=["POST", "GET"])
def login():
    t = time.time()
    ret = {
        "code": 4000,
        # 为了兼容前端，本科显示的是校区，研究生就显示学院吧
        "data": None,
        "userInfo": None,
        "cookies": None,
        # 学期
        "semester": None,
        "msg": "登录失败",
        "isLive": False
    }
    try:
        data = request.get_json()
        account = data["account"]
        password = data["password"]
        # print(account, password)
        user = GudtUtil(acount=account, password=password)
        ret = user.login()
    except Exception as e:
        pass
    end = time.time()
    print("耗时：" + str(end - t))
    return flask.jsonify(ret)


@app.route('/api/getCk', methods=["POST", "GET"])
def get_ck():
    t = time.time()
    # 假定前端传入的是json类型
    data = request.get_json()
    # print(data)
    cookies = data["cookies"]
    wid = data["semester"]
    ret = GudtUtil.get_ck_static(cookies=cookies, wid=wid)
    end = time.time()
    # print("耗时：" + str(end - t))
    # 如果获取的是空，则重新登录返回
    return flask.jsonify(ret)


@app.route('/api/score', methods=["POST", "GET"])
def get_score():
    """
    考试成绩接口
    :return:
    """
    t = time.time()
    # 假定前端传入的是json类型
    data = request.get_json()
    # print(data)
    cookies = data["cookies"]
    ret = GudtUtil.get_exam_data(cookies=cookies)
    end = time.time()
    # print("耗时：" + str(end - t))
    # 如果获取的是空，则重新登录返回
    return flask.jsonify(ret)


@app.route('/api/live', methods=["POST", "GET"])
def check_live():
    """
    检查用户信息是否有效
    :return:
    """
    t = time.time()
    # 假定前端传入的是json类型
    data = request.get_json()
    # print(data)
    cookies = data["cookies"]
    ret = GudtUtil.get_user_info_by_cookies(cookies=cookies)
    end = time.time()
    # print("耗时：" + str(end - t))
    # 如果获取的是空，则重新登录返回
    return flask.jsonify(ret)


server = pywsgi.WSGIServer(('0.0.0.0', 8888), app)
server.serve_forever()

if __name__ == "__main__":
    run_code = 0
