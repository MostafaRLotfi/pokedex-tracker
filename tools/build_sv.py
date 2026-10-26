import csv, json, re, collections
SP = json.load(open('sv_sp.json')); PS = json.load(open('ps.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
slugs = [l.strip().split('/')[2] for l in open('sv_urls.txt')]
spec = {r[1]: r for r in rows('pokemon_species.csv')}
byid = {int(r[0]): r for r in rows('pokemon_species.csv')}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
EN = {}
for sid, lang, name, *_ in rows('pokemon_species_names.csv'):
    if lang == '9': EN[int(sid)] = name
import unicodedata
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower().replace('♀', 'f').replace('♂', 'm')))
EN2N = {norm(v): k for k, v in EN.items()}
dexno = collections.defaultdict(dict)
for sid, did, no in rows('pokemon_dex_numbers.csv'):
    if did in ('31', '32', '33'): dexno[int(sid)][{'31': 'P', '32': 'K', '33': 'B'}[did]] = int(no)
slug2n = {}
for s in slugs:
    n = EN2N.get(norm(s)) or EN2N.get(norm(s.replace('-', ' ')))
    assert n, s
    slug2n[s] = n
assert len(set(slug2n.values())) == 664

# ---- stops (recommended order by level) ----
STOPS = [("Poco Path to Mesagoza", 8), ("Cortondo Gym (Bug)", 15), ("Stony Cliff Titan (Klawf)", 16), ("Artazon Gym (Grass)", 17),
 ("Open Sky Titan (Bombirdier)", 20), ("Segin Squad (Dark)", 21), ("Levincia Gym (Electric)", 24), ("Schedar Squad (Fire)", 27),
 ("Lurking Steel Titan (Orthworm)", 29), ("Cascarrafa Gym (Water)", 30), ("Navi Squad (Poison)", 33), ("Medali Gym (Normal)", 36),
 ("Montenevera Gym (Ghost)", 42), ("Quaking Earth Titan (Great Tusk / Iron Treads)", 45), ("Alfornada Gym (Psychic)", 45),
 ("Glaseado Gym (Ice)", 48), ("Ruchbah Squad (Fairy)", 51), ("Caph Squad (Fighting)", 56), ("False Dragon Titan (Tatsugiri)", 57),
 ("Pokémon League", 62), ("Area Zero: The Way Home and the post-game", 99),
 ("The Teal Mask: Kitakami", 100), ("The Indigo Disk: Blueberry Academy", 100), ("DLC Legendary Pokémon and the epilogue", 100)]
LV = [l for _, l in STOPS]
def stop_for(level): return next(i for i, l in enumerate(LV[:21]) if l >= level) if level <= 99 else 20
RAID_STOP = {1: 0, 2: 1, 3: 6, 4: 11, 5: 19, 6: 20}
FIXED_AREA_STOP = {'Poco Path': 0, 'Cabo Poco': 0, 'Inlet Grotto': 0, 'Mesagoza': 0, 'Los Platos': 0, 'Cortondo': 1,
                   'Alfornada Cavern': 14, 'Dalizapa Passage': 12, 'Socarrat Trail': 18, 'Area Zero': 20}

# min wild level per species & area from pokestop.io
minlv = collections.defaultdict(lambda: 999); area_lv = collections.defaultdict(dict)
PSNAME = lambda f: ' '.join(w.capitalize() for w in f.split('-')).replace('The ', '').replace('Pokemon League', 'Pokemon League')
for area, rs in PS.items():
    if area == 'the-great-crater-of-paldea': continue  # Area Zero opens at the finale
    an = re.sub(r'^The ', '', ' '.join(w.capitalize() for w in area.split('-')))
    an = {'Great Crater Of Paldea': 'Great Crater of Paldea', 'Pokemon League': 'Pokemon League'}.get(an, an)
    for name, vers, method, lo, hi in rs:
        n = EN2N.get(norm(name))
        if not n: continue
        minlv[n] = min(minlv[n], lo)
        area_lv[n][an] = min(area_lv[n].get(an, 999), lo)

