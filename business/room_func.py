#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import logging
from tips import *
from base.func_news import News


class RoomFunc(object):

    room_members_dict = {}  # 群的成员ID跟成员昵称
    LOG = logging.getLogger("Robot")

    def __init__(self) -> None:
        pass

    @staticmethod
    def welcome(msg, robot):
        content = msg.content
        if "邀请" in content and "加入了群聊" in content:
            nick_name = re.findall(r'邀请"(.*)"加入了群聊', content)
            if nick_name:
                robot.sendTextMsg(f"欢迎 {nick_name[0]} 加入本群 [庆祝][庆祝][庆祝]", msg.roomid)
            else:
                robot.sendTextMsg(f"欢迎加入本群 [庆祝][庆祝][庆祝]", msg.roomid)

    @staticmethod
    def record_count_msg(msg, robot):
        # self.LOG.info(f"msg其他：roomid: {msg.roomid}, sender: {msg.sender}")
        RoomFunc.common_activity(msg, robot.day_activity)
        RoomFunc.common_activity(msg, robot.month_activity)
        RoomFunc.common_activity(msg, robot.all_activity)
        # self.LOG.info(f"记录活跃度 日活: {robot.day_activity}")
        # self.LOG.info(f"记录活跃度 月活: {robot.month_activity}")

    @staticmethod
    def handler_manage_command(msg, robot):
        content = msg.content
        if "踢" in content and "@" in content:
            RoomFunc.LOG.info(f"【handler_manage_command】msg: {msg}")

            data_dict = RoomFunc.get_room_data_dict(msg, robot)
            tmp_data_dict = {value: key for key, value in data_dict.items()}

            nick_name = re.findall(r'@"(.*)" ', content)
            RoomFunc.LOG.info(f"【踢出】nick_name: {nick_name}")
            if nick_name:
                user_id = tmp_data_dict.get(nick_name[0])
                RoomFunc.LOG.info(f"【踢出】nick_name: {nick_name}, user_id: {user_id}")
                robot.wcf.del_chatroom_members(msg.roomid, user_id)

    @staticmethod
    def handler_command(msg, robot):
        content = msg.content
        if content in ["功能", "功能列表", "大橘功能"]:
            robot.sendTextMsg(room_menu, msg.roomid)
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
    def get_room_data_dict(msg, robot):
        data_dict = RoomFunc.room_members_dict.get(msg.roomid)
        if not data_dict:
            data_dict = robot.wcf.get_chatroom_members(msg.roomid)
            RoomFunc.room_members_dict.update({msg.roomid: data_dict})
        return data_dict

    @staticmethod
    def common_rank_str(activity_dict, msg, text, robot):
        data_dict = RoomFunc.get_room_data_dict(msg, robot)

        room_dict = activity_dict.get(msg.roomid)
        data_list = sorted(room_dict.items(), key=lambda x: x[1], reverse=True)
        for item in data_list[0:9]:
            user_id = item[0]
            user_name = data_dict.get(user_id)
            if user_name:
                text += f"🎈[{item[1]}]{user_name}\n"
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
