#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


class RoomFunc(object):

    def __init__(self) -> None:
        self.LOG = logging.getLogger("Robot")

    @staticmethod
    def welcome(msg, robot):
        conent = msg.content
        if "邀请" in conent and "加入了群聊" in conent:
            robot.sendTextMsg("欢迎加入本群 [庆祝][庆祝][庆祝]", msg.roomid)

    def record_count_msg(self, msg, robot):
        # self.LOG.info(f"msg其他：roomid: {msg.roomid}, sender: {msg.sender}")
        RoomFunc.common_activity(msg, robot.day_activity)
        RoomFunc.common_activity(msg, robot.month_activity)
        self.LOG.info(f"记录活跃度 日活: {robot.day_activity}")
        self.LOG.info(f"记录活跃度 月活: {robot.month_activity}")

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