# official area names (PokeAPI, region 10) – used to pull clean area names out of Serebii's text
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '10'}
LOCN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LOCN[lid][lang] = name
KNOWN = {re.sub(r'[()]', '', d['9']): lid for lid, d in LOCN.items()}
KNOWN['Great Crater of Paldea'] = 'area-zero'; KNOWN['Pokemon League'] = [k for k, v in LOCS.items() if v == 'pokemon-league'][0]
KRE = re.compile('|'.join(re.escape(k) for k in sorted(KNOWN, key=len, reverse=True)))
def canon(a): return re.sub(r'[()]', '', LOCN[KNOWN[a]]['9']) if KNOWN[a] in LOCN else a
def areas_of(txt):
    txt = re.sub(r'Tera Raid Battles:.*', '', txt)
    out = []
    for m in KRE.finditer(txt):
        a = canon(m.group(0))
        if a not in out: out.append(a)
    return out
def raids_of(txt):
    m = re.search(r'Tera Raid Battles:(.*)', txt)
    return sorted({int(x) for x in re.findall(r'(\d) Star', m.group(1))}) if m else []

SPECIAL = {  # slug: (tokens, stop)
 'sprigatito': [['x', 'starter']], 'fuecoco': [['x', 'starter']], 'quaxly': [['x', 'starter']],
 'koraidon': [['x', 'legendPartner']], 'miraidon': [['x', 'legendPartner']],
 'ting-lu': [['x', 'ruinG']], 'chien-pao': [['x', 'ruinY']], 'wo-chien': [['x', 'ruinP']], 'chi-yu': [['x', 'ruinB']],
 'gimmighoul': [['x', 'gimmighoul']],
 'ogerpon': [['x', 'ogerpon']], 'okidogi': [['x', 'loyal']], 'munkidori': [['x', 'loyal']], 'fezandipiti': [['x', 'loyal']],
 'terapagos': [['x', 'terapagos']], 'pecharunt': [['x', 'pecharunt']], 'meloetta': [['x', 'meloetta']],
 'walkingwake': [['x', 'paradoxEvent']], 'ironleaves': [['x', 'paradoxEvent']],
}
SPECIAL_STOP = {'sprigatito': 0, 'fuecoco': 0, 'quaxly': 0, 'koraidon': 20, 'miraidon': 20, 'ting-lu': 20, 'chien-pao': 20, 'wo-chien': 20,
                'chi-yu': 20, 'gimmighoul': 0, 'ogerpon': 23, 'okidogi': 23, 'munkidori': 23, 'fezandipiti': 23, 'terapagos': 23,
                'pecharunt': 23, 'meloetta': 23, 'walkingwake': 23, 'ironleaves': 23}
TRADES = {'snom': [['trade', EN2N['flabebe'], 'Cortondo']], 'haunter': [['trade', EN2N['pincurchin'], 'Levincia']]}

