#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base.func_news import News
import json

love_function_list = ["喝水提醒"]

common_function_list = ["启用大橘", "禁用大橘", "大橘状态"]
base_function_list = ["启用大橘", "禁用大橘", "大橘状态"]
admin_function_list = ["启用大橘", "禁用大橘", "大橘状态", "小黑屋"]


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


def common_activity(msg, activity_dict):
    room_data_dict = activity_dict.get(msg.roomid)
    if not room_data_dict:
        room_data_dict = {}
    day_cnt = room_data_dict.get(msg.sender)
    if not day_cnt:
        day_cnt = 1
    else:
        day_cnt += 1
    room_data_dict.update({msg.sender: day_cnt})
    activity_dict.update(room_data_dict)


