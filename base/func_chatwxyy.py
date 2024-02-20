#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import requests
from random import randint


class ChatWXYY:

    def __init__(self, wxconf=None) -> None:
        self.LOG = logging.getLogger(__file__)

        key = wxconf['key']
        secret = wxconf['secret']
        self.token = None
        self.token_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(
            key, secret)
        if key and secret:
            self.token = self.get_token()

        self.fallback = ["再见", "不要调戏我", "赶紧滚"]

    def __repr__(self):
        return '文心一言'

    @staticmethod
    def value_check(conf: dict) -> bool:
        if conf:
            return all(conf.values())
        return False

    @staticmethod
    def value_check(conf: dict) -> bool:
        if conf:
            return all(conf.values())
        return False

    def get_answer(self, msg: str, sender: str = None) -> str:
        # print("msg: " + msg)
        rsp = ""
        try:
            rsp = self.ai_qs(msg, sender)
        except Exception as e:
            self.LOG.error(f"{e}: {rsp}")
            idx = randint(0, len(self.fallback) - 1)
            rsp = self.fallback[idx]

        return rsp


    def get_token(self):
        # https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Ilkkrb0i5

        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", self.token_url, headers=headers, data=payload)

        dict_rsp = eval(response.text)
        access_token = dict_rsp.get("access_token")
        expires_in = dict_rsp.get("expires_in")
        error_description = dict_rsp.get("error_description")
        if not access_token:
            self.LOG.error("文心一言 获取token失败:" + error_description)
        return access_token

    def ai_qs(self, message, user):
        if not self.token:
            return "token未存在"

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + self.token

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, stream=False)
        # print("response--")
        # print(response.text)
        dict_rsp = json.loads(response.text)
        result = dict_rsp.get("result")
        return result
