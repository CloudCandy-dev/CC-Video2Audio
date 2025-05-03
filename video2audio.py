import subprocess
import sys
import platform
from pathlib import Path
from lib.loader import lang_load, get_text
from lib.config_lib import cf_load


# --- 初期設定 ---
# 設定と言語データを最初に読み込む
config_data = cf_load()
lang_load(config_data.get("language")) # 設定ファイルに言語指定がなければ英語をデフォルトに

# スクリプトの場所を基準に各種パスを設定
SCRIPT_DIR = Path(__file__).parent.resolve()
# 設定ファイルからディレクトリ名を取得
INPUT_DIR_NAME = config_data.get("input_dir")
OUTPUT_DIR_NAME = config_data.get("output_dir")
INPUT_DIR = SCRIPT_DIR / INPUT_DIR_NAME
OUTPUT_DIR = SCRIPT_DIR / OUTPUT_DIR_NAME

# ターゲットフォーマットを設定ファイルから取得
TARGET_FORMAT = config_data.get("target_format")

# --- 設定ファイルから読み込む値 ---
# 各出力フォーマットに対応するFFmpegオプション
FFMPEG_OPTIONS = config_data.get("ffmpeg_options", {}) # configになければ空の辞書

# 処理対象とする入力ファイルの拡張子 (リストからセットに変換)
SUPPORTED_INPUT_EXTENSIONS_LIST = config_data.get("supported_input_extensions", []) # configになければ空のリスト
SUPPORTED_INPUT_EXTENSIONS = set(SUPPORTED_INPUT_EXTENSIONS_LIST)


# --- FFmpeg実行ファイルの探索 ---
def find_ffmpeg():
    """
    FFmpeg実行ファイル名をOSによって判別し、存在を確認する。
    スクリプトと同じディレクトリ、とサブフォルダを探す。

    Returns:
        str or None: FFmpegコマンド名 (例: 'ffmpeg' or 'ffmpeg.exe' のフルパス)、見つからない場合はNone。
    """
    # OSによってffmpegの実行ファイル名を決定
    ffmpeg_exe_name = 'ffmpeg.exe' if platform.system() == "Windows" else 'ffmpeg'
    # まず ffmpeg/ffmpeg を試す
    local_ffmpeg_path = SCRIPT_DIR / 'ffmpeg' / ffmpeg_exe_name
    if local_ffmpeg_path.is_file():
        return str(local_ffmpeg_path)
    # 次に ffmpeg (スクリプト直下) を試す
    local_ffmpeg_path_alt = SCRIPT_DIR / ffmpeg_exe_name
    if local_ffmpeg_path_alt.is_file():
        return str(local_ffmpeg_path_alt)
    # 環境変数 PATH を探す (Noneを返して convert_media_to_audio 内でエラー捕捉)
    # shutil.which('ffmpeg') でも良いが、今回はローカル優先とする
    return ffmpeg_exe_name # PATHにあることを期待してコマンド名のみ返す


# --- メインの変換関数 ---
def convert_media_to_audio(input_path, output_path, format_options, ffmpeg_executable):
    """
    指定されたメディアファイルを指定された音声フォーマットに変換する。

    Args:
        input_path (Path): 入力ファイルのPathオブジェクト。
        output_path (Path): 出力ファイルのPathオブジェクト。
        format_options (dict): 全フォーマットのオプションを含む辞書 (TARGET_FORMATキーでアクセス)。
        ffmpeg_executable (str): 使用するFFmpeg実行ファイルのパスまたはコマンド名。

    Returns:
        bool: 変換が成功した場合はTrue、失敗した場合はFalse。
    """
    command = [
        ffmpeg_executable,
        '-i', str(input_path),  # 入力ファイル
        # '-n', # 同名ファイルが存在する場合、エラー終了させる場合 (Python側でチェック済)
        # '-y', # 同名ファイルが存在する場合、常に上書きする場合 (今回はスキップ)
    ]
    # TARGET_FORMAT に対応するオプションを取得して追加
    options_for_target = format_options.get(TARGET_FORMAT) # .get()を使用
    if options_for_target:
        command.extend(options_for_target)
    else:
        print(get_text("warning_target_format_options", target_format=TARGET_FORMAT))
        command.append('-vn') # 最低限、映像は削除

    command.append(str(output_path)) # 出力ファイル

    print(get_text("converting_file", input_filename=input_path.name, output_filename=output_path.name))
    # print(f"実行コマンド: {' '.join(command)}") # デバッグ用

    try:
        # Windowsでコンソールウィンドウを非表示にするための設定
        startupinfo = None
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            startupinfo=startupinfo
        )

        print(get_text("conversion_success", filename=output_path.name))
        # print("--- FFmpeg stdout ---")
        # print(process.stdout)
        # print("--- FFmpeg stderr ---")
        # print(process.stderr)
        return True

    except subprocess.CalledProcessError as e:

        print(get_text("error_ffmpeg_conversion", filename=input_path.name))
        print(get_text("error_return_code", code=e.returncode))
        # stderrにエラー詳細が含まれることが多い
        print(get_text("error_ffmpeg_stderr", stderr=e.stderr))
        # 失敗した出力ファイルを削除
        if output_path.exists():
            try:
                output_path.unlink()
                print(get_text("deleted_failed_output", filename=output_path.name))
            except OSError as unlink_err:
                print(get_text("warning_delete_failed_output", filename=output_path.name, error=unlink_err))
        return False
    except FileNotFoundError: # ffmpeg_executableが見つからない場合
        print(get_text("error_ffmpeg_command_not_found", command=ffmpeg_executable))
        # find_ffmpegで見つからなかった場合もここに到達する可能性があるのでFalseを返す
        return False
    except Exception as e:
        print(get_text("error_unexpected", filename=input_path.name, error=e))
        return False

