# Rewrites the game menu (<select id="gamesel">) on every page. Games newest release first.
import re,sys,os,json
R=sys.argv[1]
GAMES=[("za","gZa","Legends Z-A"),("sv","gSv","Scarlet & Violet"),("la","gLa","Legends: Arceus"),("bdsp","gBd","Brilliant Diamond & Shining Pearl"),("swsh","gSw","Sword & Shield"),("letsgo","gLetsgo","Let's Go"),("usum","gUs","Ultra Sun & Ultra Moon"),("sm","gSm","Sun & Moon"),("oras","gOr","Omega Ruby & Alpha Sapphire"),("xy","gXy","X & Y"),("b2w2","gB2","Black 2 & White 2"),("bw","gBw","Black & White"),("hgss","gHg","HeartGold & SoulSilver"),("dppt","gDp","Diamond, Pearl & Platinum"),("frlg","gFr","FireRed & LeafGreen"),("rse","gRs","Ruby, Sapphire & Emerald"),("gsc","gGs","Gold, Silver & Crystal"),("rby","gRb","Red, Blue & Yellow")]
GKEYS={'gLetsgo':{'ja':'Let\'s Go! ピカチュウ・イーブイ','fr':'Let\'s Go','de':'Let\'s Go','ko':'레츠고 피카츄·이브이','zh-Hant':'Let\'s Go! 皮卡丘／伊布','zh-Hans':'Let\'s Go! 皮卡丘／伊布'},'gRb':{"ja": "赤・青・ピカチュウ", "fr": "Rouge, Bleu et Jaune", "de": "Rot, Blau & Gelb", "ko": "레드·블루·피카츄", "zh-Hant": "紅／藍／皮卡丘", "zh-Hans": "红／蓝／皮卡丘"},'gGs':{"ja": "金・銀・クリスタル", "fr": "Or, Argent et Cristal", "de": "Gold, Silber & Kristall", "ko": "골드·실버·크리스탈", "zh-Hant": "金／銀／水晶", "zh-Hans": "金／银／水晶"},'gRs':{"ja": "ルビー・サファイア・エメラルド", "fr": "Rubis, Saphir et Émeraude", "de": "Rubin, Saphir & Smaragd", "ko": "루비·사파이어·에메랄드", "zh-Hant": "紅寶石／藍寶石／綠寶石", "zh-Hans": "红宝石／蓝宝石／绿宝石"},'gFr':{"ja": "ファイアレッド・リーフグリーン", "fr": "Rouge Feu et Vert Feuille", "de": "Feuerrot & Blattgrün", "ko": "파이어레드·리프그린", "zh-Hant": "火紅／葉綠", "zh-Hans": "火红／叶绿"},'gDp':{"ja": "ダイヤモンド・パール・プラチナ", "fr": "Diamant, Perle et Platine", "de": "Diamant, Perl & Platin", "ko": "디아루가·펄기아·기라티나", "zh-Hant": "鑽石／珍珠／白金", "zh-Hans": "钻石／珍珠／白金"},'gHg':{"ja": "ハートゴールド・ソウルシルバー", "fr": "Or HeartGold et Argent SoulSilver", "de": "HeartGold & SoulSilver", "ko": "하트골드·소울실버", "zh-Hant": "心金／魂銀", "zh-Hans": "心金／魂银"},'gBw':{'ja':'ブラック・ホワイト','fr':'Noir et Blanc','de':'Schwarz & Weiß','ko':'블랙·화이트','zh-Hant':'黑／白','zh-Hans':'黑／白'},'gB2':{'ja':'ブラック2・ホワイト2','fr':'Noir 2 et Blanc 2','de':'Schwarz 2 & Weiß 2','ko':'블랙2·화이트2','zh-Hant':'黑2／白2','zh-Hans':'黑2／白2'},'gXy':{'ja':'X・Y','fr':'X et Y','de':'X & Y','ko':'X·Y','zh-Hant':'X／Y','zh-Hans':'X／Y'},'gOr':{'ja':'オメガルビー・アルファサファイア','fr':'Rubis Oméga et Saphir Alpha','de':'Omega Rubin & Alpha Saphir','ko':'오메가루비·알파사파이어','zh-Hant':'終極紅寶石／始源藍寶石','zh-Hans':'终极红宝石／始源蓝宝石'},'gSm':{'ja':'サン・ムーン','fr':'Soleil et Lune','de':'Sonne & Mond','ko':'썬·문','zh-Hant':'太陽／月亮','zh-Hans':'太阳／月亮'},'gUs':{'ja':'ウルトラサン・ウルトラムーン','fr':'Ultra-Soleil et Ultra-Lune','de':'Ultrasonne & Ultramond','ko':'울트라썬·울트라문','zh-Hant':'究極之日／究極之月','zh-Hans':'究极之日／究极之月'},'gSw':{'ja':'ソード・シールド','fr':'Épée et Bouclier','de':'Schwert & Schild','ko':'소드·실드','zh-Hant':'劍／盾','zh-Hans':'剑／盾'},'gBd':{'ja':'ブリリアントダイヤモンド・シャイニングパール','fr':'Diamant Étincelant et Perle Scintillante','de':'Strahlender Diamant & Leuchtende Perle','ko':'브릴리언트 다이아몬드·샤이닝 펄','zh-Hant':'晶燦鑽石・明亮珍珠','zh-Hans':'晶灿钻石・明亮珍珠'},'gLa':{'ja':'レジェンズ アルセウス','fr':'Légendes Arceus','de':'Legenden Arceus','ko':'레전즈 아르세우스','zh-Hant':'傳說 阿爾宙斯','zh-Hans':'传说 阿尔宙斯'},'gSv':{'ja':'スカーレット・バイオレット','fr':'Écarlate et Violet','de':'Karmesin & Purpur','ko':'스칼렛·바이올렛','zh-Hant':'朱・紫','zh-Hans':'朱・紫'}}
def select(prefix,current,placeholder):
  opts=''.join(f'<option value="{prefix}{g}/" data-i18n="{k}"{" selected" if g==current else ""}>{label}</option>' for g,k,label in GAMES)
  if placeholder: opts='<option value="" data-i18n="gPick" selected hidden>Choose a game…</option>'+opts
  return f'<select id="gamesel" aria-label="Game" data-i18n-aria="gameA">{opts}</select>'
