import discord
import os
import requests
import json
import random
import time
import asyncio
import tracemalloc

client = discord.Client()


#Trigger words　（ここにある単語をDiscord上で入力すると返事がもらえるよ） :
call_words = ["きょろくん！", "きょろさん！","kyorobot","KyoRoBot","きょろボット"]
morning = ["おはよう"]
afternoon = ["こんにちは","こんにちわ"]
evening = ["こんばんは","こんばんわ"]
night = ["おやすみ"]
negativedraw_words = ["絵が描けない", "描き方分からん"]
agree_words = ["わかる", "それな","面白い"]
grass_words = ["草"]
sad_words = ["ひどい", "黙れ", "だまれ"]
image_words = ["テスト","test"]
idea_words = ["アイデア", "案がない", "idea", ]
praise_words = ["えらい","よしよし"]
mimu_words = ["みむ語録","みむっち語録"]
esaba_words = ["絵鯖語録","餌場語録"]
mimu_typo = ["みのむっち","ミノムッチ"]
getcolor = ["色ください","色欲しい","getcolor"]#スマホで見れない、原因不明
pet = ["おて","おかわり","ふせ","おまわり","おすわり"] 
illustrivia = ["豆知識","trivia",]
sexualharassment_words = ["脱いで"]
bust_words = ["おっぱい"]
shit_words = ["うんち","うんこ"]
shiritori =  ["しりとり"]
janken = ["じゃんけん"]
nkodice = ["nkodice","NKODICE","んこだいす","んこダイス","ンコダイス"]

#replies : 
starter_encouragements = ["頑張ればできるって", "とりあえず描け", "しっかり考えて描こうね","絵に絶対的正解はない"]
starter_agreements = ["それな", "わかる", "きょろさんもそう思います"]
starter_grasswords = ["草","ほんと草","草生える","wwwww","笑った","草超えて林","草超えて森","草超えて林超えて森","草超えて林超えて森超えてモーリーファンタジーｗｗｗｗｗｗｗｗｗｗｗｗｗ"]
starter_apologize = ["ごめんね"]
starter_mimu_words = ["足長いやつは四捨五入したら足","かなしくなったね","生きてください","天然ロリだ！捕まえろ！！","ショタっていいよなぁ！！！(大声)"]
starter_esaba_words = [
"「おっぱい！！！！」　by玉子鼠",
"「草　アイデアみむ語録脱いできょろくん！いいこと言って　おて　絵が描けない案がないおすわり色ください流れ弾面白いみのむっちしりとり絵鯖語録おっぱい！ひどいうんちわかるじゃんけん」　by玉子鼠",
"「雷獣誕生日？？」　byサポタ",
"「ピン留めっすゾ！オラァ！！！」　byサポタ",
"「めすおちー＾～（気さくな）」　byサポタ",
"「おりこうだー」　byきょろ",
"「スネーカジリナヤ」　byきょろ",
"「にかがわしい…？」 by NIKA"
]
starter_pet = ["わん","わんわん","わーん","わんわん","わん","わん","俺は犬じゃない"]
starter_biglaugh = ["くっそツボってて草","大草原不可避"]
starter_sexualharassment = ["う　る　さ　い","な　ぐ　る　ぞ","えっち！！！！！！","何言ってんだオメー！！！！！"]
starter_bust_words = ["AAA","AA","A","B","C","D","E","F","G","H","I",]
starter_shit_words = ["あああああああああああああああああああああああああああああああ！！！！！！！！！！！（ﾌﾞﾘﾌﾞﾘﾌﾞﾘﾌﾞﾘｭﾘｭﾘｭﾘｭﾘｭﾘｭ！！！！！！ﾌﾞﾂﾁﾁﾌﾞﾌﾞﾌﾞﾁﾁﾁﾁﾌﾞﾘﾘｲﾘﾌﾞﾌﾞﾌﾞﾌﾞｩｩｩｩｯｯｯ！！！！！！！ )"]
starter_morning =["おはよう！","しっかり寝た？","いい朝だね！","…ハズキルーペのナムル……"]
starter_afternoon =["こんにちは！","こんにちわ！","今起きたわ"]
starter_evening =["ばんちゃ～","こんばんわ！","お風呂にする？ごはんにする？それとも渡し舟に乗る、降りしきる雪は、吹雪のようである･･･ 太宰治「父 」"]
starter_night = ["おやすみ！","いい夢見てね","暫しの別れ時、日輪が再び現れし時我らの道も再び交わることになるだろう"]
starter_illustrivia = [
  "通常レイヤー　：　下にあるレイヤーの色と、設定中のレイヤーの色をそのまま重ねます。",
  "比較（暗） : 下にあるレイヤーの色と、設定中のレイヤーの色を比較し、暗い方の色を採用して合成します。",
  "乗算 : 下にあるレイヤーの色と、設定中のレイヤーの色を掛け合わせて合成します。合成後は、元の色より暗い色になります。影などを塗る際に使用されます。",
  "焼き込みカラー : 銀塩写真の「焼き込み」のような効果が得られます。下のレイヤーの画像の色を暗くし、コントラストを強くしたあとに、設定中のレイヤーの色を合成します。",
  "焼き込み（リニア） : 下のレイヤーを暗くしたあとに、設定中のレイヤーの色を合成します。",
  "減算 : 下にあるレイヤーの色と、設定中のレイヤーの色を引いて合成します。合成後は、元の色より暗い色になります。",
  "比較（明） : 下にあるレイヤーの色と、設定中のレイヤーの色を比較し、明るい方の色を採用してそれぞれの色を合成します。",
  "スクリーン : 下にあるレイヤーの色を反転した状態で、設定中のレイヤーの色を掛け合わせて合成します。乗算の反対の効果が得られます。合成後は、元の色より明るい色になります。",
  "覆い焼きカラー : 下のレイヤーの画像の色を明るくし、コントラストを弱くします。色のメリハリが弱くなります。",
  "加算 : 下にあるレイヤーの色と、設定中のレイヤーの色を足します。デジタルで色を加算すると明るい色に変化します。",
  "加算（発光）：　下にあるレイヤーの色と、設定中のレイヤーの色を足します。デジタルで色を加算すると明るい色に変化します。【加算】よりも強い効果が得られます。",
  "オーバーレイ　：　明るい部分は[スクリーン]、暗い部分は[乗算]の効果が現れます。合成後は、明るい部分はより明るく、暗い部分はより暗く表示します。",
  "ソフトライト　：　重ねた色の濃度に応じて、結果が異なります。明るい色同士を重ねると[覆い焼き]のように明るく、暗い色同士を重ねると[焼き込み]のように暗く表示されます。色の部分に重ねずに描画した場合は白になります。",
  "ハードライト　：　重ねた色の濃度に応じて、結果が異なります。明るい色同士を重ねると[スクリーン]のように明るく、暗い色同士を重ねると[乗算]のように暗く表示されます。",
  "差の絶対値　：　下にあるレイヤーの色と、設定中のレイヤーの色を引いて、その絶対値を採用して先に描いた色の部分と合成します。",
  "色収差　：　レンズで画像を集光したときに、波長が異なる光ごとに色ずれを起こす現象のことです。 描いたイラストに色収差の効果を付けることで、余韻のある画面作りができます。"
]    


