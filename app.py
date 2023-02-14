"""
    @Author: ImYrS Yang
    @Date: 2023/2/10
    @Copyright: ImYrS Yang
    @Description:
"""

import logging
from os import environ
from time import mktime, time
from datetime import datetime
from typing import NoReturn, Optional

from configobj import ConfigObj
import requests

from modules import dingtalk, serverchan, pushdeer, telegram, pushplus


def update_access_token(refresh_token: str) -> bool | dict:
    """
    使用 refresh_token 更新 access_token

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
            logging.error(f'更新 access_token 失败, 错误信息: {data}')
            return False
    except KeyError:
        pass

    expire_time = datetime.strptime(data['expire_time'], '%Y-%m-%dT%H:%M:%SZ')

    return {
        'access_token': data['access_token'],
        'refresh_token': data['refresh_token'],
        'expired_at': int((mktime(expire_time.timetuple())) + 8 * 60 * 60) * 1000,
    }


def sign_in(access_token: str) -> bool:
    """
    签到函数

    :param access_token: access_token
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
        logging.error(f'签到失败, 错误信息: {data}')
        push(data)
        return False

    current_day = None
    for i, day in enumerate(data['result']['signInLogs']):
        if day['status'] == 'miss':
            current_day = data['result']['signInLogs'][i - 1]
            break

    reward = (
        '无奖励'
        if not current_day['reward']
        else f'获得{current_day["notice"]}'
    )
    logging.info(f'签到成功, 本月累计签到 {data["result"]["signInCount"]} 天.')
    logging.info(f'本次签到 {reward}')

    push(reward, data['result']['signInCount'])

    return True


def push(
        signin_result: Optional[str] = None,
        signin_count: Optional[int] = None,
) -> NoReturn:
    """
    推送签到结果

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
            pusher.push(signin_result, signin_count, config)


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


def get_access_token() -> str | None:
    """
    从本地文件获取 access_token

    :return: access_token
    """
    try:
        with open('access_token', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def update_access_token_file(access_token: str) -> bool:
    """
    更新本地 access_token 文件

    :param access_token: access_token
    :return: 是否更新成功
    """
    try:
        with open('access_token', 'w') as f:
            f.write(access_token)
        return True
    except Exception as e:
        logging.error(f'更新 access_token 文件失败, 错误信息: {e}')
        return False


def main():
    """
    主函数

    :return:
    """
    environ['NO_PROXY'] = '*'  # 禁止代理

    init_logger()  # 初始化日志系统

    config = ConfigObj('config.ini', encoding='UTF8')  # 获取配置文件

    # 检查 access token 有效性
    if (
            int(config['expired_at']) < int(time() * 1000)
            or not get_access_token()
    ):
        logging.info('access_token 已过期, 正在更新...')
        data = update_access_token(config['refresh_token'])
        if not data:
            logging.error('更新 access_token 失败.')
            return

        update_access_token_file(data['access_token'])
        config['refresh_token'] = data['refresh_token']
        config['expired_at'] = data['expired_at']
        config.write()

    # 签到
    if not sign_in(get_access_token()):
        logging.error('签到失败.')
        return


if __name__ == '__main__':
    main()
