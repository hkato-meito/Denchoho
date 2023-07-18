import os
import openai #OpenAIのAPI
import codecs
from dotenv import load_dotenv
from pdfminer.high_level import extract_text

# サブフォルダーを【除く】、フォルダー内のPDFファイルのリスト（配列）を取得
def get_pdf_paths(directory_path):
    pdf_paths = []
    for file in os.listdir(directory_path):
        if file.endswith(".pdf"):
            pdf_paths.append(os.path.join(directory_path, file))
    return pdf_paths

# サブフォルダーを含む、フォルダー内のPDFファイルのリスト（配列）を取得
def get_pdf_paths_including_subfolders(directory_path):
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

def main():
    # PDFファイルが入っているフォルダーを指定
    # directory_path = "C:\\Users\\hkato\\Documents\\vscode\\Denchoho\\"
    # main.pyのフォルダーを取得
    directory_path = os.path.dirname(os.path.abspath(__file__))
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
        # PDFファイルを読み込んで、PDF内のテキストを取得
        pdf_text = extract_text_from_pdf(pdf_path)
        # PDFファイルの内容（テキスト）をtxtファイルに出力
        write_text_to_file(pdf_path, pdf_text)

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
            model="gpt-4",                
            messages=[
                {
                    "role": "user", 
                    "content": prompt_text + pdf_text 
                },
            ],
        )

        # PDFファイル名のリストに、変更後のPDFファイル名を追加
        changed_pdf_filenames.append(res["choices"][0]["message"]["content"])

    # 変更前後のファイル名を表示
    for original, changed in zip(original_pdf_filenames, changed_pdf_filenames):
        print(f"{original}  ->  {changed}")
        
    for i, pdf_path in enumerate(pdf_paths):
        base_name = os.path.basename(pdf_path)
        if base_name in original_pdf_filenames:
            new_name = changed_pdf_filenames[original_pdf_filenames.index(base_name)]
            new_path = os.path.join(directory_path, new_name)
            os.rename(pdf_path, new_path)

if __name__ == "__main__":
    main()
