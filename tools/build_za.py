import csv, json, re, collections
S = json.load(open('sp.json')); SL = json.load(open('slugs.json'))
MS = json.load(open('megastones.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]

# ---- species ids, names, evolution parents ----
dexnum = collections.defaultdict(dict)
for sid, did, no in rows('pokemon_dex_numbers.csv'):
    if did in ('34', '35'): dexnum[did][int(no)] = int(sid)
spec = {int(r[0]): r for r in rows('pokemon_species.csv')}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
LANGS = {'en': '9', 'ja': '11', 'fr': '5', 'de': '6', 'ko': '3', 'zh-Hant': '4', 'zh-Hans': '12'}
names = collections.defaultdict(dict)
for sid, lang, name, *_ in rows('pokemon_species_names.csv'):
    names[int(sid)][lang] = name

entries = []  # (id, species, slug, dlc)
for key, did in (('L', '34'), ('H', '35')):
    for (no, url) in SL[key]:
        sid = dexnum[did][int(no)]
        entries.append({'id': key + no, 'n': sid, 'slug': url.split('/')[2], 'dlc': key == 'H'})
assert len(entries) == 364
by_n = {e['n']: e for e in entries}
EN = {e['n']: names[e['n']]['9'] for e in entries}
slug2n = {e['slug']: e['n'] for e in entries}

# ---- zones -> unlock stop ----
ZONE_STOP = {1: 1, **{z: 2 for z in range(2, 7)}, **{z: 3 for z in range(7, 11)}, **{z: 4 for z in range(11, 14)},
             14: 5, 15: 5, 16: 6, 17: 6, 18: 7, 19: 7, 20: 9}
STOP_LV = [5, 10, 15, 25, 35, 42, 48, 55, 55, 60, 65, 100, 120, 140, 170, 200, 200]
DIST = ['Vert', 'Bleu', 'Magenta', 'Rouge', 'Jaune']
STAR_STOP = {1: 11, 2: 12, 3: 13, 4: 14, 5: 15}

def parse_base(za):
    tok = []; groups = []; stop = None; other = None
    if not za or za.startswith('Evolve') or za == 'Revive Fossil': return tok, groups, stop, other
    zones = sorted({int(z) for z in re.findall(r'Wild Zone (\d+)', za)})
    dists = sorted({d for d in DIST if re.search(d + r' (District|Sector)', za)}, key=DIST.index)
    if zones:
        tok.append(['wz', zones]); groups += ['wz%d' % z for z in zones]
        stop = min(ZONE_STOP[z] for z in zones)
    if dists:
        tok.append(['streets', 1 if len(dists) == 5 else dists]); groups.append('streets')
        other = 1
    for k, pat in (('sewers', 'The Sewers'), ('labs', 'Lysandre Labs'), ('oldhouse', 'Old House')):
        if pat in za:
            tok.append([k]); groups.append(k); other = 8 if other is None else min(other, 8)
    return tok, groups, stop, other

def parse_hs(md):
    if not md: return [], [], None
    pairs = sorted({(t, int(s)) for t, s in re.findall(r'(\w+) \((\d) Star\)', md)}, key=lambda p: (p[1], p[0]))
    if not pairs: return [], [], None
    bytype = collections.OrderedDict()
    for t, s in sorted(pairs, key=lambda p: (min(q[1] for q in pairs if q[0] == p[0]), p[0], p[1])):
        bytype.setdefault(t, []).append(s)
    return [['hs', [[t, ss] for t, ss in bytype.items()]]], ['hs-' + t for t in bytype], STAR_STOP[min(s for _, s in pairs)]

# ---- evolution methods (Serebii icon names), Eevee special-cased ----
EEVEE = {'vaporeon': 'waterstone', 'jolteon': 'thunderstone', 'flareon': 'firestone', 'espeon': 'happinessday',
         'umbreon': 'happinessnight', 'leafeon': 'leafstone', 'glaceon': 'icestone', 'sylveon': 'monamie'}
def method(e):
    if e['slug'] in EEVEE: return EEVEE[e['slug']]
    icons = [i for i in S[e['slug']]['evo'].get(e['slug'], []) if not i.startswith('mega') and 'nite' not in i]
    return icons[0] if icons else None

# ---- special sources (gifts, trades, legendaries) ----
SPECIAL = {  # slug: (tokens, stop, groups)
 'chikorita': ([['x', 'starter']], 0), 'tepig': ([['x', 'starter']], 0), 'totodile': ([['x', 'starter']], 0),
 'chespin': ([['sm', 7]], 2), 'fennekin': ([['sm', 8]], 2), 'froakie': ([['sm', 9]], 2),
 'bulbasaur': ([['sm', 22]], 3), 'charmander': ([['sm', 22]], 3), 'squirtle': ([['sm', 22]], 3),
 'aerodactyl': ([['x', 'fossil']], 4), 'tyrunt': ([['x', 'fossil']], 4), 'amaura': ([['x', 'fossil']], 4),
 'heracross': ([['trade', 25, 2]], 1),
 'xerneas': ([['x', 'xerneas']], 10), 'yveltal': ([['x', 'yveltal']], 10), 'zygarde': ([['x', 'zygarde']], 10),
 'diancie': ([['x', 'diancie']], 10), 'mewtwo': ([['x', 'mewtwo']], 10),
 'heatran': ([['x', 'heatran']], 16), 'darkrai': ([['x', 'darkrai']], 16), 'kyogre': ([['x', 'kyogre']], 16),
 'groudon': ([['x', 'groudon']], 16), 'rayquaza': ([['x', 'rayquaza']], 16), 'meltan': ([['x', 'meltan']], 16),
 'melmetal': ([['x', 'melmetal']], 16), 'magearna': ([['x', 'magearna']], 16), 'hoopa': ([['x', 'hoopa']], 16),
 'volcanion': ([['x', 'volcanion']], 16), 'genesect': ([['x', 'genesect']], 16), 'marshadow': ([['x', 'marshadow']], 16),
 'zeraora': ([['x', 'zeraora']], 16),
 **{s: ([['x', 'scan']], 16) for s in ('latias', 'latios', 'cobalion', 'terrakion', 'virizion', 'keldeo', 'meloetta')},
 'gimmighoul': ([['x', 'gimmighoul']], 11), 'feebas': ([['streets', ['Vert']]], 11),
}
KEEP_BASE = {'heracross', 'gimmighoul', 'feebas', 'chikorita', 'tepig', 'totodile', 'chespin', 'fennekin', 'froakie',
             'bulbasaur', 'charmander', 'squirtle'}  # special adds to (not replaces) normal sources

for e in entries:
    v = S[e['slug']]
    tok, groups, stop, other = ([], [], None, None) if e['dlc'] else parse_base(v['za'])
    e['other'] = other
    htok, hgroups, hstop = parse_hs(v['md'])
    if e['dlc']:
        tok, groups, stop = htok, hgroups, hstop
    else:
        e['hs'] = htok  # base-game species that also appear in Hyperspace (shown as extra info)
    if e['slug'] in SPECIAL:
        st, sp = SPECIAL[e['slug']][0], SPECIAL[e['slug']][1]
        if e['slug'] in KEEP_BASE:
            tok = st + tok
            stop = sp; e['other'] = None
        else:
            tok, stop = st, sp; e['other'] = None
        groups = groups + ['gift'] if e['slug'] not in ('feebas',) else groups + ['streets']
    e['tok'], e['g'], e['stop'] = tok, groups, stop

def lvl0(m):
    x = re.match(r'l(?:day|night)?(\d+)', m or ''); return int(x.group(1)) if x else None
for e in entries:
    if e.get('other') is not None:
        L = lvl0(method(e)) if parent.get(e['n']) in by_n else None
        o = e['other']
        if L: o = max(o, next((i for i, x in enumerate(STOP_LV[:11]) if x >= L), 10))
        e['stop'] = o if e['stop'] is None else min(e['stop'], o)

# evolutions: from parent within dex
def lvl(m):
    x = re.match(r'l(?:day|night)?(\d+)', m or ''); return int(x.group(1)) if x else None
order = sorted(entries, key=lambda e: (e['dlc'], spec[e['n']][18] and int(spec[e['n']][18])))
changed = True
while changed:
    changed = False
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n and by_n[p]['stop'] is not None:
            m = method(e); L = lvl(m)
            ps = by_n[p]['stop']
            if L and not e['dlc']:
                ls = next((i for i, x in enumerate(STOP_LV[:11]) if x >= L), 10)
                cand = max(ps, ls)
            else:
                cand = ps
            if e['dlc'] and not by_n[p]['dlc']: cand = max(cand, 11)
            had_evo = any(t[0] == 'evo' for t in e['tok'])
            if not had_evo and e['slug'] not in SPECIAL:
                e['tok'] = e['tok'] + [['evo', p, m]]
                if not e['g']: e['g'] = ['evo']
            if e['slug'] not in SPECIAL and (e['stop'] is None or cand < e['stop']):
                e['stop'] = cand; changed = True
missing = [e['id'] + ' ' + e['slug'] for e in entries if e['stop'] is None or not e['tok']]
print('missing', missing)

# evolves-into chains (within this game's dex)
kids = collections.defaultdict(list)
for e in entries:
    p = parent.get(e['n'])
    if p in by_n: kids[p].append(e['n'])
for e in entries:
    chain = []; cur = e['n']
    while kids.get(cur):
        ks = sorted(kids[cur], key=lambda n: by_n[n]['id'])
        chain.append([[k, method(by_n[k])] for k in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain

# ---- sort within stops: gifts/special, wild (by first zone), evolutions ----
def key(e):
    t0 = e['tok'][0][0] if e['tok'] else 'z'
    pri = {'x': 0, 'sm': 0, 'trade': 1, 'wz': 2, 'streets': 2, 'hs': 2, 'sewers': 3, 'labs': 3, 'oldhouse': 3, 'evo': 4}.get(t0, 5)
    zone = e['tok'][0][1][0] if t0 == 'wz' else 0
    return (e['stop'], pri, zone, e['id'])
entries.sort(key=key)

STOPS = [
 'Main Missions 1–2: arrival in Lumiose City', 'Main Mission 3: Wild Zone 1 and the city streets',
 'Main Mission 5: Wild Zones 2–6', 'Main Mission 10: Wild Zones 7–10', 'Main Mission 15: Wild Zones 11–13',
 'Main Mission 20: Wild Zones 14–15', 'Main Mission 25: Wild Zones 16–17', 'Main Mission 30: Wild Zones 18–19',
 'The Sewers, Lysandre Labs and the Old House', 'Post-game: Wild Zone 20 (Main Mission 39)', 'Post-game: Legendary Pokémon',
 'Mega Dimension: Hyperspace ★1', 'Mega Dimension: Hyperspace ★2', 'Mega Dimension: Hyperspace ★3',
 'Mega Dimension: Hyperspace ★4', 'Mega Dimension: Hyperspace ★5', 'Mega Dimension: story and special encounters']
used = sorted({e['stop'] for e in entries}); print('stops used', used)
print(collections.Counter(e['stop'] for e in entries))

# ---- Mega Stones ----
items = {r[1]: r[0] for r in rows('items.csv')}
stones = []
for name, holder, loc, slug in MS:
    hname = 'Floette' if 'Floette' in holder else holder
    hn = next((n for n, nm in EN.items() if nm == hname), None)
    ident = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    dlc = loc.startswith(('Hyperspace', 'Side Mission 1')) or (hn in by_n and by_n[hn]['dlc'])
    stones.append({'id': ident, 'item': int(items[ident]), 'name': name, 'n': hn, 'loc': loc, 'dlc': dlc})
print('stones', len(stones), 'no holder', [s['name'] for s in stones if not s['n']])

out = {'entries': [{k: e[k] for k in ('id', 'n', 'stop', 'tok', 'g', 'evo', 'dlc')} | ({'hs': e['hs']} if e.get('hs') else {}) for e in entries],
       'stops': STOPS, 'stones': stones}
json.dump(out, open('za_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))))
