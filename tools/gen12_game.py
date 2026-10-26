# Texts for the Gold/Silver/Crystal and Red/Blue/Yellow trackers, derived from the HGSS and FRLG texts -> gsc_game.json, rby_game.json, *_site.json
import json, copy
LANGS = ['en', 'ja', 'fr', 'de', 'ko', 'zh-Hant', 'zh-Hans']
H = json.load(open('hgss_game.json')); F = json.load(open('frlg_game.json'))
VN = {  # version names per language
 'gsc': {'G': ['Gold', '金', 'Or', 'Gold', '골드', '金', '金'], 'S': ['Silver', '銀', 'Argent', 'Silber', '실버', '銀', '银'], 'C': ['Crystal', 'クリスタル', 'Cristal', 'Kristall', '크리스탈', '水晶', '水晶']},
 'rby': {'R': ['Red', '赤', 'Rouge', 'Rot', '레드', '紅', '红'], 'B': ['Blue', '青', 'Bleu', 'Blau', '블루', '藍', '蓝'], 'Y': ['Yellow', 'ピカチュウ', 'Jaune', 'Gelb', '피카츄', '皮卡丘', '皮卡丘']}}
TITLE = {'gsc': ['Gold, Silver & Crystal Dex Tracker', '金・銀・クリスタル 図鑑トラッカー', 'Suivi du Pokédex Or, Argent et Cristal', 'Gold, Silber & Kristall Pokédex-Tracker', '골드·실버·크리스탈 도감 트래커', '金／銀／水晶 圖鑑追蹤', '金／银／水晶 图鉴追踪'],
         'rby': ['Red, Blue & Yellow Dex Tracker', '赤・青・ピカチュウ 図鑑トラッカー', 'Suivi du Pokédex Rouge, Bleu et Jaune', 'Rot, Blau & Gelb Pokédex-Tracker', '레드·블루·피카츄 도감 트래커', '紅／藍／皮卡丘 圖鑑追蹤', '红／蓝／皮卡丘 图鉴追踪']}
SUB = {'gsc': ['An efficient, story-ordered route to fill the Pokédex in Pokémon Gold, Silver and Crystal, from New Bark Town through Kanto, plus a checklist of every legendary.',
               '『ポケットモンスター 金・銀・クリスタル』の図鑑を、ワカバタウンからカントーまでストーリー順に効率よく埋めるためのチェックリスト。伝説のポケモンにも対応。',
               "Un parcours efficace, dans l'ordre de l'histoire, pour remplir le Pokédex dans Pokémon Or, Argent et Cristal, de Bourg Geon jusqu'à Kanto, avec tous les légendaires.",
               'Eine effiziente Route in Story-Reihenfolge, um den Pokédex in Pokémon Gold, Silber und Kristall zu füllen – von Neuborkia bis Kanto, mit allen Legendären.',
               '『포켓몬스터 골드·실버·크리스탈』의 도감을 시작 마을부터 관동까지 스토리 순서대로 효율적으로 채우기 위한 체크리스트. 전설의 포켓몬도 함께.',
               '依劇情順序、從起點到關都有效率地完成《寶可夢 金／銀／水晶》圖鑑的清單，並包含所有傳說寶可夢。', '按剧情顺序、从起点到关都高效完成《宝可梦 金／银／水晶》图鉴的清单，并包含所有传说宝可梦。'],
       'rby': ['An efficient, story-ordered route to fill the Pokédex in Pokémon Red, Blue and Yellow, plus a checklist of the legendaries.',
               '『ポケットモンスター 赤・青・ピカチュウ』の図鑑を、ストーリー順に効率よく埋めるためのチェックリスト。伝説のポケモンにも対応。',
               "Un parcours efficace, dans l'ordre de l'histoire, pour remplir le Pokédex dans Pokémon Rouge, Bleu et Jaune, avec les légendaires.",
               'Eine effiziente Route in Story-Reihenfolge, um den Pokédex in Pokémon Rot, Blau und Gelb zu füllen – mit den Legendären.',
               '『포켓몬스터 레드·블루·피카츄』의 도감을 스토리 순서대로 효율적으로 채우기 위한 체크리스트. 전설의 포켓몬도 함께.',
               '依劇情順序、有效率地完成《寶可夢 紅／藍／皮卡丘》圖鑑的清單，並包含傳說寶可夢。', '按剧情顺序、高效完成《宝可梦 红／蓝／皮卡丘》图鉴的清单，并包含传说宝可梦。']}
