import getpass
import os
import json
from pathlib import Path
import time

def find_subdirectories(directory):
    """指定されたディレクトリ内のサブディレクトリを返す"""
    if os.path.exists(directory) and os.path.isdir(directory):
        return [os.path.join(directory, subdir) for subdir in os.listdir(directory) if os.path.isdir(os.path.join(directory, subdir))]
    return []

def update_settings_with_vrchat_projects():
    settings_path = os.path.join(os.getenv('LOCALAPPDATA'), 'VRChatCreatorCompanion', 'settings.json')
    
    print(settings_path + "を確認中...")
    # settings.jsonの読み込みと検証
    try:
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as file:
                settings_data = json.load(file)
        else:
            print(f"{settings_path} が見つかりません。")
            return
    except json.JSONDecodeError:
        print("settings.json が壊れています。処理を中止します。")
        return
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return

    # 現在のuserProjectsキーの一覧を表示
    current_projects = settings_data.get('userProjects', [])
    if current_projects:
        print()
        print("既に登録されているProjects: ", end="")
        print(current_projects)
        print()
    else:
        print("既に登録されているProjectはありません。")

    # VRChatProjectsフォルダの探索
    vrchat_projects_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'VRChatProjects')

    if not os.path.exists(vrchat_projects_dir):
        print("現在のユーザー(" + getpass.getuser() + ")に VRChatProjects フォルダが見つかりませんでした。")
        confirm = input("他のユーザーのディレクトリを確認しますか？ (y/n): ").strip().lower()
        if confirm != 'y':
            print("処理を中止しました。")
            return

        user_dirs = [os.path.join("C:\\Users", user) for user in os.listdir("C:\\Users") if os.path.isdir(os.path.join("C:\\Users", user))]
        for user_dir in user_dirs:
            vrchat_projects_dir = os.path.join(user_dir, "AppData", "Local", "VRChatProjects")
            if os.path.exists(vrchat_projects_dir):
                break
        else:
            print("他のユーザーにも VRChatProjects フォルダが見つかりませんでした。管理者としてもう一度実行してみてください。")
            return

    print()
    print("VRChatProjectsを見つけました。パス: " + vrchat_projects_dir)

    # VRChatProjects内のサブディレクトリを取得
    subdirectories = find_subdirectories(vrchat_projects_dir)
    if not subdirectories:
        print(f"{vrchat_projects_dir} 内にフォルダが見つかりませんでした。")
        return

    # 追加候補を表示
    new_projects = [subdir for subdir in subdirectories if subdir not in current_projects]
    if not new_projects:
        print("追加するProjectはありません。")
        return

    print()
    print("追加候補: ", end="")
    print(new_projects)
    print()

    # ユーザーに確認
    confirm = input("これらのProjectsを追加しますか？ (y/n): ").strip().lower()
    if confirm == 'y':
        current_projects.extend(new_projects)
        settings_data['userProjects'] = current_projects

        # settings.jsonの書き込み
        try:
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(settings_data, file, indent=2, ensure_ascii=False)
            print("settings.json を更新しました。")
        except Exception as e:
            print(f"settings.json の更新中にエラーが発生しました: {e}")
    else:
        print("Projectsの追加をキャンセルしました。")

# 実行
update_settings_with_vrchat_projects()
time.sleep(5)