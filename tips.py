#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

love_function_list = ["喝水提醒"]


base_manage_function_list = ["启用大橘", "禁用大橘", "大橘状态", "^更新$"]
admin_manage_function_list = ["启用大橘", "禁用大橘", "大橘状态", "小黑屋"]


base_function_list = ["今日新闻", "天气"]
rome_function_list = ["今日新闻", "天气", "签到", "抽签", "抽奖", "打劫", "开宝箱", "排行榜", "礼物"]


person_menu = """
======功能菜单======
启用大橘 | 禁用大橘 
大橘状态 | 今日新闻 


💡私聊支持功能有限
💡可根据需求定制
===================
"""

room_menu = """
======功能菜单======
🔱排行榜 | 🔥今日新闻
===================
"""
# room_menu = '''
# ======功能菜单======
# 🍀签        到🔥抽        签🔯
# 🎁抽        奖🔥打        劫💰
# 🔱开  宝  箱🔥排  行  榜👑
# 🎁礼        物🔥小  黑  屋❌
# ➿改名提醒
# 💻指        令🔥群  空  间💡
# 📳实时疫情🔥查有效期🕓
# '''

activity_rank = '''
====排行榜指令====
🎈活跃总排行
🎈活跃月排行
🎈活跃日排行
'''















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

# d  = {"a": 1, "b": 4}
#
# a = sorted(d.items(), key=lambda x: x[1], reverse=True)
# print(a)
# rst = "====活跃日排行====\n"
# for item in a[0:9]:
#     rst += f"🎈[{item[1]}]{item[0]}\n"
# rst += "==============="
#
# print(rst)
#
# import re
# txtaa = "踢 @越凌兮"
# aaaaa = re.findall(r'@(.*)', txtaa)
# print(aaaaa)

# content = '你邀请"洛"加入了群聊'
# nick_name = re.findall(r'邀请"(.*)"加入了群聊', content)
# if nick_name:
#     print(nick_name)

