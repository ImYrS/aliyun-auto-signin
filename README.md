<div align=center>

# Aliyun Auto Signin

![GitHub release](https://img.shields.io/github/v/release/ImYrS/aliyun-auto-signin)
![wakatime](https://wakatime.com/badge/user/92b8bbab-18e1-4e0c-af6d-082cc16c9d8a/project/0547bf5c-f66c-4798-ab89-96ddb017fef7.svg)

</div>

## 说明

项目用于自动实现阿里云盘的每日签到活动.  
**支持 GitHub Action , 无需额外操作或服务器即可实现每日自动签到.**

## [如何使用 Action 无服务器签到](https://github.com/ImYrS/aliyun-auto-signin/blob/main/How-To-Use-Action.md)

## 功能

| 功能        | 是否支持 | 未来计划 |
|-----------|:----:|:----:|
| 签到        |  Y   |  -   |
| 签到推送      |  Y   |  -   |
| 多账户       |  Y   |  -   |
| Action 签到 |  Y   |  -   |

*多账户场景下的签到推送功能尚未经过完整测试, 遇到问题欢迎提出 Issues 进行反馈*

## 使用方法

1. Clone 本项目到本地或下载 Release 版本
2. 环境安装
    1. `Python >= 3.10`
    2. 安装依赖
        ```bash
        pip install configobj requests
        ```
3. 修改配置文件
    1. 复制 `example.config.ini` 为 `config.ini`
    2. 在配置文件中填入你的阿里云盘 `refresh token`, 多账户同时签到使用英文逗号分隔
    3. 按需填写推送配置参数, 支持的推送渠道见下方
    4. 保存配置文件
4. 运行并查看是否成功签到
    ```bash
    python app.py
    ```
5. 使用任意方式每日定时运行 `app.py` 即可
6. 以 nohup 等后台形式运行时, 可在 自动生成的 `.log` 文件中查看运行日志

## 低版本 Python

注意: main 分支仅支持 Python 3.10 及以上版本, 低于 3.10 的版本请移步
[低版本兼容分支](https://github.com/ImYrS/aliyun-auto-signin/tree/older-python-version)

*低版本兼容分支并非实时维护, 可能与主分支存在功能差异*

## 推送渠道

*本地运行和 Github Action 运行支持的推送渠道和配置方案不同*

| 渠道           | 本地  | Action |
|--------------|:---:|:------:|
| DingDingTalk |  Y  |   N    |
| ServerChan   |  Y  |   Y    |
| PushDeer     |  Y  |   N    |
| Telegram     |  Y  |   Y    |
| PushPlus     |  Y  |   Y    |

- 钉钉机器人
    - `app_key`: 机器人的 `appKey`
    - `app_secret`: 机器人的 `appSecret`
    - `user_id`: 接收消息的用户 `id`, 必须是钉钉 `userid`
    - [钉钉机器人开发w文档](https://open.dingtalk.com/document/isvapp/send-messages-based-on-enterprise-robot-callback)

- ServerChan
    - `sendkey`: ServerChan 发送消息的鉴权 `key`
    - [server酱官方文档](https://sct.ftqq.com)

- PushDeer (未测试)
    - `endpoint`: 默认为 `https://api2.pushdeer.com`, 自建 PushDeer Server 时才需要更改
    - [PushDeer on GitHub](https://github.com/easychen/pushdeer)

- Telegram Bot
    - `endpoint`: 默认为 `https://api.telegram.org/bot`, 自建 Bot Server 时才需要更改
    - `bot_token`: 机器人的 `token`, 从 Bot Father 处获取
    - `chat_id`: 发送签到消息的用户 `id`, 或 Channel 的 `@username`
    - `proxy`: 代理地址, 例如 `http://127.0.0.1:1080`, 支持 `HTTP` 和 `SOCKS5` 代理, 不使用代理请留空
    - [Telegram Bot API](https://core.telegram.org/bots/api)

- PushPlus
    - `token`: PushPlus 发送消息的用户令牌 `token`
    - [PushPlus官方文档](https://www.pushplus.plus)
- 欢迎 PR 更多推送渠道

## 其他

- 欢迎在 [Issues](https://github.com/ImYrS/aliyun-auto-signin/issues) 中反馈问题
- 你的 Star 是我维护的动力
- PRs are welcome
