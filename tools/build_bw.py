import csv, json, re, collections
SP = {int(k): v for k, v in json.load(open('bw_sp.json')).items()}
AR = json.load(open('bw_area.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
ids = [int(l) for l in open('bw_ids.txt')]
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
dexno = {int(sid): int(no) for sid, did, no in rows('pokemon_dex_numbers.csv') if did == '8'}
SLUGNAME = {u.split('/')[-1][:-6]: n.strip() for u, n in (l.rstrip('\n').split('|') for l in open('b2_areas.txt'))}
SLUGNAME = {k: v.replace('Pokemon', 'Pokémon') for k, v in SLUGNAME.items() if k != 'index'}
NAME2SLUG = {v: k for k, v in SLUGNAME.items()}
N2EN = {v.lower(): k for k, v in EN.items()}

STOPS = ['start', 'striaton', 'lenora', 'burgh', 'elesa', 'clay', 'skyla', 'brycen', 'drayden', 'post', 'special']
LOC = {}
def put(stop, *slugs):
    for s in slugs: LOC[s] = stop
put(0, 'nuvematown', 'route1', 'accumulatown', 'route2', 'striatoncity', 'dreamyard')
put(1, 'route3', 'wellspringcave', 'nacrenecity')
put(2, 'pinwheelforest', 'skyarrowbridge', 'casteliacity')
put(3, 'route4', 'desertresort', 'reliccastle', 'nimbasacity', 'route16', 'lostlornforest')
put(4, 'route5', 'driftveildrawbridge', 'driftveilcity', 'coldstorage')
put(5, 'route6', 'chargestonecave', 'mistraltoncity', 'celestialtower', 'route7')
put(6, 'twistmountain', 'icirruscity', 'route8', 'mooroficirrus', 'dragonspiraltower', 'mistraltoncave')
put(7, 'opelucidcity', 'route9')
put(8, 'route10', 'victoryroad', 'pokemonleague', "n'scastle")
put(9, 'route11', 'route12', 'route13', 'route14', 'route15', 'route17', 'route18', 'villagebridge', 'undellatown', 'undellabay', 'lacunosatown',
    'abundantshrine', 'blackcity', 'whiteforest', 'giantchasm', 'marvelousbridge', 'p2laboratory', "challenger'scave", 'abyssalruins',
    'libertygarden', 'tubelinebridge', 'anvilletown', 'gearstation', 'entralink')
# method gates: Rock Smash (Pinwheel Forest), Surf (Twist Mountain, from Alder), Super Rod and Dive (post-game)
def gate(meth):
    m = meth.lower()
    if 'fish' in m or 'rod' in m or 'dive' in m or 'underwater' in m: return 9
    if 'surf' in m: return 6
    return 0
wild = collections.defaultdict(list)
for slug, tabs in AR.items():
    if slug not in LOC: continue
    for meth, cond, ver, lv, *mons in tabs:
        st = max(LOC[slug], gate(meth))
        for m in mons:
            n = N2EN.get(m.lower().replace('’', "'"))
            if n and ver and 'roaming' not in meth.lower(): wild[n].append((st, meth, lv, slug, ver))
SPECIAL = {495: 'starter', 498: 'starter', 501: 'starter', 564: 'fossil', 566: 'fossil', 638: 'swords', 639: 'swords', 640: 'swords', 643: 'tao', 644: 'tao', 646: 'kyurem',
           641: 'forces', 642: 'forces', 645: 'landorus', 494: 'victini', 647: 'event', 648: 'event', 649: 'event', 570: 'event', 571: 'event'}
SPSTOP = {'starter': 0, 'fossil': 3, 'swords': 9, 'tao': 8, 'kyurem': 9, 'forces': 9, 'landorus': 9, 'victini': 10, 'event': 10}
def text_areas(txt):
    out = []
    for part in re.split(r' , |, | \|\| ', txt or ''):
        part = part.strip()
        nm = max((k for k in NAME2SLUG if part.startswith(k)), key=len, default=None)
        if nm and NAME2SLUG[nm] in LOC and NAME2SLUG[nm] not in out: out.append(NAME2SLUG[nm])
    return out
entries = []
for n in ids:
    s = SP[n]; e = {'n': n, 'dex': dexno[n]}
    tr = lambda x: bool(re.match(r'(Trade|Migrate)', x or ''))
    r, sa = s.get('B', ''), s.get('W', '')
    inR = any(x[4] == 'Black' for x in wild[n]); inS = any(x[4] == 'White' for x in wild[n])
    ex = None
    if (inR and not inS) or (tr(sa) and not tr(r)): ex = 'B'
    if (inS and not inR) or (tr(r) and not tr(sa)): ex = 'W'
    if SPECIAL.get(n) in ('starter', 'fossil', 'event', 'victini'): ex = None  # same in both versions; the page text just differs
    ex = {643: 'B', 644: 'W', 641: 'W', 642: 'B'}.get(n, ex)  # Reshiram in Black, Zekrom in White; Tornadus roams White, Thundurus Black
    e['ex'] = ex
    tok = []; stop = None
    w = sorted(wild[n])
    if w:
        stop = w[0][0]
        seen = []
        for st, meth, lv, slug, ver in w:
            if slug not in seen: seen.append(slug)
        tok.append(['area', seen]); e['lv'] = min(x[2] for x in w if x[0] == stop)
    extra = [a for a in text_areas(r) + text_areas(sa) if not w or a not in [x[3] for x in w]]
    if extra:
        extra = list(dict.fromkeys(extra))
        if tok: tok[0][1] += extra
        else: tok.append(['area', extra])
        st = min(LOC[a] for a in extra)
        if stop is None or st < stop: stop = st
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
changed = True
while changed:
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and by_n[p]['stop'] is not None and e['n'] not in SPECIAL:
            if not any(t[0] == 'evo' for t in e['tok']): e['tok'] = e['tok'] + [['evo', p, METH.get(e['n'])]]
            if e['stop'] is None or by_n[p]['stop'] < e['stop']: e['stop'] = by_n[p]['stop']; changed = True
    for e in entries:  # breed-only first stages: hatch from an evolved form you can already catch
        if e['stop'] is None and e['n'] not in SPECIAL:
            ks = [k for k, p in parent.items() if p == e['n'] and k in by_n and by_n[k]['stop'] is not None]
            if ks:
                k = min(ks, key=lambda k: by_n[k]['stop']); e['stop'] = by_n[k]['stop']; e['tok'] = [['breed', k]] + e['tok']; changed = True
DESERT = set()
for e in entries:
    if e['n'] in DESERT and e['stop'] is not None and e['stop'] < 4: e['stop'] = 4
changed = True
while changed:  # re-flow evolutions after the desert fix
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and e['n'] not in SPECIAL and by_n[p]['stop'] is not None and e['stop'] is not None and e['stop'] < by_n[p]['stop'] and not any(t[0] == 'area' for t in e['tok']):
            e['stop'] = by_n[p]['stop']; changed = True
for e in entries:
    if e['stop'] is None: e['stop'] = 10; e['tok'] = e['tok'] or [['x', 'event']]
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
    e['g'] = sorted({a for t in e['tok'] if t[0] == 'area' for a in t[1]})
    e['id'] = '%03d' % e['dex']  # Unova Pokédex number (Victini is #000)
def key(e):
    pri = {'x': 0, 'area': 1, 'evo': 3, 'breed': 3}.get(e['tok'][0][0], 4)
    return (e['stop'], pri, e.get('lv', 99), e['dex'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries)); print('exclusives', collections.Counter(e['ex'] for e in entries))
# legendaries outside the Hoenn Pokédex (Hoenn ones are checked off in the Pokédex): [n, version, place slug or key, requirement key]
LEG = []  # every Black/White legendary is in the Unova Pokédex
legs = [{'id': 'L%02d' % (i + 1), 'n': n, 'ex': v or None, 'area': a, 'req': q} for i, (n, v, a, q) in enumerate(LEG)]
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '5'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name.replace('’', "'")
byEN = {}
for d in LN.values():
    if '9' in d: byEN.setdefault(d['9'], {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d})
used = {a for e in entries for a in e['g']} | {
    'nuvematown', 'striatoncity', 'nacrenecity', 'casteliacity', 'nimbasacity', 'driftveilcity', 'mistraltoncity', 'icirruscity', 'opelucidcity', 'route3'}
names = {}
for slug in sorted(used):
    en = SLUGNAME.get(slug, slug)
    alt = {'Victory Road (B2W2)': 'Victory Road', 'PWT': 'Pokémon World Tournament'}.get(en, en)
    names[slug] = dict(en=en, **byEN.get(alt, {}))
print('untranslated', [names[s]['en'] for s in names if len(names[s]) == 1])
out = {'entries': [{k: e[k] for k in ('id', 'n', 'dex', 'stop', 'tok', 'g', 'evo', 'ex')} for e in entries], 'stops': STOPS, 'legs': legs, 'areas': names}
json.dump(out, open('bw_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False)), 'legs', len(legs))
