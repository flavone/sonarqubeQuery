from dingtalkchatbot.chatbot import DingtalkChatbot

from config import DINGDING_ACCESS_TOKEN


def send_message(access_token, data):
    if access_token is None:
        access_token = DINGDING_ACCESS_TOKEN
    __web_hook__ = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token
    robot = DingtalkChatbot(__web_hook__)
    text = ''
    if isinstance(data, list):
        for info in data:
            text += info
    elif isinstance(data, str):
        text = data
    else:
        text = '结果即不是list也不是str，无法进行转换'
    robot.send_text(text, is_at_all=True)
