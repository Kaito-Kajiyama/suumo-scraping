import requests
import lxml.html
import pdb
import re
import numpy as np
import pandas as pd
import json
import shutil

#URLを取り込む
with open('suumo_json.json') as f:
    detail_url_list = json.load(f)

#すでに取得したデータは飛ばせるようにコピーからコピー
shutil.copy('suumo_detail_copy.json', 'suumo_detail.json')

#既存のjsonファイルを読み込み
with open('suumo_detail.json', encoding="utf-8") as f:
    data_update = json.load(f)

for k in range(len(detail_url_list[0]["URL"])):
	print(k)

	#詳細を見るに移動
	response = requests.get(detail_url_list[0]["URL"][k])
	html = lxml.html.fromstring(response.content)

	#価格を抽出してみて、例外なら飛ばす
	try:
		#物件コードを抽出
		code = html.xpath("//th[contains(text(), 'SUUMO')]/following-sibling::td")[0].text

		#物件コードがすでに存在していたら次のループへ
		if code in data_update[0]["code"]:
			continue

		data_update[0]["code"].append(code)

        #価格を抽出
		price = html.xpath("//div/span[contains(@class, 'emphasis')]")[0].text
		price = re.findall(r"(\d+\.?\d*)", price)
		data_update[0]["price"].append(price)

		#物件名を抽出
		name = html.xpath("//h1")[0].text
		data_update[0]["name"].append(name)
		
		#管理費・共益費を抽出
		manage_fee = html.xpath("//div/span[contains(text(), '管理費')]")[0].text
		manage_fee = re.findall(r"(\d+\.?\d*)", manage_fee)
		data_update[0]["manage_fee"].append(manage_fee)
		
		#敷金を抽出
		deposit = html.xpath("//div/span[contains(text(), '敷金')]")[0].text
		deposit = re.findall(r"(\d+\.?\d*)", deposit)
		data_update[0]["deposit"].append(deposit)
		
		#礼金を抽出
		key_money = html.xpath("//div/span[contains(text(), '礼金')]")[0].text
		key_money = re.findall(r"(\d+\.?\d*)", key_money)
		data_update[0]["key_money"].append(key_money)
		
		#所在地を抽出
		location = html.xpath("//th[contains(text(), '所在地')]/following-sibling::td")[0].text
		data_update[0]["location"].append(location)
		
		#駅徒歩何分かを抽出
		distance = html.xpath("//div[contains(text(), '駅')]")[0].text
		distance = re.findall(r"(\d+)", distance)
		data_update[0]["distance"].append(distance)
		
		#間取りを抽出
		layout = html.xpath("//th[contains(text(), '間取り')]/following-sibling::td")[0].text
		data_update[0]["layout"].append(layout)
		
		#専有面積を抽出
		exclusive_area = html.xpath("//th[contains(text(), '専有面積')]/following-sibling::td")[0].text
		exclusive_area = re.findall(r"(\d+\.?\d*)", exclusive_area)
		data_update[0]["exclusive_area"].append(exclusive_area)
		
		#築年数を抽出
		if html.xpath("//th[contains(text(), '築年数')]/following-sibling::td")[0].text == '新築':
			data_update[0]["age"].append('0')
		else:
			age = html.xpath("//th[contains(text(), '築年数')]/following-sibling::td")[0].text
			age = re.sub(r"(\D+)", "", age)
			data_update[0]["age"].append(age)

		#階を抽出
		floor = html.xpath("//th[contains(text(), '階')]/following-sibling::td")[0].text
		floor = re.findall(r"(\d+)", floor)
		data_update[0]["floor"].append(floor)
		
		#向きを抽出
		direction = html.xpath("//th[contains(text(), '向き')]/following-sibling::td")[0].text
		data_update[0]["direction"].append(direction)
		
		#建物種別を抽出
		room_type = html.xpath("//th[contains(text(), '建物種別')]/following-sibling::td")[0].text
		data_update[0]["room_type"].append(room_type)
		
		#構造を抽出
		structure = html.xpath("//th[contains(text(), '構造')]/following-sibling::td")[0].text
		structure = re.sub(r"(\s+)", "", structure) #空白を削除
		data_update[0]["structure"].append(structure)

		if k % 10 == 0:
	        #上書き
			with open('suumo_detail.json', 'w', encoding='utf-8') as output:
				json.dump(data_update, output, indent=2, ensure_ascii=False)
		
	except Exception as e:
		print("例外のURL : ", k, " 番目")
    
    #100単位でコピーを作成
	if k % 100 == 0:
		shutil.copy('suumo_detail.json', 'suumo_detail_copy.json')
