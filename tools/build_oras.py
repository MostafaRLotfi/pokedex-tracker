import csv, json, re, collections
SP = {int(k): v for k, v in json.load(open('oras_sp.json')).items()}
AR = json.load(open('oras_area.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
ids = [int(l) for l in open('oras_ids.txt')]
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
dexno = {int(sid): int(no) for sid, did, no in rows('pokemon_dex_numbers.csv') if did == '15'}
SLUGNAME = {u.split('/')[-1][:-6]: n.strip() for u, n in (l.rstrip('\n').split('|') for l in open('oras_areas.txt'))}
SLUGNAME['pokemonleague'] = 'Pokémon League'  # the menu text is cut at the accent
NAME2SLUG = {v: k for k, v in SLUGNAME.items()}
N2EN = {v.lower(): k for k, v in EN.items()}

STOPS = ['start', 'roxanne', 'brawly', 'wattson', 'flannery', 'norman', 'winona', 'tateliza', 'wallace', 'post', 'special']
LOC = {}
def put(stop, *slugs):
    for s in slugs: LOC[s] = stop
put(0, 'littleroottown', 'route101', 'oldaletown', 'route103', 'route102', 'petalburgcity', 'route104', 'petalburgwoods', 'rustborocity')
put(1, 'route116', 'rusturftunnel', 'dewfordtown', 'granitecave', 'route106')
put(2, 'slateportcity', 'route109', 'route110', 'mauvillecity', 'route117', 'verdanturftown', 'route118', 'route111', 'route112')
put(3, 'fierypath', 'route113', 'fallarbortown', 'route114', 'meteorfalls', 'route115', 'mt.chimney', 'jaggedpass', 'lavaridgetown')
put(4, 'miragetower')
put(5, 'route105', 'route107', 'route108', 'route119', 'fortreecity', 'route120', 'seamauville', 'newmauville')
put(6, 'route121', 'safarizone', 'lilycovecity', 'mt.pyre', 'route122', 'route123', 'route124', 'mossdeepcity', 'route125', 'shoalcave',
    'route127', 'route128', 'magmahideout', 'aquahideout', 'scorchedslab')
put(7, 'route126', 'sootopoliscity', 'seafloorcavern', 'route129', 'route130', 'route131', 'route132', 'route133', 'route134', 'pacifidlogtown',
    'caveoforigin', 'skypillar', 'sealedchamber', 'soaringinthesky', 'mirageisland', 'miragecave', 'mirageforest', 'miragemountain')
put(8, 'victoryroad', 'evergrandecity', 'pokemonleague')
put(9, 'battleresort', 'desertunderpass', 'sstidal', 'southernisland', 'terracave', 'marinecave', 'namelesscavern', 'pathlessplain', 'fabledcave',
    'gnarledden', 'tracklessforest', 'crescentisle', 'secretislet', 'secretmeadow', 'secretshore', 'trainerhill', 'battlefrontier', 'battletower',
    'artisancave', 'alteringcave')
# method gates: Old Rod (Dewford), Good Rod (Route 118), Rock Smash (Dynamo Badge), Surf (Balance Badge), Super Rod (Mossdeep), Dive, DexNav exclusives (National Pokédex)
def gate(meth):
    m = meth.lower()
    if 'post nat' in m or 'national' in m: return 9
    if 'dive' in m or 'underwater' in m or 'seaweed' in m: return 7
    if 'super rod' in m: return 6
    if 'surf' in m: return 5
    if 'rock smash' in m: return 3
    if 'good rod' in m: return 2
    if 'old rod' in m: return 1
    return 0
wild = collections.defaultdict(list)
for slug, tabs in AR.items():
    if slug not in LOC: continue
    for meth, cond, ver, lv, *mons in tabs:
        st = max(LOC[slug], gate(meth))
        for m in mons:
            n = N2EN.get(m.lower().replace('’', "'"))
            if n: wild[n].append((st, meth, lv, slug, ver))
SPECIAL = {252: 'starter', 255: 'starter', 258: 'starter', 345: 'fossil', 347: 'fossil', 351: 'castform', 374: 'beldum', 360: 'wynaut',
           380: 'eon', 381: 'eon', 382: 'kyogre', 383: 'groudon', 377: 'regi', 378: 'regi', 379: 'regi', 384: 'rayquaza', 385: 'jirachi', 386: 'deoxys'}
SPSTOP = {'starter': 0, 'fossil': 4, 'castform': 5, 'beldum': 9, 'wynaut': 3, 'eon': 7, 'kyogre': 7, 'groudon': 7, 'regi': 9, 'rayquaza': 9, 'jirachi': 10, 'deoxys': 9}
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
    r, sa = s.get('R', ''), s.get('S', '')
    inR = any(x[4] == 'Omega Ruby' for x in wild[n]); inS = any(x[4] == 'Alpha Sapphire' for x in wild[n])
    ex = None
    if (inR and not inS) or (tr(sa) and not tr(r)): ex = 'R'
    if (inS and not inR) or (tr(r) and not tr(sa)): ex = 'S'
    ex = {380: 'S', 381: 'R'}.get(n, ex)  # the story Lati: Latios in Omega Ruby, Latias in Alpha Sapphire (the other needs the Eon Ticket event)
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
DESERT = {27, 328, 331, 343}  # Sandshrew, Trapinch, Cacnea, Baltoy: Route 111's desert needs the Go-Goggles from Lavaridge
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
    e['id'] = '%03d' % e['dex']
def key(e):
    pri = {'x': 0, 'area': 1, 'evo': 3, 'breed': 3}.get(e['tok'][0][0], 4)
    return (e['stop'], pri, e.get('lv', 99), e['dex'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries)); print('exclusives', collections.Counter(e['ex'] for e in entries))
# legendaries outside the Hoenn Pokédex (Hoenn ones are checked off in the Pokédex): [n, version, place slug or key, requirement key]
LEG = [[250, 'R', 'seamauville', 'bell'], [249, 'S', 'seamauville', 'bell'], [485, '', 'scorchedslab', 'heatran'], [486, '', 'islandcave', 'regigigas'],
       [480, '', 'namelesscavern', 'lake'], [481, '', 'namelesscavern', 'lake'], [482, '', 'namelesscavern', 'lake'],
       [484, 'R', 'soaringinthesky', 'palkia'], [483, 'S', 'soaringinthesky', 'palkia'], [487, '', 'soaringinthesky', 'giratina'],
       [638, '', 'pathlessplain', 'swords'], [639, '', 'pathlessplain', 'swords'], [640, '', 'pathlessplain', 'swords'],
       [643, 'R', 'fabledcave', 'tao'], [644, 'S', 'fabledcave', 'tao'], [646, '', 'gnarledden', 'kyurem'],
       [243, '', 'tracklessforest', 'beasts'], [244, '', 'tracklessforest', 'beasts'], [245, '', 'tracklessforest', 'beasts'],
       [641, 'R', 'soaringinthesky', 'forces'], [642, 'S', 'soaringinthesky', 'forces'], [645, '', 'soaringinthesky', 'landorus'], [488, '', 'crescentisle', 'cresselia']]
legs = [{'id': 'L%02d' % (i + 1), 'n': n, 'ex': v or None, 'area': a, 'req': q} for i, (n, v, a, q) in enumerate(LEG)]
# Mega Stones: [species, form, item id, place slug, timing, note]
MR = json.load(open('oras_mega_raw.json'))
TIM = [('After Delta Episode', 'afterdelta'), ('Delta Episode', 'delta'), ('Primal', 'primal'), ('Beginning', 'start'), ('beginning', 'start'), ('receive Diancie', 'event')]
NOTE = {'Intriguing Stone': 'mrstone', 'Shoal Salts': 'shoal', 'If Starter': 'starter', 'Collector Altaria': 'altaria', "Zinnia's Grandmother": 'zinnia',
        'Steven after rematch': 'steven', 'From Mother': 'mother', 'Man in suit': 'mauvillehills', 'Cozmo': 'cozmo', 'Looker': 'looker', 'Poochyena': 'poochyena',
        'Wanda': 'wanda', 'Aarune': 'aarune', 'Lisia': 'lisia', 'Berry Garden': 'berry', 'Cycling Road': 'cycling', 'Market': 'market', 'Basement': 'basement'}
STONE = {3: 'venusaurite', 6: ('charizardite-x', 'charizardite-y'), 9: 'blastoisinite', 15: 'beedrillite', 18: 'pidgeotite', 65: 'alakazite', 80: 'slowbronite',
         94: 'gengarite', 115: 'kangaskhanite', 127: 'pinsirite', 130: 'gyaradosite', 142: 'aerodactylite', 150: ('mewtwonite-x', 'mewtwonite-y'), 181: 'ampharosite',
         208: 'steelixite', 212: 'scizorite', 214: 'heracronite', 229: 'houndoominite', 248: 'tyranitarite', 254: 'sceptilite', 257: 'blazikenite', 260: 'swampertite',
         282: 'gardevoirite', 302: 'sablenite', 303: 'mawilite', 306: 'aggronite', 308: 'medichamite', 310: 'manectite', 319: 'sharpedonite', 323: 'cameruptite',
         334: 'altarianite', 354: 'banettite', 359: 'absolite', 362: 'glalitite', 373: 'salamencite', 376: 'metagrossite', 380: 'latiasite', 381: 'latiosite',
         428: 'lopunnite', 445: 'garchompite', 448: 'lucarionite', 460: 'abomasite', 475: 'galladite', 531: 'audinite', 719: 'diancite'}
megas = []
for n, name, loc in MR:
    if n in (384, 719): continue  # Rayquaza needs no stone; Diancite only comes with the event Diancie
    form = name.split()[-1] if name.split()[-1] in ('X', 'Y') else ''
    item = STONE[n] if isinstance(STONE[n], str) else STONE[n][form == 'Y']
    parts = [p.strip() for p in loc.split('|')]
    vers = []
    for p in parts:
        v = 'R' if '(Omega Ruby)' in p else ('S' if '(Alpha Sapphire)' in p else '')
        place = p.split(' - ')[0].replace('(Omega Ruby)', '').replace('(Alpha Sapphire)', '').replace('(If Starter)', '').replace('(If not Starter)', '').strip()
        place = re.sub(r' (Market|Basement|Berry Garden)$', '', place)
        slug = {'Aqua Hideout': 'aquahideout', 'Magma Hideout': 'aquahideout', 'Pokémon League': 'pokemonleague'}.get(place) or NAME2SLUG.get(place, '')
        if place.startswith('On Lati'): slug = 'onlati'
        if place.startswith('Route 114 Stone Salesman'): slug = 'route114'
        if not slug and ('Cozmo' in p or 'Aarune' in p or 'Lisia' in p or 'Pokémon Center' in p): slug = ''
        tim = next((k for s_, k in TIM if s_ in p), 'start')
        note = next((k for s_, k in NOTE.items() if s_ in p), '')
        if 'Stone Salesman' in p: note = 'salesman'
        vers.append({'v': v, 'area': slug, 'when': tim, 'note': note})
    megas.append({'id': 'M%02d' % (len(megas) + 1), 'n': n, 'form': form, 'item': item, 'how': vers})
print('megas', len(megas), [m['item'] for m in megas if not all(h['area'] or h['note'] for h in m['how'])])
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '3'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name.replace('’', "'")
byEN = {}
for d in LN.values():
    if '9' in d: byEN.setdefault(d['9'], {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d})
used = {a for e in entries for a in e['g']} | {l['area'] for l in legs} | {h['area'] for m in megas for h in m['how'] if h['area'] and h['area'] != 'onlati'} | {
    'littleroottown', 'rustborocity', 'dewfordtown', 'mauvillecity', 'lavaridgetown', 'petalburgcity', 'fortreecity', 'mossdeepcity', 'sootopoliscity', 'evergrandecity', 'lilycovecity'}
names = {}
for slug in sorted(used):
    en = SLUGNAME.get(slug, {'islandcave': 'Island Cave'}.get(slug, slug)).replace('Pokemon', 'Pokémon')
    alt = {'Evergrande City': 'Ever Grande City', 'SS Tidal': 'S.S. Tidal'}.get(en, en)
    names[slug] = dict(en=en, **byEN.get(alt, {}))
names['soaringinthesky'].update({'ja': '大空', 'ko': '하늘', 'zh-Hant': '天空', 'zh-Hans': '天空'})  # not a PokeAPI location
if 'aquahideout' in names: names['aquahideout']['en'] = 'Aqua/Magma Hideout'
print('untranslated', [names[s]['en'] for s in names if len(names[s]) == 1])
out = {'entries': [{k: e[k] for k in ('id', 'n', 'dex', 'stop', 'tok', 'g', 'evo', 'ex')} for e in entries], 'stops': STOPS, 'legs': legs, 'megas': megas, 'areas': names}
json.dump(out, open('oras_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False)), 'legs', len(legs), 'megas', len(megas))