combination1 = ["活発な", "内気な", "照れ屋な","さみしがりな","いじっぱりな","やんちゃな","ゆうかんな","図太い","わんぱくな","能天気な","のんきな","ひかえめな","おっとりした","うっかり屋な","冷静な","穏やかな","おとなしい","慎重な","挑発的な","生意気な","臆病な","せっかちな","陽気な","無邪気な","照れ屋な","素直な","気まぐれな","メスガキな"]
combination2 = ["夏服の", "冬服の", "水着の","秋服の","冬服の","和服の","エプロン姿の","パーカーの","よそ行きの格好をした","もう近くまで来ている真夏の暑さを予感させるTシャツを着た","でっかいコートを着た","だらしない格好の","明らかにオーバーサイズなパーカーを着た","夜具をかついだような大きい着物を着ている","狂人のような真紅な着物を着ている","下着なのかワンピースなのか区別のつかない服を着た","無防備な水着姿を晒している","小さい帽子をちょんと乗せている","すっかり大人の形に身体が完成されている","黄色のTシャツを着た","一見不審者と見紛うほどに全身黒ずくめの服装をしている","アバンギャルドな服装の","コンビニ帰りみたいな服装の","季節感のない服装から全体的に安っぽさが漂う","色彩の強い服装の","見た目に無頓着な","サンタコスチュームの","全体的にトーンが統一された服装の"]

combination3 = ["15","16","17","18","19","20","21","22","23","24","25","26","27",]
combination4 = ["歳",]


