import csv, json, re, collections, unicodedata
SP = json.load(open('swsh_sp.json')); LV = json.load(open('swsh_lv.json'))
AREALV = {int(k): v for k, v in LV['area'].items()}
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
slugs = [l.strip().split('/')[2] for l in open('swsh_urls.txt')]
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower().replace('♀', 'f').replace('♂', 'm')))
EN2N = {norm(v): k for k, v in EN.items()}
dexno = collections.defaultdict(dict)
for sid, did, no in rows('pokemon_dex_numbers.csv'):
    if did in ('27', '28', '29'): dexno[int(sid)][{'27': 'G', '28': 'I', '29': 'C'}[did]] = int(no)
slug2n = {s: EN2N[norm(s)] for s in slugs}
assert len(set(slug2n.values())) == len(slugs) == len(dexno), (len(slugs), len(dexno))

STOPS = ['start', 'turffield', 'hulbury', 'motostoke', 'stow', 'ballonlea', 'circhester', 'spikemuth', 'hammerlocke', 'champion', 'post', 'ioa', 'ct', 'special']
CAPS = [20, 25, 30, 35, 40, 45, 50, 55, 100]          # Wild Area catch level cap by badges
GATE = {}
def gate(stop, *names):
    for n in names: GATE[n] = stop
gate(1, 'Route 3', 'Galar Mine', 'Route 4', 'Turffield')
gate(2, 'Route 5', 'Hulbury', 'Galar Mine No. 2')
gate(3, 'Motostoke Outskirts', 'Hammerlocke')
gate(4, 'Route 6', 'Stow-on-Side')
gate(5, 'Glimwood Tangle', 'Ballonlea')
gate(6, 'Route 7', 'Route 8', 'Route 9', 'Circhester')
gate(7, 'Spikemuth')
gate(9, 'Route 10', 'Wyndon')
gate(10, 'Energy Plant', 'Battle Tower')
def stop_for(L): return next((i for i, c in enumerate(CAPS) if c >= L), 8)
SPECIAL = {'grookey': ('starter', 0), 'scorbunny': ('starter', 0), 'sobble': ('starter', 0),
 'zacian': ('legend', 10), 'zamazenta': ('legend', 10), 'eternatus': ('eternatus', 10), 'type:null': ('typenull', 10), 'bulbasaur': ('dojo', 11), 'squirtle': ('dojo', 11), 'slowpoke': ('slowpoke', 11),
 'kubfu': ('kubfu', 11), 'urshifu': ('urshifu', 11), 'calyrex': ('calyrex', 12), 'glastrier': ('steed', 12), 'spectrier': ('steed', 12),
 'regieleki': ('regi', 12), 'regidrago': ('regi', 12), 'articuno': ('birds', 12), 'zapdos': ('birds', 12), 'moltres': ('birds', 12),
 'dracozolt': ('fossil', 4), 'arctozolt': ('fossil', 4), 'dracovish': ('fossil', 4), 'arctovish': ('fossil', 4),
 'zarude': ('event', 13), 'zeraora': ('event', 13), 'marshadow': ('event', 13), 'meltan': ('event', 13), 'melmetal': ('event', 13),
 'magearna': ('event', 13), 'keldeo': ('dynamax', 12), 'cobalion': ('swords', 12), 'terrakion': ('swords', 12), 'virizion': ('swords', 12)}
LEG_DA = {'mewtwo', 'raikou', 'entei', 'suicune', 'lugia', 'ho-oh', 'latias', 'latios', 'kyogre', 'groudon', 'rayquaza', 'uxie', 'mesprit', 'azelf',
          'dialga', 'palkia', 'heatran', 'giratina', 'cresselia', 'tornadus', 'thundurus', 'landorus', 'reshiram', 'zekrom', 'kyurem', 'xerneas',
          'yveltal', 'zygarde', 'tapukoko', 'tapulele', 'tapubulu', 'tapufini', 'solgaleo', 'lunala', 'necrozma', 'nihilego', 'buzzwole',
          'pheromosa', 'xurkitree', 'celesteela', 'kartana', 'guzzlord', 'stakataka', 'blacephalon', 'poipole', 'naganadel', 'cosmog', 'cosmoem',
          'kyurem'}
def areas_of(txt):
    main = txt.split(' || ')[0]
    out = []
    for a in re.split(r' , |, ', main):
        a = re.sub(r'\s*\((Galarian|East Sea|West Sea|[A-Za-z]+ Form)\)', '', a).strip(' ,')
        if a and not re.match(r'(Evolve|Trade|Transfer|Event|Gift|Revive|Max Raid|Gigantamax|Dynamax|Breed|The (Isle|Crown)|Wild Area)', a) and a not in out: out.append(a)
    return out
