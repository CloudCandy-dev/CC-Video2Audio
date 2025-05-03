[日本語 🇯🇵](README.ja.md) | [English 🇬🇧](README.md) | [한국어 🇰🇷](README.kr.md)
# CC-video2audio

使用 FFmpeg 将视频文件转换为音频文件。
 示例1：mp4 -> mp3
 示例2：mov -> wav

支持的编解码器(视频): mp4, mov, avi, mkv, wmv, flv, webm
支持的编解码器(音频): mp3, wav, aac

---

## 如何使用

将视频文件放入 `INPUT` 文件夹（或在 `config.json` 中指定的输入文件夹），运行 `video2audio.py`，转换后的音频文件将输出到 `OUTPUT` 文件夹（或在 `config.json` 中指定的输出文件夹）。

默认转换格式为 mp3。如果需要更改，请修改 `configs/config.json` 文件中 `target_format` 的值（ex:"wav", "aac"）。
默认界面语言为英语。如果需要更改，请修改 `configs/config.json` 文件中 `language` 的值（ex:"ja", "cn", "kr"）。

使用的 FFmpeg(https://ffmpeg.org/) 版本：2025-05-01-git-707c04fe06