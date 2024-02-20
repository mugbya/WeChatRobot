#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base.func_news import News

love_function_list = ["喝水提醒"]

function_list = ["今日新闻", ]


def tips(msg, robot):
    print("tips")
    text = msg.content
    # print("tips: " + (text in function_list))
    if text in function_list:
        print("tips: " + text)
        if text == "今日新闻":
            print("tips： 今日新闻")
            # robot.newsReport()
            news = News().get_important_news()
            robot.sendTextMsg(news, msg.sender)
            return True
    return False


# text = "今日新闻"
# tips(text, None)
