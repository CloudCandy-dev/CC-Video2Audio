import os
import json

def cf_change(key: str, value: any) -> int:
    """
    configs/config.jsonのデータを編集する関数

    Args
    ----------
        key (str): 変更したい設定のキー
        value (any): 新しい値

    Returns
    ----------
    int: 変更された値の数
    """

    # 変更カウンター
    change_count = 0

    try:
        # JSONファイルを読み込む
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        # キーが存在する場合は値を更新
        if key in config_data:
            if config_data[key] != value:
                config_data[key] = value
                change_count += 1

        # 変更をファイルに保存
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

        return change_count

    except FileNotFoundError:
        raise FileNotFoundError("設定ファイルが見つかりません: " + config_path)
    except json.JSONDecodeError:
        raise ValueError("設定ファイルの形式が不正です")

def cf_load() -> object:
    """
    configs/config.jsonから設定データを取得する関数

    Returns
    ----------
        object: 変更された値の数
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"post_info": "md", "save_info": True}


# 設定ファイルのパスを取得
config_path = "/configs/config.json"
config_path = os.path.join(os.getcwd() + config_path)
