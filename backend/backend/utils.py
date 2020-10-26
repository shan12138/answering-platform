"""utils"""
import json
import requests
from django.core import serializers


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'code': "0000"
    }


class JsonUtil:
    """the class of json_util"""
    @staticmethod
    def json_util(parameter):
        """the function of returning data"""
        return_data = []
        if parameter.count() != 0:
            data_json = json.loads(serializers.serialize("json", parameter))
            for data in data_json:
                primary_key = data["pk"]
                fields = data["fields"]
                fields["pk"] = primary_key
                return_data.append(fields)
        return return_data


class YunPian(object):
    """the class of the message identify code"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_msg(self, code, mobile):
        """the function of sending message"""
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【计算机答疑系统】您的验证码是{code}，如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict
