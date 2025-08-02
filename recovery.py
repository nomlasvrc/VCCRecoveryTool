import getpass
import os
import json
import time

# これを空欄以外にしておくと、このフォルダーをVRChatProjectsが保存された場所として使用します。
# フレンドさんにProjectの復旧を頼まれた方へ：もしProjectが保存されたフォルダが分かっているなら、これを変更して、pyinstaller等でexe化して送ってあげてください。
dev_project_folder = ""

def find_subdirectories(directory):
    """指定されたディレクトリ内のサブディレクトリを返す"""
    if os.path.exists(directory) and os.path.isdir(directory):
        return [os.path.join(directory, subdir) for subdir in os.listdir(directory) if os.path.isdir(os.path.join(directory, subdir))]
    return []

def update_settings_with_vrchat_projects():
    print("settings.jsonを確認中...")
    settings_path = os.path.join(os.getenv('LOCALAPPDATA'), 'VRChatCreatorCompanion', 'settings.json')
    
    try:
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as file:
                settings_data = json.load(file)
        else:
            print(f"終了コード01：settings.json が見つかりません。")
            return
    except json.JSONDecodeError:
        print("終了コード02：settings.json が壊れています。処理を中止します。")
        return
    except Exception as e:
        print(f"終了コード99：エラーが発生しました: {e}")
        return

    print("登録Projectを確認中...")
    current_projects = settings_data.get('userProjects', [])
    if current_projects:
        print()
        print("注意：既にProjectが登録されています。")
        print("お気に入りや最終更新日時の情報が失われるため、このツールの使用は非推奨です。")
        print("登録されているProjects: "+", ".join([os.path.basename(p) for p in current_projects]))
        time.sleep(2)
    else:
        print("既に登録されているProjectはありません。")

    print()

    print("VRChatProjectsフォルダの探索中...")
    if dev_project_folder:
        vrchat_projects_dir = dev_project_folder
        print(f"開発者モードがオンになっており、フォルダーが事前に設定されています！\n {vrchat_projects_dir}")
    else:
        vrchat_projects_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'VRChatProjects')

    if not os.path.exists(vrchat_projects_dir):
        print("現在のユーザー(" + getpass.getuser() + ")に VRChatProjects フォルダが見つかりませんでした。")
        confirm = input("他のユーザーのディレクトリを確認しますか？ (y/n): ").strip().lower()
        if confirm != 'y':
            print("終了コード00：処理を中止しました。")
            return

        user_dirs = [os.path.join("C:\\Users", user) for user in os.listdir("C:\\Users") if os.path.isdir(os.path.join("C:\\Users", user))]
        for user_dir in user_dirs:
            vrchat_projects_dir = os.path.join(user_dir, "AppData", "Local", "VRChatProjects")
            if os.path.exists(vrchat_projects_dir):
                print(f"{vrchat_projects_dir} ... Found!")
                break
            else:
                print(f"{vrchat_projects_dir} ... Not found.")
        else:
            print("終了コード10：他のユーザーにも VRChatProjects フォルダが見つかりませんでした。管理者としてもう一度実行してみてください。")
            return

    print()
    print("VRChatProjectsを見つけました。パス: " + vrchat_projects_dir)

    # VRChatProjects内のサブディレクトリを取得
    subdirectories = find_subdirectories(vrchat_projects_dir)
    if not subdirectories:
        print(f"終了コード20：{vrchat_projects_dir} 内にフォルダが見つかりませんでした。")
        return

    # 追加候補を表示
    new_projects = [subdir for subdir in subdirectories if subdir not in current_projects]
    if not new_projects:
        print("終了コード30：追加するProjectはありません。")
        return

    print()
    print("追加候補: "+", ".join(new_projects))
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
            print(f"終了コード99：settings.json の更新中にエラーが発生しました: {e}")
            return
    else:
        print("終了コード00：Projectsの追加をキャンセルしました。")
        return

# 実行
update_settings_with_vrchat_projects()
time.sleep(5)