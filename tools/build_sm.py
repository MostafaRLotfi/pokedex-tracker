import csv, json, re, collections
SP = {int(k): v for k, v in json.load(open('sm_sp.json')).items()}
AR = json.load(open('sm_area.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
ids = [int(l) for l in open('sm_ids.txt')]
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
dexno = {int(sid): int(no) for sid, did, no in rows('pokemon_dex_numbers.csv') if did == '16'}
SLUGNAME = {u.split('/')[-1][:-6]: n.strip() for u, n in (l.rstrip('\n').split('|') for l in open('usum_areas.txt'))}
N2EN = {v.lower(): k for k, v in EN.items()}

STOPS = ['start', 'ilima', 'hala', 'lana', 'kiawe', 'mallow', 'olivia', 'sophocles', 'nanu', 'hapu', 'post', 'special']
LOC = {}
def put(stop, *slugs):
    for s in slugs: LOC[s] = stop
put(0, 'ikitown', 'route1', "hau'olicity", 'route2', "hau'olicemetery", 'berryfields', 'verdantcavern', 'mahalotrail')
put(1, 'route3', 'melemelemeadow', 'seawardcave', "kala'ebay", 'tencarathill', 'melemelesea', 'ruinsofconflict', 'dividingpeaktunnel')
put(2, 'heaheacity', 'heaheabeach', 'route4', 'paniolatown', 'paniolaranch', 'route5', 'brooklethill', 'pikachuvalley')
put(3, 'route6', 'royalavenue', 'route7', 'welavolcanopark', 'bigwavebeach', 'sandycave')
put(4, 'route8', 'lushjungle')
put(5, "diglett'stunnel", 'route9', 'konikonicity', 'memorialhill', 'akalaoutskirts', 'hanobeach', 'hanograndresort', 'ruinsoflife')
put(6, 'maliecity', 'maliegarden', 'route10', 'mounthokulani', 'hokulaniobservatory')
put(7, 'route11', 'route12', 'secludedshore', 'blushmountain', 'route13', 'hainadesert', 'tapuvillage', 'route14', 'thriftymegamart', 'route15',
    'route16', "ula'ulameadow", 'route17', 'potown', 'shadyhouse', 'aetherhouse', "ula'ulabeach", 'ruinsofabundance')
put(8, 'aetherparadise', 'seafolkvillage', 'poniwilds', 'ancientponipath', 'ponibreakercoast', 'exeggutorisland', 'vastponicanyon',
    'altarofthesunne', 'altarofthemoone', 'lakeofthesunne', 'lakeofthemoone')
put(9, 'mountlanakila', 'pokemonleague', 'megalotower', 'ultramegalopolis')
put(10, 'poniplains', 'ponimeadow', 'ponicoast', 'ponigauntlet', 'ponigrove', 'resolutioncave', 'battletree', 'ruinsofhope', 'plainsgrotto',
    "teamrocket'scastle", 'ultraspacewilds', 'ultraspace', 'ultracrater', 'ultradeepsea', 'ultradesert', 'ultraforest', 'ultrajungle', 'ultraplant', 'ultraruin')
WATER = re.compile(r'Surf|Fish|Bubbl', re.I)   # needs Lapras Paddle and a rod, both after Lana's trial
# lowest-stop wild method per species from area tables: (stop, method, level, slug, versions)
wild = collections.defaultdict(list)
for slug, tabs in AR.items():
    if slug not in LOC: continue
    for meth, cond, ver, lv, *mons in tabs:
        st = max(LOC[slug], 3 if WATER.search(meth) else 0)
        for m in mons:
            n = N2EN.get(m.lower().replace('’', "'"))
            if n: wild[n].append((st, meth, lv, slug, ver))
SPECIAL = {722: 'starter', 725: 'starter', 728: 'starter', 789: 'cosmog', 790: 'cosmoem', 791: 'solgaleo', 792: 'lunala', 800: 'necrozma',
           785: 'tapu', 786: 'tapu', 787: 'tapu', 788: 'tapu', 772: 'typenull', 773: 'silvally', 718: 'zygarde', 801: 'magearna', 802: 'marshadow',
           807: 'zeraora', 803: 'poipole', 804: 'naganadel', 793: 'ub', 794: 'ub', 795: 'ub', 796: 'ub', 797: 'ub', 798: 'ub', 799: 'ub', 805: 'ub', 806: 'ub',
           566: 'fossil', 567: 'fossil', 564: 'fossil', 565: 'fossil', 696: 'fossil', 697: 'fossil', 698: 'fossil', 699: 'fossil', 345: 'fossil', 347: 'fossil',
           142: 'fossil', 410: 'fossil', 408: 'fossil', 138: 'fossil', 140: 'fossil', 137: 'porygon'}
SPSTOP = {'starter': 0, 'cosmog': 10, 'cosmoem': 10, 'solgaleo': 8, 'lunala': 8, 'necrozma': 10, 'tapu': 10, 'typenull': 10, 'silvally': 10,
          'zygarde': 7, 'magearna': 11, 'marshadow': 11, 'zeraora': 11, 'poipole': 10, 'naganadel': 10, 'ub': 10, 'fossil': 3, 'porygon': 7}
def area_list(n, vers=('Sun', 'Moon')):
    w = sorted(x for x in wild[n] if x[4] in vers)
    seen = []
    for st, meth, lv, slug, ver in w:
        if slug not in seen: seen.append(slug)
    return seen
entries = []
for n in ids:
    s = SP[n]; e = {'n': n, 'dex': dexno[n]}
    us, um = s.get('S', {}).get('text', ''), s.get('M', {}).get('text', '')
    inUS = any(x[4] == 'Sun' for x in wild[n]) or bool(s.get('S', {}).get('areas'))
    inUM = any(x[4] == 'Moon' for x in wild[n]) or bool(s.get('M', {}).get('areas'))
    ex = None
    if inUS and not inUM and re.match(r'(Trade|Migrate)', um): ex = 'S'
    if inUM and not inUS and re.match(r'(Trade|Migrate)', us): ex = 'M'
    tr = lambda x: bool(re.match(r'(Trade|Migrate)', x))
    if not ex and tr(um) and not tr(us): ex = 'S'
    if not ex and tr(us) and not tr(um): ex = 'M'
    e['ex'] = ex
    tok = []; stop = None
    w = sorted(wild[n])
    if w:
        stop = w[0][0]
        tok.append(['area', area_list(n)])
        e['lv'] = min(x[2] for x in w if x[0] == stop)
    # areas named on the species page but missing from the tables (SOS-only, Island Scan etc.)
    extra = []
    for ver in ('S', 'M'):
        for slug, name, note in s.get(ver, {}).get('areas', []):
            if slug in LOC and (not w or slug not in [x[3] for x in w]):
                st = LOC[slug] + (0 if 'SOS' in note or 'Scan' in note else 0)
                note = note.strip('()')
                key = 'sos' if 'SOS' in note else ('scan' if 'Scan' in note else 'area')
                if [key, slug] not in extra: extra.append([key, slug])
                if stop is None or st < stop: stop = st
    for key in ('area', 'sos', 'scan'):
        sl = [x[1] for x in extra if x[0] == key]
        if not sl: continue
        if key == 'area' and tok and tok[0][0] == 'area': tok[0][1] += [x for x in sl if x not in tok[0][1]]
        else: tok.append([key, sl])
    if n in SPECIAL:
        k = SPECIAL[n]; tok = [['x', k]] + (tok if k != 'starter' else []); stop = SPSTOP[k]
    e['tok'] = tok; e['stop'] = stop
    entries.append(e)
by_n = {e['n']: e for e in entries}
METH = {}
for n, s in SP.items():
    for icon, title, child, img in s['evo']:
        if child not in METH and not icon.endswith('not'): METH[child] = icon
METH.update({134: 'waterstone', 135: 'thunderstone', 136: 'firestone', 196: 'happinessday', 197: 'happinessnight', 470: 'mossrock', 471: 'icerock', 700: 'fairyfriend'})
GATE = {'levelcoronet': 7, 'snow': 9, 'mossrock': 4, 'icerock': 9}  # evolution spots: Blush Mountain, Mount Lanakila, Lush Jungle
def lvl(m):
    x = re.match(r'l(\d+)', m or ''); return int(x.group(1)) if x else None
changed = True
while changed:
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and by_n[p]['stop'] is not None and e['n'] not in SPECIAL:
            if not any(t[0] == 'evo' for t in e['tok']): e['tok'] = e['tok'] + [['evo', p, METH.get(e['n'])]]
            cand = max(by_n[p]['stop'], GATE.get(METH.get(e['n']), 0))
            if e['stop'] is None or cand < e['stop']: e['stop'] = cand; changed = True
    for e in entries:  # breed-only first stages (Breed X / Poké Pelago): hatch from an evolved form you can already catch
        if e['stop'] is None and e['n'] not in SPECIAL:
            ks = [k for k, p in parent.items() if p == e['n'] and k in by_n and by_n[k]['stop'] is not None]
            if ks:
                k = min(ks, key=lambda k: by_n[k]['stop']); e['stop'] = by_n[k]['stop']; e['tok'] = [['breed', k]] + e['tok']; changed = True
for e in entries:
    if e['stop'] is None: e['stop'] = 11; e['tok'] = e['tok'] or [['x', 'event']]
print('no tokens', [EN[e['n']] for e in entries if not e['tok']])
kids = collections.defaultdict(list)
for e in entries:
    p = parent.get(e['n'])
    if p in by_n: kids[p].append(e['n'])
for e in entries:
    chain = []; cur = e['n']
    while kids.get(cur):
        ks = sorted(kids[cur], key=lambda c: by_n[c]['dex'])
        chain.append([[c, METH.get(c)] for c in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain
    e['g'] = sorted({a for t in e['tok'] if t[0] in ('area', 'sos', 'scan') for a in t[1]})
    e['id'] = '%03d' % e['dex']
def key(e):
    pri = {'x': 0, 'area': 1, 'sos': 2, 'scan': 2, 'evo': 3, 'breed': 3}.get(e['tok'][0][0], 4)
    return (e['stop'], pri, e.get('lv', 99), e['dex'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries)); print('exclusives', collections.Counter(e['ex'] for e in entries))
# place names: PokeAPI Alola locations in all 7 languages, keyed by Serebii area slug
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '7'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name.replace('’', "'")
byEN = {}
for d in LN.values():
    if '9' in d: byEN.setdefault(d['9'], {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d})
used = sorted({a for e in entries for a in e['g']} | {'ikitown', 'verdantcavern', 'brooklethill', 'welavolcanopark', 'lushjungle', 'hokulaniobservatory',
                'blushmountain', 'vastponicanyon', 'mountlanakila', 'pokemonleague', 'heaheacity'})  # used in titles and texts
names = {}
for slug in used:
    en = SLUGNAME.get(slug, slug).replace('Pokemon', 'Pokémon')
    alt = {'Berry Fields': 'Alola Berry Fields'}.get(en, en)
    names[slug] = dict(en=en, **byEN.get(alt, {}))
ULTRA = {'Ultra Crater': ('ウルトラクレーター', '울트라크레이터'), 'Ultra Deep Sea': ('ウルトラディープシー', '울트라딥시'), 'Ultra Desert': ('ウルトラデザート', '울트라데저트'),
         'Ultra Forest': ('ウルトラフォレスト', '울트라포레스트'), 'Ultra Jungle': ('ウルトラジャングル', '울트라정글'), 'Ultra Plant': ('ウルトラプラント', '울트라플랜트'), 'Ultra Ruin': ('ウルトラルイン', '울트라루인')}
for v in names.values():  # Ultra Space worlds: not in PokeAPI; ja/ko only, other languages fall back to English
    if v['en'] in ULTRA: v['ja'], v['ko'] = ULTRA[v['en']]
print('untranslated', [names[s]['en'] for s in used if len(names[s]) == 1])
ZC = json.load(open('sm_cells.json'))
known = sorted({v['en'] for v in names.values()} | set(SLUGNAME.values()), key=len, reverse=True)
EN2SLUG = {v: k for k, v in SLUGNAME.items()}
cells = []
for i, (kind, isl, loc, sub, note) in enumerate(ZC):
    slug = EN2SLUG.get(loc, loc)
    if slug not in names: names[slug] = dict(en=SLUGNAME.get(slug, loc), **byEN.get({'Berry Fields': 'Alola Berry Fields'}.get(loc, loc), {}))
    cells.append({'id': 'Z%03d' % (i + 1), 'kind': kind, 'island': isl, 'area': slug, 'sub': sub, 'note': note})
assert len(cells) == 100 and all(c['area'] in SLUGNAME for c in cells), [c['area'] for c in cells if c['area'] not in SLUGNAME]
out = {'entries': [{k: e[k] for k in ('id', 'n', 'dex', 'stop', 'tok', 'g', 'evo', 'ex')} for e in entries], 'stops': STOPS, 'cells': cells, 'areas': names}
json.dump(out, open('sm_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False)), 'cells', len(cells))
