#!/usr/bin/env python3
# -*- coding: utf-8 -*-

love_function_list = ["喝水提醒"]

function_list = ["今日新闻", ]


def tips(text: str, robot):
    if text in function_list:
        if text == "今日新闻":
            robot.newsReport()

