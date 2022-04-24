import requests
import lxml.html
import pdb
import re
import pandas as pd
import time
import json
import shutil

#頭につくURL
fwd_url = 'https://suumo.jp'
#初期値
pre_code = 14101
#格納するためのリストを定義
first_url = []

#すでに取得したデータは飛ばせるようにコピー
shutil.copy('suumo_copy.json', 'suumo_url.json')

#既存のjsonファイルを読み込み
with open('suumo_url.json') as f:
	d_update = json.load(f)

#すべての区のページにそれぞれ飛んでまわす
for m in range(18): #18まで
	print('区が変わります')
	#最初のページ(横浜市内の地区ごとの賃貸マンション・アパート検索結果)のURLを用意
	first_url.append('https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=' + str(pre_code))
	pre_code += 1

    #検索結果のページに移動
	response = requests.get(first_url[m])
	html = lxml.html.fromstring(response.content)

	#区のすべての物件のURLを取得
	for i in range(200):
		print(i)
		elements_list = html.xpath("//td/a[contains(text(), '詳細を見る')]")
		for j in range(len(elements_list)):
	        #'詳細を見る'のURLを抽出
			detail_url = fwd_url + str(elements_list[j].attrib['href'])
			if detail_url in d_update:
				continue
	
	        #辞書オブジェクトの更新
			d_update[0]["URL"].append(detail_url)

		if i % 10 == 0:
	        #上書き
			with open('suumo_url.json', 'w') as f:
				json.dump(d_update, f, indent=2, ensure_ascii=False)

		#20単位でコピーを作成
		if i % 20 == 0:
			shutil.copy('suumo_url.json', 'suumo_copy.json')

	    #'次へ'のURLを取得して移動
		next_step = html.xpath("//p/a[contains(text(), '次へ') and contains(@href, 'ichiran')]")
		if next_step != []:
			next_url = fwd_url + str(next_step[0].attrib['href'])
			response = requests.get(next_url)
			html = lxml.html.fromstring(response.content)
		else:
			break

#pdb.set_trace()
	
#確認
#with open('suumo_url.json') as f:
    #print(f.read())