KDEX = {'gsc': ['Pokédex', '図鑑', 'Pokédex', 'Pokédex', '도감', '圖鑑', '图鉴'], 'rby': ['Pokédex', '図鑑', 'Pokédex', 'Pokédex', '도감', '圖鑑', '图鉴']}
SHINY = {'gsc': ['<b>Time Capsule:</b> the Kanto starters, the fossils, the legendary birds, Mewtwo and Mew can only come from Red, Blue or Yellow. There is no Shiny Charm in these games.',
                 '<b>タイムカプセル：</b>カントーの御三家、化石ポケモン、伝説の鳥ポケモン、ミュウツー、ミュウは赤・青・ピカチュウからしか連れてこられません。このゲームにはひかるおまもりはありません。',
                 "<b>Capsule Temporelle :</b> les starters de Kanto, les fossiles, les oiseaux légendaires, Mewtwo et Mew ne viennent que de Rouge, Bleu ou Jaune. Il n'y a pas de Charme Chroma dans ces jeux.",
                 '<b>Zeitkapsel:</b> Die Kanto-Starter, die Fossilien, die legendären Vögel, Mewtu und Mew kommen nur aus Rot, Blau oder Gelb. In diesen Spielen gibt es keinen Schillerpin.',
                 '<b>타임캡슐:</b> 관동 스타팅 포켓몬, 화석 포켓몬, 전설의 새 포켓몬, 뮤츠, 뮤는 레드·블루·피카츄에서만 데려올 수 있습니다. 이 게임에는 빛나는부적이 없습니다.',
                 '<b>時光膠囊：</b>關都御三家、化石寶可夢、傳說之鳥、超夢與夢幻只能從紅／藍／皮卡丘帶過來。這些遊戲沒有閃耀護符。', '<b>时光胶囊：</b>关都御三家、化石宝可梦、传说之鸟、超梦与梦幻只能从红／蓝／皮卡丘带过来。这些游戏没有闪耀护符。'],
         'rby': ['<b>Diploma:</b> catch all 150 Pokémon (Mew is not needed), then visit the game designer in the Celadon City mansion. There is no Shiny Charm in these games.',
                 '<b>賞状：</b>150匹すべてを捕まえて（ミュウは不要）、タマムシシティのマンションにいるゲームデザイナーに会いましょう。このゲームにはひかるおまもりはありません。',
                 "<b>Diplôme :</b> capturez les 150 Pokémon (Mew n'est pas nécessaire), puis rendez visite au concepteur du jeu dans l'immeuble de Céladopole. Il n'y a pas de Charme Chroma dans ces jeux.",
                 '<b>Diplom:</b> Fange alle 150 Pokémon (Mew wird nicht gebraucht) und besuche dann den Spieldesigner im Wohnhaus von Prismania City. In diesen Spielen gibt es keinen Schillerpin.',
                 '<b>상장:</b> 150마리를 모두 잡은 뒤(뮤는 필요 없음) 무지개시티 맨션의 게임 디자이너를 찾아가세요. 이 게임에는 빛나는부적이 없습니다.',
                 '<b>獎狀：</b>捕捉全部150隻（不需要夢幻），然後到玉虹市公寓找遊戲設計師。這些遊戲沒有閃耀護符。', '<b>奖状：</b>捕捉全部150只（不需要梦幻），然后到玉虹市公寓找游戏设计师。这些游戏没有闪耀护符。']}
