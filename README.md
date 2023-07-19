# Denchoho
フォルダー内の複数のPDF請求書ファイルの内容を読み取り、GPTで電子帳簿保存法対応のファイル名(yyyymmdd_会社名_金額.pdf)を作成しリネームする。
# 事前に必要なもの
OpenAPIのAPIキー
# 使い方
1. .env_templateを.envにリネームして、OpenAI API keyにあなたのAPIキーを書き込む。
2. 必要なPythonライブラリをインストールする。
3. main.pyと同じフォルダーに、請求書PDFファイル（複数可）を置く。
4. python main.py
# 注意点
- OpeAIのAPIを使うので、OpenAIに対して料金が発生することになります。
- まずは少数のPDFファイルかつ文字数が少ないPDFで試してください。
