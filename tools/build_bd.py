import csv, json, re, collections, unicodedata
SP = json.load(open('bd_sp.json')); GU = {int(k): v for k, v in json.load(open('gu_ms.json')).items()}
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
slugs = [l.strip().split('/')[2] for l in open('bd_urls.txt')]
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
sinnoh = {int(r[0]): int(r[2]) for r in rows('pokemon_dex_numbers.csv') if r[1] == '5'}  # original Sinnoh dex (151)
assert len(sinnoh) == 151
slug2n = {s: i + 1 for i, s in enumerate(slugs)}

STOPS = ['start', 'oreburgh', 'eterna', 'veilstone', 'pastoria', 'hearthome', 'canalave', 'snowpoint', 'sunyshore', 'league', 'national', 'ramanas', 'events']
LOC = {}
def put(stop, *names):
    for n in names: LOC[n] = stop
put(0, 'Twinleaf Town', 'Sandgem Town', 'Route 201', 'Route 202', 'Lake Verity', 'Lake Verity (Gift - From Briefcase)', 'Verity Lakefront', 'Jubilife City')
put(1, 'Route 203', 'Oreburgh Gate', 'Oreburgh Mine', 'Oreburgh City', 'Route 204')
put(2, 'Floaroma Town', 'Floaroma Meadow', 'Route 205', 'Valley Windworks', 'Eterna Forest', 'Fuego Ironworks', 'Eterna City', 'Old Chateau')
put(3, 'Route 206', 'Wayward Cave', 'Route 207', 'Mt. Coronet', 'Route 208', 'Hearthome City', 'Amity Square', 'Route 209', 'Lost Tower',
    'Solaceon Town', 'Solaceon Ruins', 'Route 210', 'Route 215', 'Veilstone City', 'Ravaged Path')
put(4, 'Route 214', 'Valor Lakefront', "Ruins Maniac's Cave", "Ruins Maniac's Tunnel", 'Route 213', 'Pastoria City', 'Great Marsh')
put(5, 'Celestic Town', 'Route 211', 'Route 212', 'Trophy Garden', 'Pokémon Mansion')
put(6, 'Route 218', 'Canalave City', 'Iron Island', 'Iron Island (Gift - From Riley)', 'Route 219', 'Route 220', 'Route 221', 'Lake Valor', 'Fullmoon Island')
put(7, 'Route 216', 'Route 217', 'Acuity Lakefront', 'Snowpoint City', 'Lake Acuity')
put(8, 'Route 222', 'Sunyshore City', 'Spear Pillar', 'Galactic HQ')
put(9, 'Route 223', 'Victory Road', 'Pokemon League', 'Pokémon League')
put(10, 'Route 224', 'Route 225', 'Route 226', 'Route 227', 'Route 228', 'Route 229', 'Route 230', 'Stark Mountain', 'Sendoff Spring', 'Turnback Cave',
    'Snowpoint Temple', 'Resort Area', 'Survival Area', 'Fight Area', 'Sinnoh', 'Hearthome City (Gift - Have National Dex)')
put(11, 'Ramanas Park')
put(12, 'Newmoon Island', 'Flower Paradise', 'Hall of Origin', 'Event Only', 'Transfer from Pokémon HOME', 'Breed from Manaphy')
GU_STOP = [2, 4, 6, 7, 8, 10, 10]
RAMANAS = [('Discovery Room', '', [377, 378, 379]), ('Johto Room', 'B', [243, 244, 245]), ('Kanto Room', 'S', [144, 145, 146]),
           ('Soul Room', '', [380, 381]), ('Rainbow Room', 'B', [250]), ('Squall Room', 'S', [249]), ('Oceanic Room', '', [382]),
           ('Tectonic Room', '', [383]), ('Stratospheric Room', '', [384]), ('Genome Room', '', [150])]
