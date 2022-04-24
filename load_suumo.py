import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd
import pdb
from gspread_dataframe import get_as_dataframe, set_with_dataframe

#スクレイピングしたデータを取り込む
with open('suumo_detail.json', encoding="utf-8") as f:
    detail_list = json.load(f)

#空の辞書を定義
all_dict = {}

#{"key":value1, value2}の形に変形
for key, value in detail_list[0].items():
    all_dict[key] = value

#データフレームにする
df = pd.DataFrame(all_dict)

#findallのせいでリストになってしまっているところを数値だけ抜き取る
#数値だけにしたいカラムを定義
features = ['price', 'manage_fee', 'deposit', 'key_money', 'distance', 'exclusive_area', 'floor']

for feature in features:
    df[feature] = df[feature].apply(lambda x : float(x[0]) if x != [] else '-') #欠損値を-とする


# お決まりの文句
# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
credentials = Credentials.from_service_account_file("scrayping-347106-8c11cf38aeb2.json", scopes=scope)
#OAuth2の資格情報を使用してGoogle APIにログイン。
gc = gspread.authorize(credentials)

#スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = '1R4SfQn_JPxtQXsbiK8AKaGTBRRNKaoPmg0d0_P_Gr3s'
# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

# シートの一覧を取得する。（リスト形式）
worksheets = workbook.worksheets()

# シートを開く
worksheet = workbook.worksheet('all_data')

#指定したシートにデータを反映
set_with_dataframe(worksheet, df.reset_index())
