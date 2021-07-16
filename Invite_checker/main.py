try:
	import requests
except:
	__import__("os").system("pip install requests")

while True:
	inviteLink = input(">> ")

	if not inviteLink:
		continue
	
	if inviteLink == "!exit":
		exit()

	inviteCode = inviteLink.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").replace("discord.gg/", "")
	url = "https://discord.com/api/v8/invites/" + inviteCode
	r = requests.get(url, {"with_counts": "true"}).json()

	if len(r) == 2:
		print("unknown invite")
		continue

	splash = f'https://cdn.discordapp.com/splashes/{r["guild"]["id"]}/{r["guild"]["splash"]}.png?size=256' if r["guild"]["splash"] else "無し"
	banner = f'https://cdn.discordapp.com/banners/{r["guild"]["id"]}/{r["guild"]["banner"]}.png?size=256' if r["guild"]["banner"] else "無し"
	bUrl = "https://discord.gg/" + r["guild"]["vanity_url_code"] if r["guild"]["vanity_url_code"] else "---"
	nsfw = "はい" if r["guild"]["nsfw"] else "いいえ"
	levels = ["無制限", "低 メール認証がされているアカウントのみ", "中 Discordに登録してから5分以上経過したアカウントのみ", "高 このサーバーのメンバーとなってから10分以上経過したメンバーのみ", "最高 電話認証がされているアカウントのみ"]
	ch = {"0": "テキストチャンネル", "2": "音声チャンネル", "4": "カテゴリ", "5": "ニュース", "6": "ストア"}[str(r["channel"]["type"])]
	boostContent = '\n'.join(r["guild"]["features"])

	try:
		u = r["inviter"]["username"] + "#" + r["inviter"]["discriminator"]
		uid = r["inviter"]["id"]
		ava = f"https://cdn.discordapp.com/avatars/{uid}/{r['inviter']['avatar']}?size=256"
		cou = r["inviter"]["public_flags"]
	except: u = uid = ava = cou = "---"
	print(f"""




{'='*50}
discord.gg/{inviteCode} の情報

招待コード                    : {r["code"]}
使用回数                      : {cou}
{'-'*50}
サーバー名                    : {r["guild"]["name"]}
サーバーID                    : {r["guild"]["id"]}
サーバーの説明                : {r["guild"]["description"] if r["guild"]["description"] else "無し"}
メンバー数                    : {r["approximate_member_count"]}
現在オンラインのメンバー数    : {r["approximate_presence_count"]}
バニティURL                   : {bUrl}
認証レベル                    : {levels[int(r["guild"]["verification_level"])]}
成人向け                      : {nsfw}
サーバーアイコン              : https://cdn.discordapp.com/icons/{r["guild"]["id"]}/{r["guild"]["icon"]}.png?size=256
招待時背景                    : {splash}
サーバーバナー                : {banner}
{'-'*50}
現在解放されているブーストコンテンツ
{boostContent}
{'-'*50}
チャンネル名                  : {r["channel"]["name"]}
チャンネルID                  : {r["channel"]["id"]}
チャンネルのタイプ            : {ch}
{'-'*50}
招待を作成した人の名前 + タグ : {u}
招待を作成した人のID          : {uid}
招待を作成した人のアイコン    : {ava}
{'='*50}




""")
