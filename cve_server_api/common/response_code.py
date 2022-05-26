#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/5/19 9:46
# @Author : zhu_it2019@126.com
# @File : response_code.py
# @Software: PyCharm
# Description: 自定义状态码 统一返回json数据

from rest_framework.response import Response

from django.conf import settings


def result(code=settings.REQ_SUCCESS, message="", data=None, count=0, kwargs=None):
    """
    定义统一的 json 字符串返回格式
    :param code:
    :param message:
    :param data:
    :param count:
    :param kwargs:
    :return:
    """
    json_dict = {"code": code, "message": message, "count": count, "data": data}
    # isinstance(object对象, 类型):判断是否数据xx类型
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return Response(json_dict)


def rsp_data(data=None, message="OK", count=0):
    """
    请求响应数据
    :param message:
    :param data:
    :param count:
    :return:
    """
    return result(data=data, message=message, count=count)


def params_error(message=""):
    """
    参数错误
    :param message:
    :return:
    """
    return result(code=settings.PARMMS_ERROR, message=message, data=[])


def un_auth_error(message="", data=None):
    """
    未授权错误
    :param message:
    :param data:
    :return:
    """
    return result(code=settings.PERMISSIONS_ERROR, message=message, data=data)


def method_error(message="", data=None):
    """
    请求方法错误
    :param message:
    :param data:
    :return:
    """
    return result(code=settings.METHOD_ERROR, message=message, data=data)


def server_error(message="", data=None):
    """
    服务器内部错误
    :param message:
    :param data:
    :return:
    """
    return result(code=settings.SERVER_ERROR, message=message, data=data)