def raids_of(txt):
    m = re.search(r'Max Raid Battles?:\s*(.*)', txt)
    if not m: return []
    return list(dict.fromkeys(a.strip(' ,') for a in re.split(r' , |, ', m.group(1).split(' || ')[0]) if a.strip(' ,') and '||' not in a))

entries = []
for s in slugs:
    n = slug2n[s]; v = SP[s]; e = {'n': n, 'slug': s, 'dex': dexno[n]}
    ex = None
    for sec in ('base', 'ioa', 'ct'):
        if not ex and v[sec].get('Shield', '').startswith(('Trade from Sword', 'Trade from Pokémon Sword')): ex = 'W'
        if not ex and v[sec].get('Sword', '').startswith(('Trade from Shield', 'Trade from Pokémon Shield')): ex = 'H'
    e['ex'] = ex
    pick = lambda sec: (v[sec].get('Sword') if v[sec].get('Sword') and not v[sec]['Sword'].startswith('Trade') else v[sec].get('Shield', '')) or ''
    tok = []; stop = None
    b = pick('base')
    if b and not b.startswith('Transfer'):
        ars = areas_of(b); rd = raids_of(b)
        lv = AREALV.get(n, {})
        cands = []
        lv = {a: L for a, L in lv.items() if L >= 5}  # Lv 1 is a parsing artifact on a few area pages
        for a in ars:
            L = lv.get(a)
            if not L and a not in GATE: continue  # unknown level in the Wild Area: don't guess it's early
            cands.append(max(stop_for(L) if L else 0, GATE.get(a, 0)))
        if ars and not cands: cands.append(8)
        ars.sort(key=lambda a: lv.get(a, 999))
        if ars: tok.append(['area', ars])
        if rd:
            tok.append(['raid', rd[:6]])
            if not cands: cands.append(8)  # raid-only: every den star level is open after the eighth badge
        if cands: stop = min(cands)
    in_base = stop is not None or bool(b and not b.startswith('Transfer'))
    for sec, st in (('ioa', 11), ('ct', 12)):
        t = pick(sec)
        if not t or t.startswith('Transfer'): continue
        ars = areas_of(t); rd = raids_of(t)
        if 'Dynamax Adventures' in t: tok.append(['da']); stop = 12 if stop is None else stop
        if ars: tok.append([sec, ars])
        elif rd: tok.append([sec + 'raid', rd[:6]])
        if (ars or rd) and stop is None: stop = st
    if s in SPECIAL:
        k, st = SPECIAL[s]; tok = [['x', k]] + (tok if k in ('starter', 'fossil', 'slowpoke') else []); stop = st
    elif s in LEG_DA:
        tok = [['da']]; stop = 12
    e['tok'] = tok; e['stop'] = stop; e['dlc'] = not in_base and stop is not None and stop >= 11 or ('G' not in dexno[n] and stop is not None and stop >= 11)
    entries.append(e)
by_n = {e['n']: e for e in entries}
FIXM = {'hitmonlee': 'tyrogue20aed', 'hitmonchan': 'tyrogue20aed', 'hitmontop': 'tyrogue20aed', 'vaporeon': 'waterstone', 'jolteon': 'thunderstone',
        'flareon': 'firestone', 'espeon': 'happinessday', 'umbreon': 'happinessnight', 'leafeon': 'leafstone', 'glaceon': 'icestone', 'sylveon': 'fairyfriend',
        'malamar': 'l30upside', "sirfetch'd": 'crits', 'runerigus': 'ldamage', 'milotic': 'tradeprismscale', 'lycanroc': 'rockruff', 'urshifu': 'towers'}
def method(e):
    if e['slug'] in FIXM: return FIXM[e['slug']]
    ic = [i for i in SP[e['slug']]['evo'].get(e['slug'], []) if not i.startswith(('mega', 'gmax'))]
    return ic[0] if ic else None
def lvl(m):
    x = re.match(r'l(?:day|night)?(\d+)', m or ''); return int(x.group(1)) if x else None
changed = True
while changed:
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and by_n[p]['stop'] is not None and e['slug'] not in SPECIAL and e['slug'] not in LEG_DA:
            m = method(e); L = lvl(m); ps = by_n[p]['stop']
            cand = max(ps, stop_for(L)) if (L and ps <= 9) else ps
            if not any(t[0] == 'evo' for t in e['tok']): e['tok'] = e['tok'] + [['evo', p, m]]
            if e['stop'] is None or cand < e['stop']: e['stop'] = cand; changed = True
