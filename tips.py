#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base.func_news import News
import json

love_function_list = ["喝水提醒"]

manage_function_list = ["启用大橘", "禁用大橘"]

function_list = ["今日新闻", ]

menu = '''
======功能菜单======
🍀签        到🔥抽        签🔯
🎁抽        奖🔥打        劫💰
🔱开  宝  箱🔥排  行  榜👑
🎁礼        物🔥小  黑  屋❌
➿改名提醒
💻指        令🔥群  空  间💡
📳实时疫情🔥查有效期🕓
'''


# def command(msg, robot):
#     text = msg.content
#
#     user = None
#     if msg.sender:
#         user = msg.sender
#     if msg.roomid:
#         user = msg.roomid
#
#
#     if text in manage_function_list:
#         with open("enable.json", "w+") as f:
#             file_data = f.readlines()
#             data_dict = {}
#             if file_data:
#                 data_dict = json.loads(file_data)
#             if text == "启用大橘":
#                 data_dict.update({"user": 1})
#             elif text == "禁用大橘":
#                 data_dict.update({"user": 0})
#             f.write(json.dumps(data_dict))
#
#
#     if text in function_list:
#         # print("tips: " + text)
#         if text == "今日新闻":
#             # print("tips： 今日新闻")
#             # robot.newsReport()
#             news = News().get_important_news()
#
#             robot.sendTextMsg(news, user)
#             return True
#     return False


# text = "今日新闻"
# tips(text, None)