entries = []
for s in slugs:
    n = slug2n[s]; v = SP[s]; b = v['base']; e = {'n': n, 'slug': s}
    ex = None
    if b.get('Violet', '').startswith('Trade from Scarlet'): ex = 'S'
    if b.get('Scarlet', '').startswith('Trade from Violet'): ex = 'V'
    for sec in ('tm', 'id'):
        if not ex and v[sec].get('Violet', '').startswith('Trade from Scarlet'): ex = 'S'
        if not ex and v[sec].get('Scarlet', '').startswith('Trade from Violet'): ex = 'V'
    e['ex'] = ex
    main = b.get('Scarlet') if not (b.get('Scarlet', '').startswith('Trade')) else b.get('Violet', '')
    main = main or ''
    in_base = bool(main) and not main.startswith('Transfer')
    tok = []; stop = None
    if in_base:
        ars = areas_of(main)
        ars.sort(key=lambda a: area_lv[n].get(a, 999))
        if ars: tok.append(['area', ars])
        rd = raids_of(main)
        cands = []
        if minlv[n] < 999: cands.append(stop_for(minlv[n]))
        cands += [FIXED_AREA_STOP[a] for a in ars if a in FIXED_AREA_STOP]
        if rd:
            tok.append(['raid', rd]); cands.append(RAID_STOP[rd[0]])
        if ars and all(a == 'Area Zero' for a in ars): cands = [20]
        if ars and not cands: cands.append(10)  # area without level data
        stop = min(cands) if cands else None
    dlc_tok = []
    for sec, st in (('tm', 21), ('id', 22)):
        t = v[sec].get('Scarlet') if not v[sec].get('Scarlet', '').startswith('Trade') else v[sec].get('Violet', '')
        if not t: continue
        ars = areas_of(t); rd = raids_of(t)
        if ars: dlc_tok.append([sec, ars])
        if rd and not in_base: dlc_tok.append(['raid', rd])
        if (ars or rd) and stop is None: stop = st
    e['dlc'] = not in_base
    e['tok'] = tok + dlc_tok if not in_base else tok
    e['dlcTok'] = dlc_tok if in_base else []
    if s in SPECIAL:
        e['tok'] = SPECIAL[s] + (e['tok'] if s in ('gimmighoul',) else []); stop = SPECIAL_STOP[s]
    if s in TRADES:
        e['tok'] = TRADES[s] + e['tok']; stop = min(stop if stop is not None else 99, 1 if s == 'snom' else 6)
    TITAN = {'klawf': 2, 'bombirdier': 4, 'orthworm': 8, 'greattusk': 13, 'irontreads': 13, 'tatsugiri': 18, 'dondozo': 18}
    if s in TITAN: stop = TITAN[s] if stop is None else min(stop, TITAN[s])
    e['stop'] = stop
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
            cand = max(ps, stop_for(L)) if (L and ps <= 20) else ps
            if not any(t[0] == 'evo' for t in e['tok']): e['tok'] = e['tok'] + [['evo', p, m]]
            if e['stop'] is None or cand < e['stop']: e['stop'] = cand; changed = True
miss = [e['slug'] for e in entries if e['stop'] is None or not e['tok']]
print('missing', miss)
kids = collections.defaultdict(list)
for e in entries:
    p = parent.get(e['n'])
    if p in by_n: kids[p].append(e['n'])
def disp(e):
    d = dexno[e['n']]
    return ('P', d['P']) if 'P' in d else (('K', d['K']) if 'K' in d else ('B', d['B']))
for e in entries:
    k, no = disp(e); e['id'] = '%s%03d' % (k, no)
    chain = []; cur = e['n']
    while kids.get(cur):
        ks = sorted(kids[cur], key=lambda n: by_n[n]['id'] if 'id' in by_n[n] else str(n))
        chain.append([[c, method(by_n[c])] for c in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain
    e['g'] = sorted({a for t in e['tok'] + e['dlcTok'] if t[0] in ('area', 'tm', 'id') for a in t[1]})
def key(e):
    t0 = e['tok'][0][0]
    pri = {'x': 0, 'trade': 1, 'area': 2, 'tm': 2, 'id': 2, 'raid': 3, 'evo': 4}.get(t0, 5)
    return (e['stop'], pri, minlv[e['n']] if minlv[e['n']] < 999 else 99, e['id'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries))
print('exclusives', collections.Counter(e['ex'] for e in entries))

# ---- Ominous Stakes ----
SR = json.load(open('stakes_raw.json'))
COLOR = {'Purple': ('P', 'wo-chien', 'Grasswither Shrine'), 'Yellow': ('Y', 'chien-pao', 'Icerend Shrine'),
         'Blue': ('B', 'chi-yu', 'Firescourge Shrine'), 'Green': ('G', 'ting-lu', 'Groundblight Shrine')}
stakes = [{'id': COLOR[c][0] + no, 'color': c, 'no': int(no), 'area': a.strip(), 'n': slug2n[COLOR[c][1]]} for c, no, a, _ in SR]
order = ['Purple', 'Yellow', 'Blue', 'Green']
stakes.sort(key=lambda s: (order.index(s['color']), s['no']))
out = {'entries': [{k: e[k] for k in ('id', 'n', 'stop', 'tok', 'g', 'evo', 'dlc', 'ex')} | ({'dlcTok': e['dlcTok']} if e['dlcTok'] else {})
                   | ({'dex': dexno[e['n']]}) for e in entries],
       'stops': [s for s, _ in STOPS], 'stakes': stakes,
       'areas': {re.sub(r'[()]', '', d['9']): {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d}
                 for d in LOCN.values() if '9' in d}}
json.dump(out, open('sv_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))))