# --- メイン処理 ---
if __name__ == "__main__":
    print(get_text("processing_start"))
    print(get_text("input_folder_info", input_dir=INPUT_DIR))
    print(get_text("output_folder_info", output_dir=OUTPUT_DIR))
    print(get_text("target_format_info", target_format=TARGET_FORMAT))

    # FFmpeg実行ファイルを探す
    ffmpeg_exec = find_ffmpeg()
    if not ffmpeg_exec: # find_ffmpegがNoneを返した場合 (ローカルに見つからなかった場合)
         # find_ffmpegがNoneを返すのは、ローカルに見つからなかった場合
         # shutil.whichをここで呼ぶか、エラーメッセージを出す
         print(get_text("error_ffmpeg_not_found"))
         print(get_text("error_ffmpeg_not_found_msg1"))
         print(get_text("error_ffmpeg_not_found_msg2", ffmpeg_name='ffmpeg.exe' if platform.system() == "Windows" else 'ffmpeg'))
         print(get_text("error_ffmpeg_not_found_msg3", script_dir=SCRIPT_DIR))
         input(get_text("press_any_key_to_exit"))
         sys.exit(1)
    else:
        print(get_text("ffmpeg_in_use", ffmpeg_path=ffmpeg_exec)) # 表示上はパスまたはコマンド名


    # 設定ファイルから読み込んだFFmpegオプションと拡張子の内容確認
    if not FFMPEG_OPTIONS:
        print(get_text("warning_config_options_missing"))
        # 必要であればここで処理を中断するなどの対応
    if not SUPPORTED_INPUT_EXTENSIONS:
        print(get_text("warning_config_extensions_missing"))
        # 必要であればここで処理を中断するなどの対応

    # 出力フォーマットのオプション存在確認
    if TARGET_FORMAT not in FFMPEG_OPTIONS:
        print(get_text("target_format_is_notexist", target_format=TARGET_FORMAT))
        if FFMPEG_OPTIONS: # オプション自体が読み込めていれば表示
             print(get_text("available_formats", formats=', '.join(FFMPEG_OPTIONS.keys())))
        input(get_text("press_any_key_to_exit"))
        sys.exit(1)

    # 出力フォルダが存在しない場合は作成
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(get_text("error_create_output_folder", output_dir=OUTPUT_DIR, error=e))
        input(get_text("press_any_key_to_exit"))
        sys.exit(1)

    # 入力フォルダの存在確認
    if not INPUT_DIR.exists():
        print(get_text("error_input_folder_not_found", input_dir=INPUT_DIR))
        print(get_text("error_input_folder_create_msg", input_dir_name=INPUT_DIR_NAME))
        input(get_text("press_any_key_to_exit"))
        sys.exit(1)
    elif not INPUT_DIR.is_dir():
        print(get_text("error_input_path_is_not_dir", input_dir=INPUT_DIR))
        print(get_text("error_input_create_dir_msg", input_dir_name=INPUT_DIR_NAME))
        input(get_text("press_any_key_to_exit"))
        sys.exit(1)

    success_count = 0
    failure_count = 0
    skipped_count = 0
    processed_files = 0 # 処理対象として認識したファイル/フォルダの総数

    print(get_text("conversion_start_separator"))

    # 入力フォルダ内のファイルを処理
    try:
        items_in_input = list(INPUT_DIR.iterdir())
    except OSError as e:
        print(get_text("error_read_input_folder", input_dir=INPUT_DIR, error=e))
        input(get_text("press_any_key_to_exit"))
        sys.exit(1)

    if not items_in_input:
        print(get_text("input_folder_empty"))
    elif not SUPPORTED_INPUT_EXTENSIONS: # 処理対象拡張子が空なら何もしない
        print(get_text("warning_empty_extensions_config"))
    else:
        total_items = len(items_in_input)
        # first_ffmpeg_error = True # FFmpeg初回実行エラーフラグ (convert_media_to_audio内で処理するため不要)
        for i, item_path in enumerate(items_in_input):
            processed_files += 1
            print(get_text("processing_progress", current=i+1, total=total_items, filename=item_path.name))

            if item_path.is_file():
                input_extension = item_path.suffix.lower()

                if input_extension in SUPPORTED_INPUT_EXTENSIONS:
                    output_filename = item_path.stem + '.' + TARGET_FORMAT
                    output_path = OUTPUT_DIR / output_filename

                    if output_path.exists():
                        print(get_text("skip_file_exists", filename=output_path.name))
                        skipped_count += 1
                    else:
                        # FFMPEG_OPTIONS全体を渡す
                        conversion_result = convert_media_to_audio(item_path, output_path, FFMPEG_OPTIONS, ffmpeg_exec)
                        if conversion_result:
                            success_count += 1
                        else:
                            failure_count += 1
                else:
                    print(get_text("skip_unsupported_extension", filename=item_path.name, extension=input_extension))
                    skipped_count += 1
            elif item_path.is_dir():
                 print(get_text("skip_is_directory", name=item_path.name))
                 skipped_count += 1
            else:
                 print(get_text("skip_not_file_or_dir", name=item_path.name))
                 skipped_count += 1

    print(get_text("conversion_end_separator"))
    print(get_text("processing_result_header"))
    print(get_text("result_total_items", count=processed_files))
    print(get_text("result_success_count", count=success_count))
    print(get_text("result_failure_count", count=failure_count))
    print(get_text("result_skipped_count", count=skipped_count))

    if failure_count > 0:
        print(get_text("warning_failures_occurred"))

    print(get_text("processing_complete"))
    input(get_text("press_any_key_to_exit"))