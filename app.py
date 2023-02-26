"""
    @Author: ImYrS Yang
    @Date: 2023/2/10
    @Copyright: ImYrS Yang
    @Description:
"""

import logging
from os import environ
from sys import argv
from time import mktime
from datetime import datetime
from typing import NoReturn, Optional

from configobj import ConfigObj
import requests

from modules import dingtalk, serverchan, pushdeer, telegram, pushplus


def get_access_token(refresh_token: str) -> bool | dict:
    """
    使用 refresh_token 获取 access_token

    :param refresh_token: refresh_token
    :return: 更新成功返回字典, 失败返回 False
    """
    data = requests.post(
        'https://auth.aliyundrive.com/v2/account/token',
        json={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
    ).json()

    try:
        if data['code'] in [
            'RefreshTokenExpired', 'InvalidParameter.RefreshToken',
        ]:
            logging.error(f'[{refresh_token}] 获取 access token 失败, 错误信息: {data}')
            return False
    except KeyError:
        pass

    expire_time = datetime.strptime(data['expire_time'], '%Y-%m-%dT%H:%M:%SZ')

    return {
        'access_token': data['access_token'],
        'refresh_token': data['refresh_token'],
        'expired_at': int((mktime(expire_time.timetuple())) + 8 * 60 * 60) * 1000,
        'phone': data['user_name'],
    }


def sign_in(access_token: str, phone: str) -> bool:
    """
    签到函数

    :param access_token: access_token
    :param phone: 用户手机号
    :return: 是否签到成功
    """
    data = requests.post(
        'https://member.aliyundrive.com/v1/activity/sign_in_list',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
        json={},
    ).json()

    if 'success' not in data:
        logging.error(f'[{phone}] 签到失败, 错误信息: {data}')
        push(data)
        return False

    current_day = None
    for i, day in enumerate(data['result']['signInLogs']):
        if day['status'] == 'miss':
            current_day = data['result']['signInLogs'][i - 1]
            break

    reward = (
        '无奖励'
        if not current_day['isReward']
        else f'获得 {current_day["reward"]["name"]} {current_day["reward"]["description"]}'
    )
    logging.info(f'[{phone}] 签到成功, 本月累计签到 {data["result"]["signInCount"]} 天.')
    logging.info(f'[{phone}] 本次签到 {reward}')

    push(phone, reward, data['result']['signInCount'])

    return True


def push(
        phone: str,
        signin_result: Optional[str] = None,
        signin_count: Optional[int] = None,
) -> NoReturn:
    """
    推送签到结果

    :param phone: 用户手机号
    :param signin_result: 签到结果
    :param signin_count: 当月累计签到天数
    :return:
    """
    config = ConfigObj('config.ini', encoding='UTF8')

    configured_push_types = [
        i.strip()
        for i in (
            [config['push_types']]
            if type(config['push_types']) == str
            else config['push_types']
        )
    ]

    for push_type, pusher in {
        'dingtalk': dingtalk,
        'serverchan': serverchan,
        'pushdeer': pushdeer,
        'telegram': telegram,
        'pushplus': pushplus,
    }.items():
        if push_type in configured_push_types:
            pusher.push(phone, signin_result, signin_count, config)


def init_logger() -> NoReturn:
    """
    初始化日志系统

    :return:
    """
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log_format = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
    )

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(log_format)
    log.addHandler(ch)

    # Log file
    log_name = 'aliyun_auto_signin.log'
    fh = logging.FileHandler(log_name, mode='a', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_format)
    log.addHandler(fh)


def get_config_from_env() -> Optional[dict]:
    """
    从环境变量获取配置

    :return: 配置字典, 配置缺失返回 None
    """
    try:
        return {
            'refresh_token': (
                [environ['REFRESH_TOKEN']]
                if not environ['REFRESH_TOKEN']
                else environ['REFRESH_TOKEN'].split(',')
            ),
            'push_types': (
                [environ['PUSH_TYPES']]
                if not environ['PUSH_TYPES']
                else environ['PUSH_TYPES'].split(',')
            ),
            'serverchan_send_key': environ['SERVERCHAN_SEND_KEY'],
            'telegram_endpoint': 'https://api.telegram.org',
            'telegram_bot_token': environ['TELEGRAM_BOT_TOKEN'],
            'telegram_chat_id': environ['TELEGRAM_CHAT_ID'],
            'pushplus_token': environ['PUSHPLUS_TOKEN'],
        }
    except KeyError as e:
        logging.error(f'环境变量 {e} 缺失.')
        return None


def main():
    """
    主函数

    :return:
    """
    environ['NO_PROXY'] = '*'  # 禁止代理

    init_logger()  # 初始化日志系统

    by_action = (
        True
        if len(argv) == 2 and argv[1] == 'action'
        else False
    )

    # 获取配置
    config = (
        get_config_from_env()
        if by_action
        else ConfigObj('config.ini', encoding='UTF8')
    )

    if not config:
        logging.error('获取配置失败.')
        return

    # 获取所有 refresh token 指向用户
    users = (
        [config['refresh_token']]
        if type(config['refresh_token']) == str
        else config['refresh_token']
    )

    new_users = []

    for user in users:
        # Access Token
        data = get_access_token(user)
        if not data:
            logging.error(f'[{user}] 获取 access token 失败.')
            new_users.append(user)
            continue

        new_users.append(data['refresh_token'])

        # 签到
        if not sign_in(data['access_token'], data['phone']):
            logging.error(f'[{data["phone"]}] 签到失败.')
            continue

    if not by_action:
        # 更新 refresh token
        config['refresh_token'] = new_users


if __name__ == '__main__':
    main()
