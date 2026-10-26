import csv, json, re, collections, unicodedata
SP = json.load(open('la_sp.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
slugs = [l.strip().split('/')[2] for l in open('la_urls.txt')]
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower().replace('♀', 'f').replace('♂', 'm')))
EN2N = {norm(v): k for k, v in EN.items()}
dexno = {int(r[0]): int(r[2]) for r in rows('pokemon_dex_numbers.csv') if r[1] == '30'}
slug2n = {s: EN2N[norm(s)] for s in slugs}
assert set(slug2n.values()) == set(dexno), 'dex mismatch'

AREAS = ['Jubilife Village', 'Obsidian Fieldlands', 'Crimson Mirelands', 'Cobalt Coastlands', 'Coronet Highlands', 'Alabaster Icelands']
AREA_STOP = {'Jubilife Village': 0, 'Obsidian Fieldlands': 1, 'Crimson Mirelands': 2, 'Cobalt Coastlands': 3, 'Coronet Highlands': 4, 'Alabaster Icelands': 5}
STOP_LV = [5, 18, 30, 40, 48, 58, 65, 70]
STOPS = ['start', 'Obsidian Fieldlands', 'Crimson Mirelands', 'Cobalt Coastlands', 'Coronet Highlands', 'Alabaster Icelands', 'redchain', 'post']

def parse(parts):
    """-> list of tokens: ['area', area, [sublocs]] / ['dist', area] / ['mmo', area]"""
    toks = []
    for p in parts:
        m = re.match(r'(Jubilife Village|Obsidian Fieldlands|Crimson Mirelands|Cobalt Coastlands|Coronet Highlands|Alabaster Icelands)\s*:?\s*(.*)$', p)
        if not m: continue
        area, rest = m.group(1), m.group(2).strip()
        if rest.startswith('Massive Mass Outbreak'): toks.append(['mmo', area]); continue
        if rest.startswith('Space-time Distortion'): toks.append(['dist', area]); continue
        subs = [re.sub(r'\s*or nearby$', '', x).strip() for x in rest.split(' , ') if x.strip()]
        subs = [x for x in subs if x and not x.startswith('Space-time')]
        toks.append(['area', area, subs])
        if 'Space-time Distortion' in rest: toks.append(['dist', area])
    return toks

SPECIAL = {'rowlet': 'starter', 'cyndaquil': 'starter', 'oshawott': 'starter',
 'dialga': 'dialgaPalkia', 'palkia': 'dialgaPalkia', 'uxie': 'lakes', 'mesprit': 'lakes', 'azelf': 'lakes',
 'heatran': 'heatran', 'regigigas': 'regigigas', 'cresselia': 'cresselia', 'giratina': 'giratina',
 'tornadus': 'forces', 'thundurus': 'forces', 'landorus': 'forces', 'enamorus': 'enamorus',
 'manaphy': 'manaphy', 'phione': 'manaphy', 'darkrai': 'darkrai', 'shaymin': 'shaymin', 'arceus': 'arceus',
 'spiritomb': 'spiritomb', 'unown': 'unown'}
SPECIAL_STOP = {'starter': 0, 'dialgaPalkia': 6, 'unown': 2, 'spiritomb': 6}

entries = []
for s in slugs:
    n = slug2n[s]; toks = parse(SP[s]['la'])
    e = {'n': n, 'slug': s, 'id': '%03d' % dexno[n]}
    wild = [t for t in toks if t[0] in ('area', 'dist')]
    stop = min((AREA_STOP[t[1]] for t in wild), default=None)
    if s in SPECIAL:
        k = SPECIAL[s]; e['tok'] = [['x', k]] + (wild if k in ('starter', 'unown', 'spiritomb') else [])
        stop = SPECIAL_STOP.get(k, 7)
    else:
        e['tok'] = wild or [t for t in toks if t[0] == 'mmo'][:2]
        if stop is None and not any(True for _ in []): stop = None
    e['mmo'] = sorted({t[1] for t in toks if t[0] == 'mmo'}, key=AREAS.index)
    e['stop'] = stop
    e['g'] = sorted({t[1] for t in toks if t[0] == 'area'} | {'dist|' + t[1] for t in toks if t[0] == 'dist'})
    entries.append(e)
by_n = {e['n']: e for e in entries}

def method(e):
    ic = [i for i in SP[e['slug']]['evo'].get(e['slug'], []) if not i.startswith('mega')]
    return ic[0] if ic else None
