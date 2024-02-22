# -*- coding: utf-8 -*-
import traceback
import logging
import re
import time
import xml.etree.ElementTree as ET
from queue import Empty
from threading import Thread

from wcferry import Wcf, WxMsg

from tips import *
from business.room_func import RoomFunc
from business.base_func import BaseFunc
from base.func_bard import BardAssistant
from base.func_chatglm import ChatGLM
from base.func_chatgpt import ChatGPT
from base.func_chengyu import cy
from base.func_news import News
from base.func_tigerbot import TigerBot
from base.func_xinghuo_web import XinghuoWeb
from base.func_chatwxyy import ChatWXYY
from configuration import Config
from constants import ChatType
from job_mgmt import Job

__version__ = "39.0.10.1"


class Robot(Job):
    """个性化自己的机器人
    """

    def __init__(self, config: Config, wcf: Wcf, chat_type: int) -> None:
        self.wcf = wcf
        self.config = config
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.allContacts = self.getAllContacts()

        self.baseFunc = BaseFunc()
        self.roomFunc = RoomFunc()

        self.enable_robot_dict = {}  # 记录个人/群是否启用机器人
        self.day_activity = {}  # 记录群里的日活跃度
        self.month_activity = {}  # 记录群里的月活跃度
        self.all_activity = {}  # 记录群里的总活跃度

        # dbs = self.wcf.get_dbs()
        # self.LOG.info(f"【dbs】{str(dbs)}")
        #
        # tables = self.wcf.get_tables("ChatMsg.db")
        # self.LOG.info(f"【tables】{str(tables)}")

        with open("room/day_activity", "r") as f:
            line = f.readline()
            if line:
                self.day_activity = json.loads(line)
        with open("room/month_activity", "r") as f:
            line = f.readline()
            if line:
                self.month_activity = json.loads(line)
        with open("room/all_activity", "r") as f:
            line = f.readline()
            if line:
                self.all_activity = json.loads(line)
        with open("enable.json", "r") as f:
            line = f.readline()
            if line:
                self.enable_robot_dict = json.loads(line)

        self.LOG.info(f"【初始化缓存的机器人启用情况】{str(self.enable_robot_dict)}")
        self.LOG.info(f"【初始化缓存日活跃度】{str(self.day_activity)}")

        if ChatType.is_in_chat_types(chat_type):
            if chat_type == ChatType.TIGER_BOT.value and TigerBot.value_check(self.config.TIGERBOT):
                self.chat = TigerBot(self.config.TIGERBOT)
            elif chat_type == ChatType.CHATGPT.value and ChatGPT.value_check(self.config.CHATGPT):
                self.chat = ChatGPT(self.config.CHATGPT)
            elif chat_type == ChatType.XINGHUO_WEB.value and XinghuoWeb.value_check(self.config.XINGHUO_WEB):
                self.chat = XinghuoWeb(self.config.XINGHUO_WEB)
            elif chat_type == ChatType.CHATGLM.value and ChatGLM.value_check(self.config.CHATGLM):
                self.chat = ChatGLM(self.config.CHATGLM)
            elif chat_type == ChatType.BardAssistant.value and BardAssistant.value_check(self.config.BardAssistant):
                self.chat = BardAssistant(self.config.BardAssistant)
            elif chat_type == ChatType.CHATWXYY.value and ChatWXYY.value_check(self.config.ChatWXYY):
                self.chat = ChatWXYY(self.config.ChatWXYY)
            else:
                self.LOG.warning("未配置模型")
                self.chat = None
        else:
            if TigerBot.value_check(self.config.TIGERBOT):
                self.chat = TigerBot(self.config.TIGERBOT)
            elif ChatGPT.value_check(self.config.CHATGPT):
                self.chat = ChatGPT(self.config.CHATGPT)
            elif XinghuoWeb.value_check(self.config.XINGHUO_WEB):
                self.chat = XinghuoWeb(self.config.XINGHUO_WEB)
            elif ChatGLM.value_check(self.config.CHATGLM):
                self.chat = ChatGLM(self.config.CHATGLM)
            elif BardAssistant.value_check(self.config.BardAssistant):
                self.chat = BardAssistant(self.config.BardAssistant)
            elif ChatWXYY.value_check(self.config.ChatWXYY):
                self.chat = ChatWXYY(self.config.ChatWXYY)
            else:
                self.LOG.warning("未配置模型")
                self.chat = None

        self.LOG.info(f"已选择: {self.chat}")

    @staticmethod
    def value_check(args: dict) -> bool:
        if args:
            return all(value is not None for key, value in args.items() if key != 'proxy')
        return False

    def toAt(self, msg: WxMsg) -> bool:
        """处理被 @ 消息
        :param msg: 微信消息结构
        :return: 处理状态，`True` 成功，`False` 失败
        """
        if self.baseFunc.enable_robot(msg, self):
            return self.toChitchat(msg)
        return False

    def toChengyu(self, msg: WxMsg) -> bool:
        """
        处理成语查询/接龙消息
        :param msg: 微信消息结构
        :return: 处理状态，`True` 成功，`False` 失败
        """
        status = False
        texts = re.findall(r"^([#|?|？])(.*)$", msg.content)
        # [('#', '天天向上')]
        if texts:
            flag = texts[0][0]
            text = texts[0][1]
            if flag == "#":  # 接龙
                if cy.isChengyu(text):
                    rsp = cy.getNext(text)
                    if rsp:
                        self.sendTextMsg(rsp, msg.roomid)
                        status = True
            elif flag in ["?", "？"]:  # 查词
                if cy.isChengyu(text):
                    rsp = cy.getMeaning(text)
                    if rsp:
                        self.sendTextMsg(rsp, msg.roomid)
                        status = True

        return status

    def toChitchat(self, msg: WxMsg) -> bool:
        """闲聊，接入 ChatGPT
        """
        if not self.chat:  # 没接 ChatGPT，固定回复
            rsp = "你@我干嘛？"
        else:  # 接了 ChatGPT，智能回复
            q = re.sub(r"@.*?[\u2005|\s]", "", msg.content).replace(" ", "")
            rsp = self.chat.get_answer(q, (msg.roomid if msg.from_group() else msg.sender))

        if rsp:
            if msg.from_group():
                self.sendTextMsg(rsp, msg.roomid, msg.sender)
            else:
                self.sendTextMsg(rsp, msg.sender)

            return True
        else:
            self.LOG.error(f"无法从 ChatGPT 获得答案")
            return False

    def processMsg(self, msg: WxMsg) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
        群号：msg.roomid  微信ID：msg.sender  消息内容：msg.content
        content = "xx天气信息为："
        receivers = msg.roomid
        self.sendTextMsg(content, receivers, msg.sender)
        """

        # 群聊消息
        if msg.from_group():

            RoomFunc.record_count_msg(msg, self)  # 记录发言次数，方便统计活跃度
            RoomFunc.welcome(msg, self)
            RoomFunc.handler_command(msg, self)

            # 如果在群里被 @
            if msg.roomid not in self.config.GROUPS:  # 不在配置的响应的群列表里，忽略
                return

            if msg.is_at(self.wxid):  # 被@
                self.toAt(msg)

            # tips(msg, self)

            # else:  # 其他消息
            #     self.toChengyu(msg)

            return  # 处理完群聊信息，后面就不需要处理了

        # 非群聊信息，按消息类型进行处理
        if msg.type == 37:  # 好友请求
            self.autoAcceptFriendRequest(msg)

        elif msg.type == 10000:  # 系统信息
            self.sayHiToNewFriend(msg)

        elif msg.type == 0x01:  # 文本消息
            # 让配置加载更灵活，自己可以更新配置。也可以利用定时任务更新。
            if msg.from_self():
                if msg.content == "^更新$":
                    self.config.reload()
                    self.LOG.info("已更新")
            else:
                if self.baseFunc.enable_robot(msg, self):
                    if not BaseFunc.print_menu(msg, self):
                        self.toChitchat(msg)  # 闲聊

    def onMsg(self, msg: WxMsg) -> int:
        try:
            self.LOG.info(msg)  # 打印信息
            flag = self.baseFunc.manage_command(msg, self)  # 首先执行管理指令
            self.LOG.info(f"【管理指令】是否是管理执行指令 {flag}")
            if not flag:
                self.processMsg(msg)
        except Exception as e:
            self.LOG.error(e)
        return 0

    def enableRecvMsg(self) -> None:
        self.wcf.enable_recv_msg(self.onMsg)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                # self.LOG.error(f"【等待消息】************************")
                try:
                    msg = wcf.get_msg()
                    if msg.roomid and msg.roomid not in self.config.GROUPS:
                        return
                    self.LOG.info(f"msg：roomid: {msg.roomid}, sender: {msg.sender}, content: {msg.content}")

                    flag = self.baseFunc.manage_command(msg, self)  # 首先执行管理指令
                    self.LOG.info(f"【管理指令】是否是管理执行指令 {flag}")
                    if not flag:
                        self.processMsg(msg)
                    # self.processMsg(msg)
                except Empty:
                    # self.LOG.error(f"【空消息】！！！！！！！！！！！！！！ ")
                    continue  # Empty message
                except Exception as e:
                    traceback.print_exc()
                    self.LOG.error(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 发送消息
        :param msg: 消息字符串
        :param receiver: 接收人wxid或者群id
        :param at_list: 要@的wxid, @所有人的wxid为：notify@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            if at_list == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = at_list.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f" @{self.wcf.get_alias_in_chatroom(wxid, receiver)}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三
        if ats == "":
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)

    def getAllContacts(self) -> dict:
        """
        获取联系人（包括好友、公众号、服务号、群成员……）
        格式: {"wxid": "NickName"}
        """
        contacts = self.wcf.query_sql("MicroMsg.db", "SELECT UserName, NickName FROM Contact;")
        return {contact["UserName"]: contact["NickName"] for contact in contacts}

    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            self.runPendingJobs()
            time.sleep(1)

    def autoAcceptFriendRequest(self, msg: WxMsg) -> None:
        try:
            xml = ET.fromstring(msg.content)
            v3 = xml.attrib["encryptusername"]
            v4 = xml.attrib["ticket"]
            fromusername = xml.attrib["fromusername"] # 申请人的wxid
            content = xml.attrib["content"] # 发送的备注
            scene = int(xml.attrib["scene"])
            self.wcf.accept_new_friend(v3, v4, scene)

            if "试用" == content:
                self.wcf.add_chatroom_members("48193485317@chatroom", fromusername)
        except Exception as e:
            self.LOG.error(f"同意好友出错：{e}")

    def sayHiToNewFriend(self, msg: WxMsg) -> None:
        nickName = re.findall(r"你已添加了(.*)，现在可以开始聊天了。", msg.content)
        if nickName:
            # 添加了好友，更新好友列表
            self.allContacts[msg.sender] = nickName[0]
            self.sendTextMsg(f"Hi {nickName[0]}，我自动通过了你的好友请求。", msg.sender)

    def newsReport(self) -> None:
        receivers = self.config.NEWS
        if not receivers:
            return

        news = News().get_important_news()
        for r in receivers:
            self.sendTextMsg(news, r)

    def drink(self) -> None:
        receivers = self.config.DRINK
        if not receivers:
            return

        for r in receivers:
            self.sendTextMsg("我的公主，1小时到了，起来去喝水吧 😘", r)

    def save_cache(self):
        _is_receiving_msg = self.wcf.is_receiving_msg()
        self.LOG.info(f"【是否已启动接收消息功能】{_is_receiving_msg}")

        with open("room/day_activity", "w") as f:
            f.write(json.dumps(self.day_activity))
        with open("room/month_activity", "w") as f:
            f.write(json.dumps(self.month_activity))
        with open("room/all_activity", "w") as f:
            f.write(json.dumps(self.all_activity))

    def init_current_day_data(self):
        self.day_activity = {}
        with open("room/day_activity", "w") as f:
            f.write(json.dumps(self.day_activity))

    def init_current_month_data(self):
        self.month_activity = {}
        with open("room/month_activity", "w") as f:
            f.write(json.dumps(self.month_activity))

