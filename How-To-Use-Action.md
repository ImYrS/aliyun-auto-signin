# Action 使用教程

## 准备工作

1. 创建一个新的仓库, 如 `aliyun-signin-action`
2. 在仓库中新建文件 `.github/workflows/signin.yml`
   > 用于配置 Github Action 的工作流

## 编写 Action 配置

1. 编辑 `.github/workflows/signin.yml` 文件, 写入 Action 配置, 以下是参考配置
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
             PUSH_TYPES:
             SERVERCHAN_SEND_KEY: ${{ secrets.SERVERCHAN_SEND_KEY }}
             TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
             TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
             PUSHPLUS_TOKEN: ${{ secrets.PUSHPLUS_TOKEN }}
   ```
2. 按需修改 PUSH_TYPES 参数, 以启用推送功能
   > 由于配置复杂或渠道 IP 限制等原因, 部分渠道不支持在 Github Action 中使用, 详见项目首页的[推送渠道](https://github.com/ImYrS/aliyun-auto-signin/blob/main/README.md#%E6%8E%A8%E9%80%81%E6%B8%A0%E9%81%93)

## 配置 GitHub Secrets

在仓库的 `Settings` -> `Secrets and Variables` -> `Actions` 中添加以下 Secrets
- `REFRESH_TOKENS` (必需)
     > 阿里云盘 refresh token, 多账户使用英文逗号 (,) 分隔
- `SERVERCHAN_SEND_KEY` (可选)
     > Server酱推送渠道的 SendKey
- `TELEGRAM_BOT_TOKEN` (可选)
     > Telegram Bot Token
- `TELEGRAM_CHAT_ID` (可选)
     > Telegram 接收推送消息的会话 ID
- `PUSHPLUS_TOKEN` (可选)
     > PushPlus Token

> 这些 `Secrets` 将加密存储在 GitHub, 无法被读取, 但是可以在 Action 中使用

## 运行 Action

你将有两种方式运行 Action

- 手动运行
  - 在仓库的 `Actions` -> `Aliyun Signin` -> `Run workflow` 中点击 `Run workflow` 按钮运行
- 定时自动运行
  - 上方参考的配置文件中已经配置了定时自动运行, 每天国际时间 17:20 运行一次, 中国时间 01:20, 可根据需要调整

## 其他

这是本人的第一次 Action 尝试, 如有不足之处, 请多多指教.  
异常请反馈至本项目的 [Issues](https://github.com/ImYrS/aliyun-auto-signin/issues).