ROOM = {n: r for r, _, ms in RAMANAS for n in ms}
SPECIAL = {387: 'starter', 388: None, 390: 'starter', 393: 'starter', 447: 'riolu', 133: 'eevee', 151: 'mew', 385: 'jirachi',
           483: 'dialga', 484: 'palkia', 480: 'uxie', 481: 'mesprit', 482: 'azelf', 487: 'giratina', 485: 'heatran', 486: 'regigigas',
           488: 'cresselia', 491: 'event', 492: 'event', 493: 'event', 489: 'phione', 490: 'manaphy'}
SPECIAL_STOP = {'starter': 0, 'riolu': 6, 'eevee': 10, 'mew': 10, 'jirachi': 10, 'dialga': 8, 'palkia': 8, 'uxie': 8, 'mesprit': 8, 'azelf': 8,
                'giratina': 10, 'heatran': 10, 'regigigas': 10, 'cresselia': 10, 'event': 12, 'phione': 12, 'manaphy': 12}
FOSSIL = {408: 'skull', 409: None, 410: 'armor', 411: None, 138: 'helix', 140: 'dome', 142: 'amber', 345: 'root', 347: 'claw'}

unknown = collections.Counter(); entries = []
for s in slugs:
    n = slug2n[s]; v = SP[s]; e = {'n': n, 'id': '%03d' % n, 'sid': sinnoh.get(n)}
    ex = 'B' if v['S'].lower().startswith('trade from pokémon brilliant diamond') else ('S' if v['B'].lower().startswith('trade from pokémon shining pearl') else None)
    e['ex'] = ex
    txt = v['B'] if not v['B'].lower().startswith('trade') else v['S']
    parts = [p.strip() for p in re.split(r' , |, ', txt) if p.strip()]
    places = [p for p in parts if not p.startswith(('Evolve', 'Breed ', 'Trade', 'trade')) and 'Revive' not in p and 'Savefile' not in p]
    tok = []; cands = []
    gu = 'Grand Underground' in places
    places = [p for p in places if p != 'Grand Underground']
    for p in places:
        if p in LOC: cands.append(LOC[p])
        else: unknown[p] += 1
    if places: tok.append(['area', places])
    EN2N = {re.sub(r'[^a-z]', '', x.lower()): i + 1 for i, x in enumerate(slugs)}
    for p in parts:
        mb = re.match(r'Breed (.+)$', p)
        if mb:
            ns = [EN2N.get(re.sub(r'[^a-z]', '', x.lower())) for x in mb.group(1).split('/')]
            if ns and ns[0]: tok.append(['breed', ns[0]]); cands.append(10)
    if gu:
        ms = GU.get(n, 5); tok.append(['gu', ms]); cands.append(GU_STOP[ms])
    stop = min(cands) if cands else None
    if n in FOSSIL and FOSSIL[n]:
        f = FOSSIL[n]; tok = [['x', 'fossil_' + f]] + tok
        stop = 2 if f in ('skull', 'armor') else 10
    if n in ROOM:
        tok = [['room', ROOM[n]]]; stop = 11
    if n in SPECIAL and SPECIAL[n]:
        k = SPECIAL[n]; tok = [['x', k]] + (tok if k in ('eevee',) else []); stop = SPECIAL_STOP[k]
    e['tok'] = tok; e['stop'] = stop
    entries.append(e)
print('unmapped places', unknown.most_common(40))
by_n = {e['n']: e for e in entries}

def method(e):
    slug = slugs[e['n'] - 1]
    ic = [i for i in SP[slug]['evo'].get(slug, []) if not i.startswith('mega') and not i.startswith('gmax')]
    return ic[0] if ic else None
def lvl(m):
    x = re.match(r'l(?:day|night)?(\d+)', m or ''); return int(x.group(1)) if x else None
STOP_LV = [7, 14, 22, 30, 33, 36, 39, 42, 49, 55, 60, 70, 70]
changed = True
while changed:
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and by_n[p]['stop'] is not None and not (e['n'] in SPECIAL and SPECIAL[e['n']]) and e['n'] not in ROOM:
            m = method(e); L = lvl(m); ps = by_n[p]['stop']
            cand = max(ps, next((i for i, x in enumerate(STOP_LV) if x >= L), 10)) if L and ps < 10 else ps
            if not e['sid'] and cand < 10: cand = 10  # non-Sinnoh evolutions need the National Dex's pre-evolution anyway
            if not any(t[0] == 'evo' for t in e['tok']): e['tok'] = e['tok'] + [['evo', p, m]]
            if e['stop'] is None or cand < e['stop']: e['stop'] = cand; changed = True
