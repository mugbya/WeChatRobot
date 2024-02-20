#!/usr/bin/env python3
# -*- coding: utf-8 -*-

love_function_list = ["喝水提醒"]

function_list = ["今日新闻", ]


def tips(text: str, robot):
    print("tips")
    if text in function_list:
        if text == "今日新闻":
            print("tips： 今日新闻")
            robot.newsReport()
            return True
    return False