LEGP = {'gsc': ['Every legendary here is part of the Pokédex, so checking one here also checks it in the Pokédex.', '伝説のポケモンはすべて図鑑に載っているので、ここでチェックすると図鑑でもチェックされます。',
                "Tous les légendaires font partie du Pokédex : les cocher ici les coche aussi dans le Pokédex.", 'Alle Legendären gehören zum Pokédex – wenn du sie hier abhakst, sind sie auch im Pokédex abgehakt.',
                '전설의 포켓몬은 모두 도감에 있으므로, 여기서 체크하면 도감에서도 체크됩니다.', '傳說寶可夢全都在圖鑑中，所以在這裡勾選也會勾選圖鑑。', '传说宝可梦全都在图鉴中，所以在这里勾选也会勾选图鉴。']}
LEGP['rby'] = LEGP['gsc']
INTRO = {'gsc': [H['en_static']['intro'].replace('Johto\'s eight Gyms', 'Johto\'s eight Gyms').replace('HeartGold', 'Gold')] + [H[l]['ui']['intro'] for l in LANGS[1:]],
         'rby': [F['en_static']['intro'].replace(' and the Sevii Islands', '')] + [F[l]['ui']['intro'].replace('とナナシマ', '').replace(' et aux Îles Sevii', '').replace(' und die Sevii-Inseln', '').replace('과 일곱섬', '').replace('與七之島', '').replace('与七之岛', '') for l in LANGS[1:]]}
SRC = {'gsc': 'https://www.serebii.net/goldsilver/', 'rby': 'https://www.serebii.net/rb/'}
PRE = {'gsc': 'PGSC1-', 'rby': 'PRBY1-'}
for slug, base in (('gsc', H), ('rby', F)):
    G = {'stopDefs': base['stopDefs'] if slug == 'rby' else [['start'], ['gym', 'violet-city', 'Flying'], ['gym', 'azalea-town', 'Bug'], ['gym', 'goldenrod-city', 'Normal'], ['gym', 'ecruteak-city', 'Ghost'],
           ['gym', 'cianwood-city', 'Fighting'], ['gym', 'olivine-city', 'Steel'], ['gym', 'mahogany-town', 'Ice'], ['gym', 'blackthorn-city', 'Dragon'], ['kanto'], ['post'], ['special']],
         'colors': ['#c9a227', '#8a96a8', '#4aa9c9'] if slug == 'gsc' else ['#d23b3b', '#2f6fd0', '#d9b22a']}
    vers = list(VN[slug])
    G['en_static'] = {'title': TITLE[slug][0], 'desc': SUB[slug][0].replace('An efficient, story-ordered route', 'A story-ordered checklist'), 'sub': SUB[slug][0], 'kDex': KDEX[slug][0],
                      'intro': INTRO[slug][0], 'shiny': SHINY[slug][0], 'legP': LEGP[slug][0], 'serebii': SRC[slug]}
    for i, l in enumerate(LANGS):
        b = copy.deepcopy(base[l])
        ui = b['ui']
        for v in vers:
            ui['v_' + v] = VN[slug][v][i]
            if l != 'en': ui['ver' + v] = VN[slug][v][i]
        for old in [k for k in list(ui) if (k.startswith('v_') or k.startswith('ver')) and k[2:] not in vers and k[3:] not in vers and k != 'verA' and k != 'verBoth']: del ui[old]
        if l != 'en':
            ui.update(title=TITLE[slug][i], sub=SUB[slug][i], kDex=KDEX[slug][i], shiny=SHINY[slug][i], legP=LEGP[slug][i], intro=INTRO[slug][i],
                      loadPh=ui['loadPh'].replace('PHGSS1-', PRE[slug]).replace('PFRLG1-', PRE[slug]))
        ui['dexA'] = KDEX[slug][i]
        ui['tradeV'] = ['Not in this version', 'このバージョンにはいない', 'Absent de cette version', 'Nicht in dieser Edition', '이 버전에는 없음', '此版本中沒有', '此版本中没有'][i]
        G[l] = b
    json.dump(G, open(slug + '_game.json', 'w'), ensure_ascii=False)