for e in entries:
    if e['stop'] is None: e['stop'] = 10
    if not e['sid'] and e['stop'] < 10 and not any(t[0] == 'x' for t in e['tok']): e['stop'] = 10  # non-Sinnoh dex species can't be found before the National Dex
print('no tokens', [e['id'] for e in entries if not e['tok']])
kids = collections.defaultdict(list)
for e in entries:
    p = parent.get(e['n'])
    if p in by_n: kids[p].append(e['n'])
for e in entries:
    chain = []; cur = e['n']
    while kids.get(cur):
        ks = sorted(kids[cur])
        chain.append([[c, method(by_n[c])] for c in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain
    e['g'] = sorted(set(next((t[1] for t in e['tok'] if t[0] == 'area'), [])) | ({'Grand Underground'} if any(t[0] == 'gu' for t in e['tok']) else set()))
def key(e):
    t0 = e['tok'][0][0] if e['tok'] else 'z'
    pri = {'x': 0, 'room': 0, 'area': 1, 'gu': 2, 'evo': 3}.get(t0, 4)
    return (e['stop'], pri, e['sid'] or 999, e['n'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries))
print('exclusives', collections.Counter(e['ex'] for e in entries))
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '4'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name
areas = {d['9']: {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d} for d in LN.values() if '9' in d}
used = {p for e in entries for t in e['tok'] if t[0] == 'area' for p in t[1]}
print('untranslated places', sorted(p for p in used if p not in areas)[:40])
out = {'entries': [{k: e[k] for k in ('id', 'n', 'sid', 'stop', 'tok', 'g', 'evo', 'ex')} for e in entries], 'stops': STOPS,
       'rooms': [{'room': r, 'ver': v, 'mons': ms} for r, v, ms in RAMANAS], 'areas': areas}
json.dump(out, open('bd_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))))
# CJK names for the main towns/places (PokeAPI only has en/fr/de for Sinnoh)
CITY={'Twinleaf Town':('フタバタウン','떡잎마을','雙葉鎮','双叶镇'),'Sandgem Town':('マサゴタウン','잔모래마을','真砂鎮','真砂镇'),
 'Jubilife City':('コトブキシティ','축복시티','祝慶市','祝庆市'),'Oreburgh City':('クロガネシティ','무쇠시티','黑金市','黑金市'),
 'Floaroma Town':('ソノオタウン','꽃향기마을','花苑鎮','花苑镇'),'Eterna City':('ハクタイシティ','영원시티','百代市','百代市'),
 'Hearthome City':('ヨスガシティ','연고시티','家緣市','家缘市'),'Veilstone City':('トバリシティ','장막시티','帷幕市','帷幕市'),
 'Pastoria City':('ノモセシティ','습원시티','濕原市','湿原市'),'Celestic Town':('カンナギタウン','신수마을','神和鎮','神和镇'),
 'Canalave City':('ミオシティ','운하시티','水脈市','水脉市'),'Snowpoint City':('キッサキシティ','선단시티','切博市','切博市'),
 'Sunyshore City':('ナギサシティ','물가시티','濱海市','滨海市'),'Mt. Coronet':('テンガンざん','천관산','天冠山','天冠山'),
 'Great Marsh':('だいしつげん','대습원','大濕地','大湿地'),'Grand Underground':('地下大洞窟','지하대동굴','地下大洞窟','地下大洞窟')}
for k,(ja,ko,zt,zs) in CITY.items(): out['areas'].setdefault(k,{}).update({'ja':ja,'ko':ko,'zh-Hant':zt,'zh-Hans':zs})
out['areas']['Grand Underground'].update({'fr':'Grands Souterrains','de':'Untergrund'})
json.dump(out, open('bd_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
