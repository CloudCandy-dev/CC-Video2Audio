 [English🇬🇧](README.md) | [日本語🇯🇵](README.ja.md) | [简体中文🇨🇳](README.CN.md)
# CC-video2audio

FFmpeg을 사용하여 비디오 파일을 오디오 파일로 변환합니다.
 예1: mp4 -> mp3
 예2: mov -> wav

지원 코덱(비디오): mp4, mov, avi, mkv, wmv, flv, webm
지원 코덱(오디오): mp3, wav, aac

---

## 사용법

`INPUT` 폴더(또는 `config.json`에서 지정한 입력 폴더)에 비디오 파일을 넣고 `video2audio.py`를 실행하면, `OUTPUT` 폴더(또는 `config.json`에서 지정한 출력 폴더)에 변환된 오디오 파일이 출력됩니다.

기본 변환 형식은 mp3입니다. 변경하려면 `configs/config.json` 파일 내의 `target_format` 값을 변경하십시오 (예: "wav", "aac").
기본 표시 언어는 영어입니다. 변경하려면 `configs/config.json` 파일 내의 `language` 값을 변경하십시오 (예: "ja", "zh-CN", "ko").

사용 중인 FFmpeg(https://ffmpeg.org/) 버전: 2025-05-01-git-707c04fe06