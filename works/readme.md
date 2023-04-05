# LLMを利用するための方針

1. pdfファイルから文章を抽出
1. 文章をチャンクに分割
1. チャンクからキーワードを抽出
1. クエリからキーワードを抽出
1. クエリのキーワードから該当チャンクを抽出
1. 該当チャンクを抜いてきて、コンテキストを作成
1. コンテキストとクエリを合わせてGPTへのプロンプトを作成

## チャンクをどうやって作るか

「。」で区切って、300文字をギリギリ超えないまでの長さの文字列に区切る。最初の一個で超えたら、その文は捨てる。

## チャンクデータをどうやって持っとくか

- sqliteに入れる
- スキーマ
  - ファイルid
  - チャンクid
  - チャンク位置
  - キーワード