[日本語 🇯🇵](README.ja.md) | [简体中文 🇨🇳](README.cn.md) | [한국어 🇰🇷](README.kr.md)
# CC-video2audio

Convert video files to audio files using FFmpeg.
 ex1：mp4 -> mp3
 ex2：mov -> wav

Support codecs(video): mp4, mov, avi, mkv, wmv, flv, webm
Support codecs(audio): mp3, wav, aac

---

## How to use

Put the video file in the `INPUT` folder (or the input folder specified in `config.json`), run `video2audio.py`, and the converted audio file will be output to the `OUTPUT` folder (or the output folder specified in `config.json`).

The default conversion format is mp3. If you want to change it, change the value of `target_format` in `configs/config.json` (e.g., "wav", "aac").
The default display language is English. If you want to change it, change the value of `language` in `configs/config.json` (e.g., "ja", "zh-CN", "ko").

Using FFmpeg(https://ffmpeg.org/) Version: 2025-05-01-git-707c04fe06