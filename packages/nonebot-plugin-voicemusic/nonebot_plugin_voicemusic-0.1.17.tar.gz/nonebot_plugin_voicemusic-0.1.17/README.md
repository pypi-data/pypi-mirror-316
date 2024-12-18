<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-voicemusic

_✨ NoneBot 语音发送点歌插件 ✨_

## 📖 介绍

从 QChatGPT 移植的 Nonebot 语音收听点歌插件

## 致谢：

[QChatGPT_Plugin_Music](https://github.com/zzseki/QChatGPT_Plugin_Music)

[QChatGPT_Plugin_QQMusic](https://github.com/wcwq98/ChatGPT_Plugin_QQMusic)

[星之阁API](https://api.xingzhige.com)

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-voicemusic

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-voicemusic
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-voicemusic
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-voicemusic
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-voicemusic
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_voicemusic"]

</details>

## ⚙️ 配置

需要下载安装ffmpeg

Linux可执行如下命令来安装ffmpeg
```
sudo apt install ffmpeg
```

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 说明 |
|:-----:|:----:|:----:|
| uin | 是 | 提供key的qq号 |
| key | 是 | qqmusic_key |

例：

```
UIN = "YOUR_UIN" # 请将这里的'YOUR_UIN'替换为提供key的qq号
```
```
SKEY = "YOUR_SKEY" # 请将这里的'YOUR_SKEY'替换为获取的qqmusic_key
```

获取qqmusic_key/qm_keyst的方法:[打开QQ音乐官网](https://y.qq.com/),登录后按f12并切换到应用（application）后在cookies中寻找参数填入就好
只能获取QQ音乐上有的音乐

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 点歌 <歌名> <歌手> | 群员 | 否 | 群聊 | 歌手为可选项 |
### 效果图

![919e9a51d7af4dc558b2b4968f3a13c3](https://github.com/user-attachments/assets/ec29fffe-7aee-44c6-a66b-c4f68e1bba40)
