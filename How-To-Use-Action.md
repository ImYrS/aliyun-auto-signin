# Action 使用指南

## 特性

- 无服务器支持, 0 成本运行
- 自动跟随主仓库更新代码
- 推送至 Telegram 渠道无需代理

## 注意

此文为小白不友好教程, 请尽量利用搜索引擎解决问题.  
**如有提出 Issues 的必要, 请尽量提供报错截图, 错误情况, 以及尝试过的解决方案.**

提问前必看: [提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)

## 准备工作

1. 创建一个新的公开或隐私仓库, 如 `aliyun-signin-action`
   > 不需要 Fork 本仓库, 采用 `uses` 的方式引用本仓库 Action, 实现自动更新
2. 在仓库中新建文件 `.github/workflows/signin.yml`
   > 用于配置 Github Action 的工作流

## 编写 Action 配置

1. 创建 `.github/workflows/signin.yml` 文件, 写入 Action 配置, 以下是参考配置
    ```yaml
    name: Aliyun Signin
    
    on:
      schedule:
       # 每天国际时间 17:20 运行一次, 中国时间 01:20
        - cron: '20 17 * * *'
      workflow_dispatch:
    jobs:
      signin:
        name: Aliyun Signin
        runs-on: ubuntu-latest
        steps:
          - uses: ImYrS/aliyun-auto-signin@main
            with:
              REFRESH_TOKENS: ${{ secrets.REFRESH_TOKENS }}
              GP_TOKEN: ${{ secrets.GP_TOKEN}}
              PUSH_TYPES: ''
              SERVERCHAN_SEND_KEY: ${{ secrets.SERVERCHAN_SEND_KEY }}
              TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
              TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
              PUSHPLUS_TOKEN: ${{ secrets.PUSHPLUS_TOKEN }}
              SMTP_HOST: ${{ secrets.SMTP_HOST }}
              SMTP_PORT: ${{ secrets.SMTP_PORT }}
              SMTP_TLS: ${{ secrets.SMTP_TLS }}
              SMTP_USER: ${{ secrets.SMTP_USER }}
              SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
              SMTP_SENDER: ${{ secrets.SMTP_SENDER }}
              SMTP_RECEIVER: ${{ secrets.SMTP_RECEIVER }}
    ```
2. 按需填写上方配置中的 PUSH_TYPES 参数, 以启用推送功能. 使用 `telegram` 和 `smtp` 渠道在 Action 中可能获得更好体验.
   > 由于配置复杂或渠道 IP 限制等原因, 部分渠道不支持在 Github Action 中使用,
   详见项目首页的[推送渠道](https://github.com/ImYrS/aliyun-auto-signin/blob/main/README.md#%E6%8E%A8%E9%80%81%E6%B8%A0%E9%81%93)


## 配置 GitHub Secrets

在仓库的 `Settings` -> `Secrets and Variables` -> `Actions` 中点击 `New repository secret` 按照推送需要添加 Secrets.  
添加时 `Name` 为下方全大写的配置 key, `Secret` 为对应的值, 均不需要引号.

- `REFRESH_TOKENS` **[必选]** *阿里云盘 refresh token, 多账户使用英文逗号 (,) 分隔*
- `GP_TOKEN` [建议选择] 在 Action 中运行时更新 refresh token

> **获取 GP_TOKEN 的方法**  
> 
> 点击 github 头像 -> `Settings` (注意与配置 Secrets 不是同一个 Settings) -> `Developer settings` -> `Personal access token` -> `Tokens(classic)` -> `Generate new token`  
> 
> 权限选择 `repo`，不然不能更新 Secrets。记住生成的 token，离开页面后无法查看

- `SERVERCHAN_SEND_KEY` [可选] *Server酱推送渠道的 SendKey*
- `TELEGRAM_BOT_TOKEN` [可选] *Telegram Bot Token*
- `TELEGRAM_CHAT_ID` [可选] *Telegram 接收推送消息的会话 ID*
- `PUSHPLUS_TOKEN` [可选] *PushPlus Token*
- `SMTP_HOST` [可选] *SMTP 服务器地址*
- `SMTP_PORT` [可选] *SMTP 服务器端口*
- `SMTP_TLS` [可选] *SMTP 服务器是否使用 TLS*
- `SMTP_USER` [可选] *SMTP 服务器用户名*
- `SMTP_PASSWORD` [可选] *SMTP 服务器密码*
- `SMTP_SENDER` [可选] *SMTP 发件人邮箱*
- `SMTP_RECEIVER` [可选] *SMTP 收件人邮箱*

> 这些 `Secrets` 将加密存储在 GitHub, 无法被直接读取, 但可以在 Action 中使用

正确添加后应显示在 `Repository secrets` 区域而非 `Environment secrets`.

## 运行 Action

你将有两种方式运行 Action

- 手动运行
    - 在仓库的 `Actions` -> `Aliyun Signin` -> `Run workflow` 中点击 `Run workflow` 按钮运行
- 定时自动运行
    - 上方参考的配置文件中已经配置了定时自动运行, 每天国际时间 17:20 运行一次, 中国时间 01:20, 可根据需要调整

## 查看结果

可以在运行的 Action 运行记录中的 `Run ImYrS/aliyun-auto-signin@main` 末尾查看运行结果

## 注意

当前 Action Workflow 尚未经过完全验证, 已知存在或可能存在以下问题.

- 无法自动更新 refresh token, 可能存在运行数天后鉴权失败的情况, 需要手动更新.
- 不配置推送渠道且代码未报错情况下无法直观检查签到结果, 只能进入 workflow 日志查看.

**如果你有更好或其他解决方案, 欢迎 PR**

## 其他

这是本人的第一次 Action 尝试, 如有不足之处, 请多多指教.  
异常请反馈至本项目的 [Issues](https://github.com/ImYrS/aliyun-auto-signin/issues).
