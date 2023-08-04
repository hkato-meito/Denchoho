# Denchoho（電子帳簿保存法対応ファイル名変換）

フォルダー内の PDF 請求書ファイルの内容を読み取り、GPT で電子帳簿保存法対応のファイル名(yyyymmdd*会社名*金額.pdf)を作成しリネームする。

# 事前に必要なもの

OpenAPI の API キー

# 必要な Python ライブラリをインストールする

pip install openai  
pip install python-dotenv  
pip install pdfminer.six

# 使い方

1. .env_template を.env にリネームして、OpenAI API key にあなたの API キーを書き込む。
2. 必要な Python ライブラリをインストールする。
3. main.py と同じフォルダーに、請求書 PDF ファイル（複数可）を置く。
4. python main.py

# 注意点

- OpeAI の API を使うので、OpenAI に対して料金が発生することになります。
- まずは少数の PDF ファイルかつ文字数が少ない PDF で試してください。
