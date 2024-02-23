#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tips import *
from business import room_data
from business.base_func import BaseFunc


class PersonFunc(object):

    def __init__(self) -> None:
        self.LOG = logging.getLogger("Robot")

    @staticmethod
    def print_menu(msg, robot):
        text, user = BaseFunc.command_common(msg)
        if text in ["功能", "功能列表", "大橘功能"]:
            robot.sendTextMsg(person_menu, user)
            return True
        return False

    @staticmethod
    def handler_command(msg, robot):
        text, user = BaseFunc.command_common(msg)
        if text in ["功能", "功能列表", "大橘功能"]:
            robot.sendTextMsg(person_menu, user)
            return True
        if text == ["试用", "使用", "使用大橘"]:
            robot.wcf.add_chatroom_members(room_data.test_room_id, msg.sender)

        return False