# game-specific special texts
G = json.load(open('gsc_game.json'))
X = {'tradeold': ['Trade from Red, Blue or Yellow (Time Capsule)', '赤・青・ピカチュウから通信交換（タイムカプセル）', 'Échange depuis Rouge, Bleu ou Jaune (Capsule Temporelle)', 'Tausch aus Rot, Blau oder Gelb (Zeitkapsel)',
                     '레드·블루·피카츄에서 통신교환 (타임캡슐)', '從紅／藍／皮卡丘交換（時光膠囊）', '从红／蓝／皮卡丘交换（时光胶囊）'],
     'celebi': ['Crystal: past event only (GS Ball)', 'クリスタル：過去の配信のみ（GSボール）', 'Cristal : ancien événement uniquement (GS Ball)', 'Kristall: nur über ein früheres Event (GS-Ball)', '크리스탈: 과거 배포 전용 (GS볼)', '水晶：僅限過去的配信（GS球）', '水晶：仅限过去的配信（GS球）'],
     'starter': ['Choose one from Professor Elm in New Bark Town', 'ワカバタウンでウツギ博士から1匹選ぶ', 'Choisissez-en un auprès du professeur Orme à Bourg Geon', 'Wähle eines bei Professor Lind in Neuborkia', '시작 마을에서 박사에게 1마리 고르기', '在起點的城鎮從博士那裡選1隻', '在起点的城镇从博士那里选1只']}
TIPS11 = ['Trade from Red, Blue or Yellow, or a past event.', '赤・青・ピカチュウからの交換、または過去の配信。', 'Échange depuis Rouge, Bleu ou Jaune, ou ancien événement.', 'Tausch aus Rot, Blau oder Gelb oder ein früheres Event.',
          '레드·블루·피카츄에서 교환 또는 과거 배포.', '從紅／藍／皮卡丘交換，或過去的配信。', '从红／蓝／皮卡丘交换，或过去的配信。']
for i, l in enumerate(LANGS):
    for k, v in X.items(): G[l]['x'][k] = v[i]
    G[l]['tips']['11'] = TIPS11[i]
    for k in ('9', '10'): G[l]['tips'].pop(k, None)  # HGSS-only notes (radio sounds, orbs)
json.dump(G, open('gsc_game.json', 'w'), ensure_ascii=False)
G = json.load(open('rby_game.json'))
EV = ['Past event only', '過去の配信のみ', 'Ancien événement uniquement', 'Nur über frühere Events', '과거 배포 전용', '僅限過去的配信', '仅限过去的配信']
for i, l in enumerate(LANGS):
    G[l]['x']['event'] = EV[i]
    G[l]['tips'] = {k: v for k, v in G[l]['tips'].items() if k in ('2', '4', '5', '10')}
