import os
import json
from lib.config_lib import cf_load

def lang_load(lang_code : str = None) -> object:
    """
    言語コードに基づいて言語ファイルを読み込む
    Args
    ----------
        lang_code (str): 読み込みたい言語のコード
    """
    global config_data, langfile_dir, lang_data
    if lang_code is None:
        lang_code = config_data.get("language")
    lang_file = os.path.join(langfile_dir, f"{lang_code}.json")
    default_lang_file = os.path.join(langfile_dir, f"{'en'}.json")

    try:
        with open(lang_file, "r", encoding="utf-8") as file:
            lang_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"警告: 言語ファイル '{lang_code}.json' が見つからないか、無効です。デフォルト言語を使用します。")
        try:
            with open(default_lang_file, "r", encoding="utf-8") as file:
                lang_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("エラー: デフォルト言語ファイル 'en.json' が見つからないか、無効です。プログラムを終了します。")
            exit(1)

def get_text(key, **key_args):
    """
    言語ファイルから言語コードに対応するメッセージを取得し、必要に応じてフォーマット
    Args
    ----------
        key (str): 抽出したい言語データのキー
        key_args (str): キーに埋め込む用の引数

    Returns:
    ----------
        object: 取り出した言語ファイルのjsonオブジェクト
    """
    global lang_data
    try:
        text = lang_data.get(key, key)
        return text.format(**key_args)
    except KeyError:
        return f"メッセージ '{key}' が見つかりません。"


config_data = cf_load()
langfile_dir = os.getcwd() + "/languages"
lang_data   = lang_load()