def lvl(m):
    x = re.match(r'l(?:day|night)?(\d+)', m or ''); return int(x.group(1)) if x else None
changed = True
while changed:
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and by_n[p]['stop'] is not None and e['slug'] not in SPECIAL:
            m = method(e); L = lvl(m); ps = by_n[p]['stop']
            cand = max(ps, next((i for i, x in enumerate(STOP_LV) if x >= L), 7)) if L else ps
            if not any(t[0] == 'evo' for t in e['tok']):
                e['tok'] = [t for t in e['tok'] if t[0] != 'mmo'] + [['evo', p, m]]
            if e['stop'] is None or cand < e['stop']: e['stop'] = cand; changed = True
for e in entries:  # only reachable through Massive Mass Outbreaks (post-game)
    if e['stop'] is None: e['stop'] = 7
miss = [e['slug'] for e in entries if not e['tok']]
print('no tokens', miss)
kids = collections.defaultdict(list)
for e in entries:
    p = parent.get(e['n'])
    if p in by_n: kids[p].append(e['n'])
for e in entries:
    chain = []; cur = e['n']
    while kids.get(cur):
        ks = sorted(kids[cur], key=lambda n: by_n[n]['id'])
        chain.append([[c, method(by_n[c])] for c in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain
def key(e):
    t0 = e['tok'][0][0]
    pri = {'x': 0, 'area': 1, 'dist': 2, 'mmo': 3, 'evo': 4}.get(t0, 5)
    return (e['stop'], pri, e['id'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries))

W = json.load(open('wisps.json')); U = json.load(open('unown.json'))
wisps = sorted([{'id': 'W%d%02d' % (AREAS.index(a), no), 'area': a, 'no': no, 'loc': loc} for a, no, loc in W], key=lambda w: w['id'])
unown = [{'id': 'U' + f, 'form': f, 'loc': loc} for f, loc in U]
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '9'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name
areas = {d['9']: {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d} for d in LN.values() if '9' in d}
# the five main areas aren't in PokeAPI: official Japanese/Korean/Chinese names; French/German left in English (not verified)
areas.update({'Obsidian Fieldlands': {'ja': '黒曜の原野', 'ko': '흑요 들판', 'zh-Hant': '黑曜原野', 'zh-Hans': '黑曜原野'},
 'Crimson Mirelands': {'ja': '紅蓮の湿地', 'ko': '홍련 습지', 'zh-Hant': '紅蓮濕地', 'zh-Hans': '红莲湿地'},
 'Cobalt Coastlands': {'ja': '群青の海岸', 'ko': '군청 해안', 'zh-Hant': '群青海岸', 'zh-Hans': '群青海岸'},
 'Coronet Highlands': {'ja': '天冠の山麓', 'ko': '천관 산기슭', 'zh-Hant': '天冠山麓', 'zh-Hans': '天冠山麓'},
 'Alabaster Icelands': {'ja': '純白の凍土', 'ko': '순백 동토', 'zh-Hant': '純白凍土', 'zh-Hans': '纯白冻土'}})
areas.setdefault('Jubilife Village', {}).update({'ja': 'コトブキムラ', 'ko': '축복마을', 'zh-Hant': '祝慶村', 'zh-Hans': '祝庆村'})
# Serebii spellings that differ from PokeAPI's
key = lambda x: re.sub(r'[^a-z]', '', re.sub(r'^the ', '', x.lower())).rstrip('s')
bykey = {key(k): k for k in list(areas)}
def fixname(x):
    base = re.sub(r'\s*\((?:Story|Male Only|Female Only)\)', '', x).strip()
    return bykey.get(key(base), base)
for e in entries:
    for t in e['tok']:
        if t[0] == 'area': t[2] = list(dict.fromkeys(fixname(x) for x in t[2]))
for w in wisps: w['loc'] = fixname(w['loc'])
for u in unown: u['loc'] = fixname(u['loc'])
used = {x for e in entries for t in e['tok'] if t[0] == 'area' for x in t[2]} | {w['loc'] for w in wisps} | {u['loc'] for u in unown} | set(AREAS)
print('place names without translations:', sorted(x for x in used if x not in areas)[:30])
out = {'entries': [{k: e[k] for k in ('id', 'n', 'stop', 'tok', 'g', 'evo')} | ({'mmo': e['mmo']} if e['mmo'] else {}) for e in entries],
       'stops': STOPS, 'wisps': wisps, 'unown': unown, 'areas': areas}
json.dump(out, open('la_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))), 'wisps', len(wisps), 'unown', len(unown))
