from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.core.cache import cache


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # 获取本来应该返回的exception的response

    if response is not None:
        response.data['status_code'] = response.status_code  # 可添加status_code
        # response.data['error_code'] = 1
        try:
            response.data["message"] = response.data['detail']  # 增加message这个key
            del response.data['detail']
        except:
            pass
    if response is None:
        return HttpResponse("禁止单独测试接口")

    return response


class myException422(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


def jwt_response_username_userid_token(token, user=None, request=None):
    """
    自定义验证成功后的返回数据处理函数
    :param token:
    :param user:
    :param request:
    :return:
    """

    data = {
        # jwt令牌
        'status_code': 200,
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'role':user.role,
    }
    return data





