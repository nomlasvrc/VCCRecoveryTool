# VCC Recovery Tool

## これは何？
PCが突然死するなどしてVRChat Creator Companion(VCC)が必要とする`settings.json`ファイルが壊れてしまったときにProjectsの復元をサポートするツールです。

## いつ使うの？
![Projectが無いVCCのスクリーンショット](Docs/screenshot.png)
こうなったときです。<br>

## 仕組みを教えて
あなたがアバターやワールドを作成・改変したUnity Projectsが初期フォルダの`%localappdata%\VRChatProjects`にあると**仮定して**、その中にあるフォルダをProjectsとしてVCCの`settings.json`に登録します。<br>
変更している場合や、VRChatProjectsにUnityProjectではないフォルダが含まれていた場合も確認の上処理を行いますので、普段使いするツールではありません。<br>
**VCCは親フォルダーを`Add Exsisting Project`するとその中にあるフォルダをProjectsとして追加します。本当にこのツールで行うべきか十分に考えたうえで使用してください。**

## どうやって使うの？
1. Pythonをインストール済みの方は`recovery.py`を、インストールしていない方や、よく分からない方は`recovery.exe`をダウンロードして起動
1. 「settings.json が壊れています。処理を中止します。」と表示された場合、`settings.json`を手動で修正するか、VCCを開いて初期化してからこのツールを再度起動（非推奨）
1. 画面の指示に従って復元

### 注意点
 - 追加候補はよく確認してください。UnityProject以外が含まれている可能性があります。
 - お気に入りや最終更新日時の情報が失われる不具合を確認しています。

## トラブルシューティング
> [!NOTE]
> バックアップや、古いPCなどから、Project自体は救出できたが、Project一覧には表示されない場合、VCCで親フォルダーを`Add Exsisting Project`してください。<br>
### 終了コード
|コード|理由|対処法|
|---|---|---|
|01|settings.jsonの検出失敗|他のユーザーや、バックアップなどの、`[ユーザー名]\AppData\Local\VRChatCreatorCompanion`にsettings.jsonとvcc.liteDbがないか確認してください。もしあれば、これらのファイルを`[自分のユーザー名]\AppData\Local\VRChatCreatorCompanion`に配置することで、Project一覧が復活するはずです。|
|02|settings.jsonが壊れている|手動で修正するか、VCCを開いて初期化してからこのツールを再度起動（非推奨）してください。|
|10|VRChatProjectsフォルダの検出失敗|管理者権限で再度実行してみてください。|
|20|Projectの検出失敗|`VRChatProjects`フォルダが空です。このツールでは何もできません。バックアップが無いかなどを確認してみてください。|
|30|Project登録済み|検出したProjectは既に全て登録されています。（これは開発者想定外のエラーです。）|
|00|ユーザーがキャンセル|-|
|99|その他のエラー|エラーメッセージを確認し、必要に応じてGitHubのIssueに報告してください。|

## ライセンスを教えて
MIT Licenseです。[ここ](LICENSE)に書いてあります。<br>
MIT Licenseということはこのツールは自己責任で使ってくださいということです。
