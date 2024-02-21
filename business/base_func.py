#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tips import *
from business.room_data import *


class BaseFunc(object):

    def __init__(self) -> None:
        self.LOG = logging.getLogger("Robot")

    def manage_command(self, msg, robot):
        text, user = BaseFunc.command_common(msg)

        self.LOG.info(f"room_id: {msg.roomid}, msg.roomid in room_data_dit: {msg.roomid in room_data_dit}, msg.sender in room_data_dit.get(msg.roomid): {msg.sender in room_data_dit.get(msg.roomid)}")
        self.LOG.info(f"判断结果: {(msg.roomid and msg.roomid in room_data_dit and msg.sender in room_data_dit.get(msg.roomid))}")

        if not msg.roomid and (msg.roomid and msg.roomid in room_data_dit and msg.sender in room_data_dit.get(msg.roomid)):  # 有操作权限才能使用管理指令
            if text in base_manage_function_list:
                self.LOG.info(f"【管理指令】{text}")

                if text == "大橘状态":
                    rst = robot.enable_robot_dict.get(user)
                    if rst == 1:
                        robot.sendTextMsg("大橘正在提供服务～🐱", user)
                    elif rst == 0:
                        robot.sendTextMsg("大橘正在沉默中 🐱🐱🐱", user)
                    if rst is None:
                        # 如果还没初始化使能情况
                        if "@chatroom" in user:
                            robot.sendTextMsg("大橘正在沉默中 🐱🐱🐱", user)  # 群默认不开启
                        else:
                            robot.sendTextMsg("大橘正在提供服务～🐱", user)
                else:
                    with open("enable.json", "w") as f:
                        data_dict = {}
                        if text == "启用大橘":
                            data_dict.update({user: 1})
                            robot.sendTextMsg("大橘开始提供服务 🐱", user)
                        elif text == "禁用大橘":
                            data_dict.update({user: 0})
                            robot.sendTextMsg("大橘已经开始沉默 🐱🐱🐱", user)

                        robot.enable_robot_dict.update(data_dict)
                        f.write(json.dumps(robot.enable_robot_dict))
                self.LOG.info(f"【当前缓存的机器人启用情况】{str(robot.enable_robot_dict)}")
                return True
        return False

    def enable_robot(self, msg, robot):
        text, user = BaseFunc.command_common(msg)

        rst = robot.enable_robot_dict.get(user)
        self.LOG.info(f"【是否启用了大橘】当前用户/群{user} 状态：{rst}. (1-启用 0-禁用)")
        if rst == 1:
            # 如果被启用，返回True
            return True

        if rst is None:
            # 初始化时群默认不开启大橘，个人默认开启大橘
            if "@chatroom" in user:
                return False
            else:
                return True
        return False

    @staticmethod
    def command_common(msg):
        text = msg.content
        user = None
        if msg.sender:
            user = msg.sender
        if msg.roomid:
            user = msg.roomid

        return text, user

