import csv, json
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
L = {'9': 'en', '1': 'ja', '5': 'fr', '6': 'de', '3': 'ko', '4': 'zh-Hant', '12': 'zh-Hans'}
d = json.load(open('b2_data.json'))
ns = {e['n'] for e in d['entries']} | {l['n'] for l in d['legs']}
NAMES = {l: {} for l in L.values()}
for sid, lang, name, *_ in rows('pokemon_species_names.csv'):
    if lang in L and int(sid) in ns: NAMES[L[lang]][sid] = name
ITEMS_W = ['dusk-stone', 'fire-stone', 'ice-stone', 'leaf-stone', 'moon-stone', 'shiny-stone', 'sun-stone', 'thunder-stone', 'water-stone', 'dawn-stone',
           'kings-rock', 'metal-coat', 'upgrade', 'dubious-disc', 'oval-stone', 'razor-claw', 'electirizer', 'magmarizer', 'protector', 'reaper-cloth',
           'dragon-scale', 'prism-scale', 'deep-sea-tooth', 'deep-sea-scale', 'razor-fang']
iid = {r[1]: r[0] for r in rows('items.csv')}; iid['upgrade'] = iid['up-grade']
miss = [i for i in ITEMS_W if i not in iid]; print('missing items', miss)
ITEMS = {l: {} for l in L.values()}
for i, lang, name in rows('item_names.csv'):
    for k in ITEMS_W:
        if iid.get(k) == i and lang in L: ITEMS[L[lang]][k] = name
MOVES_W = {'ancientpower': 'ancient-power', 'doublehit': 'double-hit', 'mimic': 'mimic', 'rollout': 'rollout', 'stomp': 'stomp', 'taunt': 'taunt'}
mid = {r[1]: r[0] for r in rows('moves.csv')}
MOVES = {l: {} for l in L.values()}
for i, lang, name in rows('move_names.csv'):
    for k, v in MOVES_W.items():
        if mid[v] == i and lang in L: MOVES[L[lang]][k] = name
tid = {r[0]: r[1].capitalize() for r in rows('types.csv')}
TYPES = {l: {} for l in L.values()}
for i, lang, name in rows('type_names.csv'):
    if lang in L and int(i) <= 18: TYPES[L[lang]][tid[i]] = name
for l in L.values(): print(l, len(NAMES[l]), len(ITEMS[l]), len(MOVES[l]), len(TYPES[l]))
json.dump({'NAMES': NAMES, 'ITEMS': ITEMS, 'MOVES': MOVES, 'TYPES': TYPES}, open('b2_names.json', 'w'), ensure_ascii=False, separators=(',', ':'))
