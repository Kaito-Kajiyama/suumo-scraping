import requests
import lxml.html
import pdb
import re
import json
import shutil
import time

#URLを取り込む
with open('suumo_url.json') as f:
    detail_url_list = json.load(f)

#すでに取得したデータは飛ばせるようにコピーファイルからコピー
shutil.copy('suumo_detail_copy.json', 'suumo_detail.json')

#抽出先のjsonファイルを読み込み
with open('suumo_detail.json', encoding="utf-8") as f:
    data_update = json.load(f)

for k in range(len(detail_url_list[0]["URL"])):
	print(k)

	#詳細を見るに移動
	response = requests.get(detail_url_list[0]["URL"][k])
	html = lxml.html.fromstring(response.content)

	#すでに掲載終了した物件の可能性があるため、価格を抽出しようとして、できないなら飛ばす
	try:
        #価格を抽出
		price = html.xpath("//div/span[contains(@class, 'emphasis')]")[0].text
		price = re.findall(r"(\d+\.?\d*)", price)

		#物件コードを抽出
		code = html.xpath("//th[contains(text(), 'SUUMO')]/following-sibling::td")[0].text

		#物件名を抽出
		name = html.xpath("//h1")[0].text
		
		#管理費・共益費を抽出
		manage_fee = html.xpath("//div/span[contains(text(), '管理費')]")[0].text
		manage_fee = re.findall(r"(\d+\.?\d*)", manage_fee)
		
		#敷金を抽出
		deposit = html.xpath("//div/span[contains(text(), '敷金')]")[0].text
		deposit = re.findall(r"(\d+\.?\d*)", deposit)
		
		#礼金を抽出
		key_money = html.xpath("//div/span[contains(text(), '礼金')]")[0].text
		key_money = re.findall(r"(\d+\.?\d*)", key_money)
		
		#所在地を抽出
		location = html.xpath("//th[contains(text(), '所在地')]/following-sibling::td")[0].text
		
		#駅徒歩何分かを抽出
		distance = html.xpath("//div[contains(text(), '駅')]")[0].text
		distance = re.findall(r"(\d+)", distance)
		
		#間取りを抽出
		layout = html.xpath("//th[contains(text(), '間取り')]/following-sibling::td")[0].text
		
		#専有面積を抽出
		exclusive_area = html.xpath("//th[contains(text(), '専有面積')]/following-sibling::td")[0].text
		exclusive_area = re.findall(r"(\d+\.?\d*)", exclusive_area)

		#階を抽出
		floor = html.xpath("//th[contains(text(), '階')]/following-sibling::td")[0].text
		floor = re.findall(r"(\d+)", floor)
		
		#向きを抽出
		direction = html.xpath("//th[contains(text(), '向き')]/following-sibling::td")[0].text
		
		#建物種別を抽出
		room_type = html.xpath("//th[contains(text(), '建物種別')]/following-sibling::td")[0].text
		
		#構造を抽出
		structure = html.xpath("//th[contains(text(), '構造')]/following-sibling::td")[0].text
		structure = re.sub(r"(\s+)", "", structure) #空白を削除

		#被っているデータがあれば次のループへ
		if (code in data_update[0]["code"]) and (name in data_update[0]["name"]) and (location in data_update[0]["location"]) and (exclusive_area in data_update[0]["exclusive_area"]) and (layout in data_update[0]["layout"]):
			continue

		#データを追加
		data_update[0]["code"].append(code)
		data_update[0]["price"].append(price)
		data_update[0]["name"].append(name)
		data_update[0]["manage_fee"].append(manage_fee)
		data_update[0]["deposit"].append(deposit)
		data_update[0]["key_money"].append(key_money)
		data_update[0]["location"].append(location)
		data_update[0]["distance"].append(distance)
		data_update[0]["layout"].append(layout)
		data_update[0]["exclusive_area"].append(exclusive_area)
		data_update[0]["floor"].append(floor)
		data_update[0]["direction"].append(direction)
		data_update[0]["room_type"].append(room_type)
		data_update[0]["structure"].append(structure)

		#築年数を抽出して追加
		if html.xpath("//th[contains(text(), '築年数')]/following-sibling::td")[0].text == '新築':
			data_update[0]["age"].append('0')
		else:
			age = html.xpath("//th[contains(text(), '築年数')]/following-sibling::td")[0].text
			age = re.sub(r"(\D+)", "", age)
			data_update[0]["age"].append(age)
		
	except Exception as e:
		print("例外のURL : ", k, " 番目")
		time.sleep(5)
    
	#20単位で上書き
	if k % 1 == 0:
		with open('suumo_detail.json', 'w', encoding='utf-8') as output:
			json.dump(data_update, output, indent=2, ensure_ascii=False)

    #40単位でコピーを作成
	if k % 4 == 0:
		shutil.copy('suumo_detail.json', 'suumo_detail_copy.json')
