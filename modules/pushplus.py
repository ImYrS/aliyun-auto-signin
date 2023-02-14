from typing import Optional
import logging

import requests
from configobj import ConfigObj


class Pusher:
    def __init__(
            self,
            token: str
	):
        self.token = token

    def send(self, title: str, content: str) -> dict:
        """
        发送消息

        :param title: 通知标题
        :param content: 消息内容
        :return:
        """
        return requests.post(
            'http://www.pushplus.plus/send',
            json={
                'token': self.token,
                'title': title,
                'content': content,
            }
        ).json()
def push(
        signin_result: Optional[str],
        signin_count: Optional[int],
        config: Optional[ConfigObj],
) -> bool:
    """
    签到消息推送

    :param signin_result: 签到结果
    :param signin_count: 签到天数
    :param config: 配置文件, ConfigObj 对象
    :return:
    """
    if not config['pushplus_token']:
        logging.error('PushPlus 推送参数配置不完整')
        return False

    try:
        pusher = Pusher(config['pushplus_token'])
        pusher.send(
            '阿里云盘自动签到',
            f'签到成功: 本月累计签到 {signin_count} 天. 本次签到 {signin_result}'
            if signin_result and signin_count
            else f'签到失败: {signin_result}',
        )
        logging.info('PushPlus 推送成功')
    except Exception as e:
        logging.error(f'PushPlus 推送失败, 错误信息: {e}')
        return False

    return True