for e in entries:
    if e['stop'] is None: e['stop'] = 13; e['tok'] = e['tok'] or [['x', 'event']]
    e['dlc'] = e['stop'] in (11, 12) or (e['stop'] == 13 and 'G' not in e['dex'])
print('no tokens', [e['slug'] for e in entries if not e['tok']])
kids = collections.defaultdict(list)
for e in entries:
    p = parent.get(e['n'])
    if p in by_n: kids[p].append(e['n'])
def disp(e):
    d = e['dex']; return ('G', d['G']) if 'G' in d else (('I', d['I']) if 'I' in d else ('C', d['C']))
for e in entries:
    k, no = disp(e); e['id'] = '%s%03d' % (k, no)
for e in entries:
    chain = []; cur = e['n']
    while kids.get(cur):
        ks = sorted(kids[cur], key=lambda c: by_n[c]['id'])
        chain.append([[c, method(by_n[c])] for c in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain
    e['g'] = sorted({a for t in e['tok'] if t[0] in ('area', 'ioa', 'ct') for a in t[1]})
def key(e):
    t0 = e['tok'][0][0]
    pri = {'x': 0, 'area': 1, 'ioa': 1, 'ct': 1, 'raid': 2, 'ioaraid': 2, 'ctraid': 2, 'da': 2, 'evo': 3}.get(t0, 4)
    return (e['stop'], pri, min([L for L in AREALV.get(e['n'], {}).values() if L >= 5] or [99]), e['id'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries)); print('exclusives', collections.Counter(e['ex'] for e in entries))
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '8'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name
areas = {d['9']: {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d} for d in LN.values() if '9' in d}
used = {a for e in entries for t in e['tok'] if t[0] in ('area', 'ioa', 'ct', 'raid', 'ioaraid', 'ctraid') for a in t[1]}
print('untranslated', sorted(a for a in used if a not in areas)[:40])
# CJK names for the Gym towns (PokeAPI only has en/fr/de for Galar); left out where unsure, so they fall back to English
CJK = {'Turffield': ('ターフタウン', '터프마을'), 'Hulbury': ('バウタウン', '바우마을', '水舟鎮', '水舟镇'), 'Motostoke': ('エンジンシティ', '엔진시티', '機擎市', '机擎市'),
       'Stow-on-Side': ('ラテラルタウン', '라테랄마을'), 'Ballonlea': ('アラベスクタウン', '아라베스크마을'), 'Circhester': ('キルクスタウン', '키르크스마을'),
       'Spikemuth': ('スパイクタウン', '스파이크마을', '尖釘鎮', '尖钉镇'), 'Hammerlocke': ('ナックルシティ', '너클시티', '拳關市', '拳关市'), 'Wyndon': ('シュートシティ', '슛시티', '宮門市', '宫门市')}
for k, v in CJK.items():
    areas.setdefault(k, {}).update(dict(zip(('ja', 'ko', 'zh-Hant', 'zh-Hans'), v)))
DIG = json.load(open('diglett.json')); GM = json.load(open('gmax.json'))
GM.append([892, 'Urshifu', 'Max Soup, after receiving Urshifu (Isle of Armor)'])
digs = [{'id': 'D%03d' % (i + 1), 'area': a, 'no': no} for i, (a, no, _) in enumerate(DIG)]
GMX = {25: ['lgpe'], 133: ['lgpe'], 52: ['event'], 143: ['event'], 849: ['event'], 809: ['home'], 812: ['soup'], 815: ['soup'], 818: ['soup'], 892: ['soup'],
       3: ['ioaden', 'Forest of Focus', 'Training Lowlands'], 9: ['ioaden', 'Workout Sea', 'Stepping-Stone Sea']}
GVER = {68: 'W', 94: 'H', 131: 'H', 839: 'W', 841: 'W', 842: 'H'}
gmax = []
for n, _, loc in GM:
    k = GMX.get(n) or ['den'] + [a for a in loc.split(' / ') if a not in ('Sword', 'Shield')]
    assert all(a in areas for a in k[1:]), (n, k)
    gmax.append({'id': 'X%03d' % n, 'n': n, 'how': k, 'ex': GVER.get(n)})
out = {'entries': [{k: e[k] for k in ('id', 'n', 'stop', 'tok', 'g', 'evo', 'ex', 'dlc', 'dex')} for e in entries], 'stops': STOPS, 'digs': digs, 'gmax': gmax, 'digRewards': [[5, 52, 'A'], [10, 79, 'G'], [20, 37, 'A'], [30, 27, 'A'], [40, 26, 'A'], [50, 105, 'A'], [75, 103, 'A'], [100, 0, ''], [150, 50, 'A']], 'areas': areas}
json.dump(out, open('swsh_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))), 'digs', len(digs), 'gmax', len(gmax))