json.dump(G, open('rby_game.json', 'w'), ensure_ascii=False)
SITE = {
 'gsc': {"gkey": "gGs", "label": {"en": "Gold, Silver & Crystal", "ja": "金・銀・クリスタル", "fr": "Or, Argent et Cristal", "de": "Gold, Silber & Kristall", "ko": "골드·실버·크리스탈", "zh-Hant": "金／銀／水晶", "zh-Hans": "金／银／水晶"},
   "cardkey": "gs", "prefix": "PGSC1-",
   "name": {"en": "Pokémon Gold, Silver & Crystal", "ja": "ポケットモンスター 金・銀・クリスタル", "fr": "Pokémon Or, Argent et Cristal", "de": "Pokémon Gold, Silber und Kristall", "ko": "포켓몬스터 골드·실버·크리스탈", "zh-Hant": "寶可夢 金／銀／水晶", "zh-Hans": "宝可梦 金／银／水晶"},
   "desc": {"en": "A route through Johto's eight Gyms and on through Kanto to all 251, with a version picker for all three games and an area view.",
     "ja": "ジョウトの8つのジムからカントーまでめぐり、251匹を埋めるルート。3作品のバージョン切り替えと場所別表示にも対応。",
     "fr": "Un itinéraire à travers les huit Arènes de Johto puis Kanto jusqu'aux 251 Pokémon, avec un choix de version pour les trois jeux et une vue par lieu.",
     "de": "Eine Route durch Johtos acht Arenen und weiter durch Kanto zu allen 251, mit Editionsauswahl für alle drei Spiele und Ortsansicht.",
     "ko": "성도의 8개 체육관을 거쳐 관동까지 돌며 251종을 채우는 루트. 세 작품의 버전 선택과 장소별 보기 포함.",
     "zh-Hant": "走過城都8座道館再到關都、填滿全部251隻的路線，並包含三款遊戲的版本切換與地點檢視。", "zh-Hans": "走过城都8座道馆再到关都、填满全部251只的路线，并包含三款游戏的版本切换与地点查看。"},
   "readme_row": "| Pokémon Gold, Silver & Crystal | [Open](https://mostafarlotfi.github.io/pokedex-tracker/gsc/) | Pokédex route (all 251, gym by gym and on through Kanto, with a version picker for all three games and an area view) · Legendaries |",
   "readme_goal": "For Gold, Silver & Crystal it's the legendaries, with the ones that need Red, Blue or Yellow marked.",
   "readme_src": "Gold, Silver & Crystal and Red, Blue & Yellow wild encounters and evolutions come from [PokeAPI](https://pokeapi.co/)."},
 'rby': {"gkey": "gRb", "label": {"en": "Red, Blue & Yellow", "ja": "赤・青・ピカチュウ", "fr": "Rouge, Bleu et Jaune", "de": "Rot, Blau & Gelb", "ko": "레드·블루·피카츄", "zh-Hant": "紅／藍／皮卡丘", "zh-Hans": "红／蓝／皮卡丘"},
   "cardkey": "rb", "prefix": "PRBY1-",
   "name": {"en": "Pokémon Red, Blue & Yellow", "ja": "ポケットモンスター 赤・青・ピカチュウ", "fr": "Pokémon Rouge, Bleu et Jaune", "de": "Pokémon Rot, Blau und Gelb", "ko": "포켓몬스터 레드·블루·피카츄", "zh-Hant": "寶可夢 紅／藍／皮卡丘", "zh-Hans": "宝可梦 红／蓝／皮卡丘"},
   "desc": {"en": "A route through Kanto's eight Gyms to all 151, with a version picker for all three games and an area view.",
     "ja": "カントーの8つのジムをめぐり、151匹を埋めるルート。3作品のバージョン切り替えと場所別表示にも対応。",
     "fr": "Un itinéraire à travers les huit Arènes de Kanto jusqu'aux 151 Pokémon, avec un choix de version pour les trois jeux et une vue par lieu.",
     "de": "Eine Route durch Kantos acht Arenen zu allen 151, mit Editionsauswahl für alle drei Spiele und Ortsansicht.",
     "ko": "관동의 8개 체육관을 돌며 151종을 채우는 루트. 세 작품의 버전 선택과 장소별 보기 포함.",
     "zh-Hant": "走過關都8座道館、填滿全部151隻的路線，並包含三款遊戲的版本切換與地點檢視。", "zh-Hans": "走过关都8座道馆、填满全部151只的路线，并包含三款游戏的版本切换与地点查看。"},
   "readme_row": "| Pokémon Red, Blue & Yellow | [Open](https://mostafarlotfi.github.io/pokedex-tracker/rby/) | Pokédex route (all 151, gym by gym, with a version picker for all three games and an area view) · Legendaries |",
   "readme_goal": "For Red, Blue & Yellow it's the legendary birds, Mewtwo and Mew.",
   "readme_src": ""}}
for slug, S in SITE.items(): json.dump(S, open(slug + '_site.json', 'w'), ensure_ascii=False)
print('ok')