def get_quote():
    response = requests.get("https://meigen.doodlenote.net/api/json.php")
    json_data = json.loads(response.text)
    quote = json_data[0]['meigen'] + " - " + json_data[0]['auther']
    return (quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if message.content.startswith('-inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('いいこと言って'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in getcolor):
      random_number = random. randint(0,16777215)
      hex_number = str(hex(random_number))
      hex_number2 ='#'+ hex_number[2:]
      
      embed = discord.Embed(color=random_number,title="この色とかどう？ : "+ hex_number2)
      embed.set_image(url="https://www.thecolorapi.com/id?hex="+ hex_number[2:] + "&format=svg")
      await message.channel.send(embed=embed)



    if any(word in msg for word in call_words):
        await message.channel.send("きょろさんだよ！" + (message.author.mention) + "さんの役に立てるといいな！")
        await message.channel.send("https://replit.com/@Kyoro/kyoroBot")

        embed = discord.Embed(color=0x272973,title="KyoRoBotのコマンドたち（仮）")
        embed.add_field(name="`アイデア`",value="イラストお題提供")
        embed.add_field(name="`絵鯖語録`",value="過去に生まれたいくつものパワーワード")
        embed.add_field(name="`色ください`",value="ランダムに色を提供してくれるよ")
        embed.add_field(name="`豆知識`",value="イラストに関わる豆知識を吐き散らかす")
        embed.add_field(name="`いいこと言って`",value="ランダムに名言を吐き散らかす")
        embed.add_field(name="`じゃんけん`",value="じゃんけんできるよ")
        embed.add_field(name="`しりとり`",value="文字数指定がついた一人しりとり")
        embed.add_field(name="`NKODICE`",value="流行りのサイコロゲーム（「ま」を「わ」に置き換えてあるよ）")
        embed.add_field(name="- - - - - - - -",value= "会話してると特定のキーワードに反応して会話に割り込んできたりもするよ")
        await message.channel.send(embed=embed)

    if any(word in msg for word in idea_words):
        await message.channel.send(
            random.choice(combination2) + random.choice(combination1) +
            random.choice(combination3) + random.choice(combination4))

    if any(word in msg for word in negativedraw_words):
        await message.channel.send(random.choice(starter_encouragements))

    if any(word in msg for word in agree_words):
        await message.channel.send(random.choice(starter_agreements))

    if any(word in msg for word in shit_words):
        await message.channel.send(random.choice(starter_shit_words))

    if any(word in msg for word in grass_words):
        await message.channel.send(random.choice(starter_grasswords))

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_apologize))

    if any(word in msg for word in sexualharassment_words):
        await message.channel.send(random.choice(starter_sexualharassment))

    if any(word in msg for word in morning):
        await message.channel.send(random.choice(starter_morning))
    
    if any(word in msg for word in afternoon):
        await message.channel.send(random.choice(starter_afternoon))

    if any(word in msg for word in evening):
        await message.channel.send(random.choice(starter_evening))
    
    if any(word in msg for word in night):
        await message.channel.send(random.choice(starter_night))


    if any(word in msg for word in image_words):
        await message.channel.send("起きてるよ～")

    if any(word in msg for word in praise_words):
        await message.channel.send("えへへ")

    if any(word in msg for word in pet):
        await message.channel.send(random.choice(starter_pet))
    
    if any(word in msg for word in bust_words):
        X = (random.choice(starter_bust_words))
        await message.channel.send((message.author.mention)+"さんは"+ X +"カップだよ！")
        if X == "AAA" :
          await message.channel.send("イカしたバンド名みたいだ！！")
        elif X == "AA":
          await message.channel.send("狭い隙間でも抜けられそうだね！！！")
        elif X == "A":
          await message.channel.send("えぇ！？")
        elif X == "B":
          await message.channel.send("Bを90度回転してみてごらん？それが君が夢見たものだよｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
        elif X == "C":
          await message.channel.send("Cを２つ並べればでかい")
        elif X == "D":
          await message.channel.send("めんせきにぶんのいちぱいあーるじじょう！")
        elif X == "E":
          await message.channel.send("Eとおもいます")
        elif X == "F":
          await message.channel.send("とてもでかい")
        elif X == "G":
          await message.channel.send("Gは視線にはたらくGravityのG")
        elif X == "H":
          await message.channel.send("エッッッッッ")
        elif X == "I":
          await message.channel.send("大凶筋")




    if any(word in msg for word in illustrivia):
      variable = random.choice(starter_illustrivia)
      await message.channel.send(variable)

      if variable ==  "色収差　：　レンズで画像を集光したときに、波長が異なる光ごとに色ずれを起こす現象のことです。 描いたイラストに色収差の効果を付けることで、余韻のある画面作りができます。" :
         await message.channel.send(file=discord.File('Chroma Abb.jpg'))
         await message.channel.send("こんなかんじだよ")

    if any(word in msg for word in mimu_typo):
        await message.channel.send("もしかして : みむっち")

    if any(word in msg for word in mimu_words):
        X = ("「" + random.choice(starter_mimu_words) + "」" + "  byみむ")
        embed = discord.Embed(color = 1234575,title = X)
        await message.channel.send(embed=embed)



    if any(word in msg for word in esaba_words):
        X = random.choice(starter_esaba_words)
        Y = random. randint(0,16777215)
        embed = discord.Embed(color = Y,title = X)
        await message.channel.send(embed=embed)

        if X == "「雷獣誕生日？？」　byサポタ" :
          await message.channel.send("ここボルトロスいる？")
          await message.channel.send(file=discord.File('ボルトロス.png'))

    if any(word in msg for word in shiritori):
      async def on_message(message):
        if message.author == client.user:
         return
      await message.channel.send(" いいよ！")
      X = random.randint(0,43)
      Y = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
      Z = (Y[int(X)])
      A = random.randint(5,20)
      C = 0
      channel = message.channel
      author = message.author
      win = "あなたの勝ち！"
      lose = "あなたの負け！"
      error = "ゲームが中断されました"
      async def reply_check(m):
        return (m.channel == channel) and m.author == author

      while C < 5 :
        B = random.randint(3,7)
        await message.channel.send((message.author.mention) + "さん、" + "「" + Z + "」" + "から始まる" + str(B) + "文字の" + "ひらがな言葉をいれて！" + "五回連続で出来たらあなたの勝ちだよ！")
        reply = await client.wait_for('message',check=reply_check)
        re = reply.content
        if re[0] != Z :
          await message.channel.send ("正しい文字から始まる言葉を入力しやがれください")
          result = error
          break
        Z = re[-1]
        
        if len(re) == B :
          C = C + 1
          if C < 5 :
            await message.channel.send ("次は「" + Z + "」だよ")
          else :
            result = win
        if len(re) != B :
          await message.channel.send ("正しい文字数を入力しやがれください")
          result = error
          break
        elif Z == 'ん':
          await message.channel.send ("いま「" + "ん" + "」で終わったなぁ！？ばぁーーーーーーーーーーーかｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
          result = lose
          break

      embed = discord.Embed(color=0x272973,title=result)
      await message.channel.send(embed=embed)

    if any(word in msg for word in janken):
        await message.channel.send(" いいよ！")
        await message.channel.send(" 最初はグー、")
        await message.channel.send(" じゃんけん...")
        embed = discord.Embed(color=0x272973,title="ぐー、ちょき、ぱーのどれかを打ってね")
        await message.channel.send(embed=embed)

        jkbot = random.choice(("ぐー", "ちょき", "ぱー"))
        A = 10
        
        draw = "引き分けだよ～"
        wn = "あなたの勝ち！"
        lst = random.choice(("きょろさんの勝ち！弱ｗｗｗｗｗｗｗｗｗｗｗｗやめたら？じゃんけん",
       "ふぁーーーーーーーーーーーｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ負けてやんのｗｗｗｗｗｗｗｗｗｗｗｗｗｗ","君ｗｗｗｗｗｗのｗｗ負ｗｗｗｗｗけｗｗｗｗｗだｗｗｗｗｗよｗｗｗｗｗｗｗｗｗｗ"))
        error = "正しく入力しやがれください"

        def jankencheck(m):
            return (m.author == message.author)

        reply = await client.wait_for("message", check=jankencheck,)
        if reply.content == jkbot:
            judge = draw
        else:
            if reply.content == "ぐー":
                if jkbot == "ちょき":
                    judge = wn
                else:
                    judge = lst

            elif reply.content == "ちょき":
                if jkbot == "ぱー":
                    judge = wn
                else:
                    judge = lst

            elif reply.content == "ぱー":
                if jkbot == "ぐー":
                    judge = wn
                else:
                    judge = lst

            elif reply.content != "ぐー"or"ちょき"or"ぱー" :
                judge = error
          
       


        await message.channel.send(jkbot)
        await message.channel.send(judge)
    

    if any(word in msg for word in nkodice):
      Dice = ["お","わ","ち","う","ん","こ",]

      A = random.choice(Dice)
      B = random.choice(Dice)
      C = random.choice(Dice)
      D = random.choice(Dice)
      E = random.choice(Dice)
      F = random.choice(Dice)
      G = random.choice(Dice)
      H = random.choice(Dice)
      I = random.choice(Dice)
      J = random.choice(Dice)

      result = A + B + C + D + E + F
      A = discord.Embed(color=random.randint(0,16777215),title=A)
      await message.channel.send(embed=A)
      B = discord.Embed(color=random.randint(0,16777215),title=B)
      await message.channel.send(embed=B)
      C = discord.Embed(color=random.randint(0,16777215),title=C)
      await message.channel.send(embed=C)
      D = discord.Embed(color=random.randint(0,16777215),title=D)
      await message.channel.send(embed=D)
      E = discord.Embed(color=random.randint(0,16777215),title=E)
      await message.channel.send(embed=E)
      F = discord.Embed(color=random.randint(0,16777215),title=F)
      await message.channel.send(embed=F)
      #G = discord.Embed(color=random.randint(0,16777215),title=G)
      #await message.channel.send(embed=G)
      #H = discord.Embed(color=random.randint(0,16777215),title=H)
      #await message.channel.send(embed=H)
      #I = discord.Embed(color=random.randint(0,16777215),title=I)
      #await message.channel.send(embed=I)
      #J = discord.Embed(color=random.randint(0,16777215),title=J)
      #await message.channel.send(embed=J)
      point = 0

      if "お" in result :
        if "う" in result : 
          if "ち" in result :
            point = point + 1
            ouchi = discord.Embed(color=random.randint(0,16777215),title="OUCHI")
            await message.channel.send(embed=ouchi)
        if "ち" in result :
          if result.count("ち") >= 2 :
            if result.count("ん") >= 2 :
              point = point + 1
              わんわん = discord.Embed(color=random.randint(0,16777215),title="OCHINCHIN")
              await message.channel.send(embed=わんわん)
          if "ん" in result :
            if "こ" in result :
              point = point + 1
              おちんこ = discord.Embed(color=random.randint(0,16777215),title="OCHINKO")
              await message.channel.send(embed=おちんこ)
        if "わ" in result :
          if "ん" in result :
            point = point + 1
            owan = discord.Embed(color=random.randint(0,16777215),title="OWAN")
            await message.channel.send(embed=owan)
        
      if "わ" in result :
        if result.count("わ") >= 2 :
          if result.count("ん") >= 2 :
            point = point + 1
            wanwan = discord.Embed(color=random.randint(0,16777215),title="WANWAN")
            await message.channel.send(embed=wanwan)
        if "ん" in result :
          if "こ" in result :
            point = point + 1
            wanko = discord.Embed(color=random.randint(0,16777215),title="WANKO")
            await message.channel.send(embed=wanko)
          
      if "ち" in result :
        if result.count("ち") >= 2 :
          if result.count("ん") >= 2 :
            point = point + 1
            おちんこ = discord.Embed(color=random.randint(0,16777215),title="CHINCHIN")
            await message.channel.send(embed=おちんこ)
        if "ん" in result :
          if "こ" in result : 
            point = point + 1
            ちんこ = discord.Embed(color=random.randint(0,16777215),title="CHINKO")
            await message.channel.send(embed=ちんこ)
        if result.count("わ") >= 2 :
          point = point + 1
          ちわわ = discord.Embed(color=random.randint(0,16777215),title="CHIWAWA")
          await message.channel.send(embed=ちわわ)
      
      if "う" in result :
        if "ん" in result :
          if "こ" in result :
            point = point + 1
            unko = discord.Embed(color=random.randint(0,16777215),title="UNKO")
            await message.channel.send(embed=unko)
          if "ち" in result :
            point = point + 1
            unchi = discord.Embed(color=random.randint(0,16777215),title="UNCHI")
            await message.channel.send(embed=unchi)
        if "ち" in result : 
          if "わ" in result :
            point = point + 1
            uchiwa = discord.Embed(color=random.randint(0,16777215),title="UCHIWA")
            await message.channel.send(embed=uchiwa)
    
      if point > 0 :
        await message.channel.send ("おめでとう" + (message.author.mention) + "さん、" + str(point) + "単語作れたね！")
      if point == 0 :
        await message.channel.send ("残念！またあそんでね！")


    if message.content.startswith('wwwww'):
      await message.channel.send(random.choice(starter_biglaugh))



    
my_secret = os.environ['TOKEN']
client.run(os.environ['TOKEN'])
