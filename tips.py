#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base.func_news import News
import json

love_function_list = ["喝水提醒"]


base_manage_function_list = ["启用大橘", "禁用大橘", "大橘状态"]
admin_manage_function_list = ["启用大橘", "禁用大橘", "大橘状态", "小黑屋"]


base_function_list = ["今日新闻", "天气"]
rome_function_list = ["今日新闻", "天气", "签到", "抽签", "抽奖", "打劫", "开宝箱", "排行榜", "礼物", "日活跃度", "月活跃度"]


person_menu = """启用大橘 | 禁用大橘 | 大橘状态"""

room_menu = '''
======功能菜单======
🍀签        到🔥抽        签🔯
🎁抽        奖🔥打        劫💰
🔱开  宝  箱🔥排  行  榜👑
🎁礼        物🔥小  黑  屋❌
➿改名提醒
💻指        令🔥群  空  间💡
📳实时疫情🔥查有效期🕓
'''


def command_common(msg):
    text = msg.content
    user = None
    if msg.sender:
        user = msg.sender
    if msg.roomid:
        user = msg.roomid

    return text, user

# a  = {"a": 1}
#
# with open("enable.json", "r+") as f:
# # with open("enable.json", "w") as f:
#     file_data = f.readline()
#     print(file_data)
#     data_dict = {}
#     if file_data:
#         print("---")
#         data_dict = json.loads(file_data)
#         data_dict.update({"aaa": 2})
#         a.update(data_dict)
#
#     f.seek(0)
#     f.truncate()
#     f.write(json.dumps(a))
