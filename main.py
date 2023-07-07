# develop branch

import os
import openai #OpenAIのAPI
import codecs
from dotenv import load_dotenv
from pdfminer.high_level import extract_text

# フォルダー内のPDFファイルのリスト（配列）を取得
def get_pdf_paths(directory_path):
    pdf_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))
    return pdf_paths

# PDFファイルを読み込んで、PDF内のテキストを取得
def extract_text_from_pdf(file_path):
    text = extract_text(file_path)
    # print(text)
    return text

# PDFの内容をテキストとしてtxtファイル（BOM付きUTF-8）に書き出す
def write_text_to_file(file_path, text):
    # ファイルパスから拡張子を除き、.txtを追加
    new_file_path = os.path.splitext(file_path)[0] + '.txt'

    # ファイルをUTF-8 BOMとして書き出す
    with codecs.open(new_file_path, 'w', 'utf-8-sig') as f:
        f.write(text)

##########################################

# PDFファイルが入っているフォルダーを指定
directory_path = "C:\\Users\\hkato\\Documents\\vscode\\Denchoho\\"
# フォルダー内のPDFファイルの配列pdf_pathsを取得
pdf_paths = get_pdf_paths(directory_path)
# 変更前のPDFファイル名
original_pdf_filenames = []
# 変更後のPDFファイル名
changed_pdf_filenames = []

# .envからOpenAI APIキーを取得しセット
load_dotenv()
openai.api_key = os.getenv("API_KEY")

for pdf_path in pdf_paths:
  original_pdf_filenames.append(os.path.basename(pdf_path))
  # pdf_path = "C:\\Users\\hkato\\Documents\\vscode\\Denchoho\\アマゾン.pdf"
  # PDFファイルを読み込んで、PDF内のテキストを取得
  pdf_text = extract_text_from_pdf(pdf_path)
  # PDFファイルの内容（テキスト）をtxtファイルに出力
  write_text_to_file(pdf_path, pdf_text)

  # prompt_text = "日本では2023年4月1日から、中小企業でも1か月間の法定労働時間が60時間を超える時間の割増賃金率が上がります。この件について、1000文字程度でブログを書いてください。"

  # プロンプトの命令部分を指定（この後、PDF請求書内のテキストをpdf_textで指定する）
  prompt_text = """
                次の請求書PDFのテキストから
                ＜請求日＞_＜請求元会社名＞_＜請求金額＞.pdf
                というファイル名を作ってください。
                条件：
                ・＜請求日＞、＜請求元会社名＞、＜請求金額＞の形式は以下の通りとしてください。
                  ＜請求日＞はyyyymmdd
                  ＜請求元会社名＞は会社名フルネーム
                  ＜請求元会社名＞は3桁カンマ区切りは入れず、通貨がドルの場合は数字の先頭に$を付ける（通貨が円または\の場合は数字のみとする）
                ・回答の最後にファイル名のみ表示してください。

                  請求書：
                """

  # resにAPIのレスポンスが格納される
  res = openai.ChatCompletion.create(
    model="gpt-4",                # ChatGPTのモデルを選択
    # model="gpt-3.5-turbo",        # ChatGPTのモデルを選択する
    # temperature=1.0,              # 手堅い [0.1, 0.5, 1.0, 1.5, 2.0] 独創的
    # max_tokens=500,               # 生成するトークンの最大数(GPT-4モデルの上限は8,192トークン)
    messages=[
        # {"role": "system",
        #  "content": "あなたは社内の総務担当者です。userの指示に従って文章を作成してください。"
        # },
        {
            "role": "user", # role(役割)をsystem, user, assistantの3種類から選択する
            "content": prompt_text + pdf_text # プロンプトとPDFのテキストを指定
        },
    ],
  )

  # レスポンス（res）を出力する
  print(res)
  # レスポンス（res）の中から返答のみを指定して出力する
  # print(res["choices"][0]["message"]["content"])
  
  # PDFファイル名のリストに、変更後のPDFファイル名を追加
  changed_pdf_filenames.append(res["choices"][0]["message"]["content"])

# 変更前後のファイル名を表示
for original, changed in zip(original_pdf_filenames, changed_pdf_filenames):
    print(f"{original}  ->  {changed}")