pages=[('index.html','','',True)]+[(g+'/index.html','../',g,False) for g,_,_ in GAMES if os.path.exists(f'{R}/{g}/index.html')]
for path,prefix,cur,ph in pages:
  p=f'{R}/{path}'; s=open(p).read()
  s,n=re.subn(r'<select id="gamesel".*?</select>',select(prefix,cur,ph),s,count=1,flags=re.S); assert n==1,path
  for key,tr in GKEYS.items():  # add missing translations next to gZa (hand-written JS objects or JSON-style generated ones)
    for lang,v in tr.items():
      base=s.find('const I18N')
      for head,kq in ((('"%s":{'%lang) if '-' in lang else ('%s:{'%lang),''),('"%s":{'%lang,'"')):
        i=s.find(head,base)
        if i>=0: break
      if i<0: continue
      j=s.find(kq+'gZa'+kq+':"',i)
      if j<0 and not kq: kq='"'; j=s.find('"gZa":"',i)
      seg_end=s.find('}},',i)
      if seg_end<0: seg_end=s.find('\n};',i)  # last language block
      if seg_end<0: seg_end=s.find('}};',i)
      if j<0 or j>seg_end or (kq+key+kq+':"') in s[i:seg_end]: continue
      k=s.find('"',j+len(kq+'gZa'+kq)+2)+1
      s=s[:k]+','+kq+key+kq+':'+json.dumps(v,ensure_ascii=False)+s[k:]
  open(p,'w').write(s); print('menu updated',path)
