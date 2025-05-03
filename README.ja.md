 [English 🇬🇧](README.md) | [简体中文 🇨🇳](README.cn.md) | [한국어 🇰🇷](README.kr.md)
# CC-video2audio

FFmpeg を使用して動画ファイルを音声ファイルに変換します。
 例1：mp4 -> mp3
 例2：mov -> wav

対応コーデック(動画): mp4, mov, avi, mkv, wmv, flv, webm
対応コーデック(音声): mp3, wav, aac

---

## 使い方

`INPUT` フォルダ (または `config.json` で指定した入力フォルダ) に動画ファイルを入れ、`video2audio.py` を実行すると、`OUTPUT` フォルダ (または `config.json` で指定した出力フォルダ) に変換された音声ファイルが出力されます。

デフォルトの変換形式は mp3 です。変更したい場合は `configs/config.json` 内の `target_format` の値を変更してください (例: "wav", "aac")。
デフォルトの表示言語は英語です。変更したい場合は `configs/config.json` 内の `language` の値を変更してください (例: "ja", "cn", "kr")。

使用している FFmpeg(https://ffmpeg.org/) バージョン: 2025-05-01-git-707c04fe06