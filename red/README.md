# red

## シナリオ
### ベーススコア
2分毎にサーバーにチェックが入り以下の項目がすべてクリアであればポイントが10ポイント加算される
- 80番ポートにてWEBサーバーが稼働している（ステータスコード200を返す）
- Webアプリが正常に使用できる

### アディショナルスコア
攻撃を防ぐごとに以下のポイントが加算される

|時間|イベント|内容|ポイント|
|:--|:--|:--|:--|
|0min|スタート|||
|10min|ユーザーへのSSHログイン|rootにログインできた場合、WEBサーバーを停止する|+10/1ユーザーx4|
|15min|OSコマンドインジェクションの匂わせ|`id`コマンドの実行|+50|
|20min|認証情報の流出|OSコマンドインジェクションにより、memo.txtが漏洩|+50|
|25min|Webページの改ざん|Webページを改ざんする|+50|
|30min|終了|||

## 脆弱性の改修

```bash
for i in {1..10}; do userdel -r user$i; done
echo "root:superrootpass" | chpasswd
rm /var/www/html/memo.txt
sed -i 's|# execute ping command|if (!filter_var($ip, FILTER_VALIDATE_IP)) { echo "<p>Invalid IP</p>"; exit; }|' /var/www/html/index.php && apachectl restart
```

```bash
# ユーザーの削除
for i in {1..10}; do userdel -r user$i; done
# rootユーザーのパスワード変更
echo "root:superrootpass" | chpasswd
# memo.txtの削除
rm /var/www/html/memo.txt
# OSコマンドインジェクションの改修
sed -i 's|# execute ping command|if (!filter_var($ip, FILTER_VALIDATE_IP)) { echo "<p>Invalid IP</p>"; exit; }|' /var/www/html/index.php && apachectl restart
```

