#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tips import *
from base.func_news import News


class RoomFunc(object):

    def __init__(self) -> None:
        self.LOG = logging.getLogger("Robot")
        self.room_members = {}




    @staticmethod
    def welcome(msg, robot):
        content = msg.content
        if "邀请" in content and "加入了群聊" in content:
            robot.sendTextMsg("欢迎加入本群 [庆祝][庆祝][庆祝]", msg.roomid)

    def record_count_msg(self, msg, robot):
        # self.LOG.info(f"msg其他：roomid: {msg.roomid}, sender: {msg.sender}")
        RoomFunc.common_activity(msg, robot.day_activity)
        RoomFunc.common_activity(msg, robot.month_activity)
        RoomFunc.common_activity(msg, robot.all_activity)
        self.LOG.info(f"记录活跃度 日活: {robot.day_activity}")
        self.LOG.info(f"记录活跃度 月活: {robot.month_activity}")

    @staticmethod
    def handler_command(msg, robot):
        content = msg.content
        if "签到" == content:
            pass
        if "抽签" == content:
            pass
        if "抽奖" == content:
            pass
        if "打劫" == content:
            pass
        if "开宝箱" == content:
            pass
        if "排行榜" == content:
            robot.sendTextMsg(activity_rank, msg.roomid)
        if "礼物" == content:
            pass
        if "活跃日排行" == content:
            rst = "====活跃日排行====\n"
            RoomFunc.common_rank_str(robot.day_activity, msg, rst, robot)
        if "活跃月排行" == content:
            rst = "====活跃月排行====\n"
            RoomFunc.common_rank_str(robot.month_activity, msg, rst, robot)
        if "活跃总排行" == content:
            rst = "====活跃总排行====\n"
            RoomFunc.common_rank_str(robot.all_activity, msg, rst, robot)
        if "今日新闻" == content:
            news = News().get_important_news()
            robot.sendTextMsg(news, msg.roomid)

    @staticmethod
    def common_rank_str(activity_dict, msg, text, robot):
        chatroom_members = robot.wcf.get_chatroom_members(msg.roomid)

        room_dict = activity_dict.get(msg.roomid)
        data_list = sorted(room_dict.items(), key=lambda x: x[1], reverse=True)
        for item in data_list[0:9]:
            user_id = item[0]
            text += f"🎈[{item[1]}]{chatroom_members.get(user_id)}\n"
        text += "==============="
        robot.sendTextMsg(text, msg.roomid)

    @staticmethod
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
        activity_dict.update({msg.roomid: room_data_dict})
