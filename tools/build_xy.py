import csv, json, re, collections
SP = {int(k): v for k, v in json.load(open('xy_sp.json')).items()}
AR = json.load(open('xy_area.json'))
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
ids = [int(l) for l in open('xy_ids.txt')]
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
dexes = collections.defaultdict(dict)
for sid, did, no in rows('pokemon_dex_numbers.csv'):
    if did in ('12', '13', '14'): dexes[int(sid)][{'12': 'C', '13': 'O', '14': 'M'}[did]] = int(no)  # Central, Coastal, Mountain
SLUGNAME = {u.split('/')[-1][:-6]: n.strip() for u, n in (l.rstrip('\n').split('|') for l in open('xy_areas.txt'))}
SLUGNAME = {k: v.replace('Pokemon', 'Pokémon').replace('Poke Ball', 'Poké Ball') for k, v in SLUGNAME.items() if k != 'index'}
NAME2SLUG = {v: k for k, v in SLUGNAME.items()}
N2EN = {v.lower(): k for k, v in EN.items()}

STOPS = ['start', 'viola', 'grant', 'korrina', 'ramos', 'clemont', 'valerie', 'olympia', 'wulfric', 'post', 'special']
LOC = {}
def put(stop, *slugs):
    for s in slugs: LOC[s] = stop
put(0, 'vanivilletown', 'aquacordetown', 'route1', 'route2', 'route3', 'santaluneforest', 'santalunecity')
put(1, 'route4', 'lumiosecity', 'route5', 'camphriertown', 'route6', 'parfumpalace', 'route7', 'connectingcave', 'route8', 'ambrettetown', 'route9',
    'glitteringcave', 'cyllagecity', 'route22', 'battlechateau')
put(2, 'route10', 'geosengetown', 'route11', 'reflectioncave', 'shalourcity', 'towerofmastery')
put(3, 'route12', 'azurebay', 'coumarinecity')
put(4, 'route13', 'kalospowerplant')
put(5, 'route14', 'laverrecity', 'pokeballfactory')
put(6, 'route15', 'losthotel', 'route16', 'dendemilletown', 'frostcavern', 'route17', 'anistarcity')
put(7, 'route18', 'couriwaytown', 'terminuscave', 'route19', 'snowbellecity', 'teamflarehq', 'lysandrelabs', 'flarecafe')
put(8, 'route20', 'pokemonvillage', 'route21', 'victoryroad', 'pokemonleague')
put(9, 'kiloudecity', 'battlemaison', 'seaspiritsden', "seaspirit'sden", 'chamberofemptiness')
# method gates: Old Rod and Rock Smash (Ambrette Town), Surf (Shalour City), Good Rod (Coumarine City), Super Rod (Route 16)
def gate(meth):
    m = meth.lower()
    if 'super rod' in m: return 6
    if 'surf' in m or 'good rod' in m: return 3
    if 'rock smash' in m or 'old rod' in m: return 1
    return 0
wild = collections.defaultdict(list)
for slug, tabs in AR.items():
    if slug not in LOC: continue
    for meth, cond, ver, lv, *mons in tabs:
        st = max(LOC[slug], gate(meth))
        for m in mons:
            n = N2EN.get(m.lower().replace('’', "'"))
            if n: wild[n].append((st, meth, lv, slug, ver))
SPECIAL = {650: 'starter', 653: 'starter', 656: 'starter', 1: 'kanto', 4: 'kanto', 7: 'kanto', 696: 'fossil', 698: 'fossil', 142: 'aerodactyl', 448: 'lucario',
           131: 'lapras', 143: 'snorlax', 716: 'xerneas', 717: 'yveltal', 718: 'zygarde', 150: 'mewtwo', 144: 'birds', 145: 'birds', 146: 'birds',
           719: 'event', 720: 'event', 721: 'event'}
SPSTOP = {'starter': 0, 'kanto': 1, 'fossil': 1, 'aerodactyl': 1, 'lucario': 2, 'lapras': 3, 'snorlax': 1, 'xerneas': 7, 'yveltal': 7, 'zygarde': 9, 'mewtwo': 9, 'birds': 9, 'event': 10}
def text_areas(txt):
    out = []
    for part in re.split(r' , |, | \|\| ', txt or ''):
        part = part.strip()
        nm = max((k for k in NAME2SLUG if part.startswith(k)), key=len, default=None)
        if nm and NAME2SLUG[nm] in LOC and NAME2SLUG[nm] not in out: out.append(NAME2SLUG[nm])
    return out
entries = []
for n in ids:
    s = SP[n]; e = {'n': n, 'dex': dexes[n]}
    tr = lambda x: bool(re.match(r'(Trade|Migrate)', x or ''))
    r, sa = s.get('X', ''), s.get('Y', '')
    inR = any(x[4] == 'X' for x in wild[n]); inS = any(x[4] == 'Y' for x in wild[n])
    ex = None
    if (inR and not inS) or (tr(sa) and not tr(r)): ex = 'X'
    if (inS and not inR) or (tr(r) and not tr(sa)): ex = 'Y'
    ex = {716: 'X', 717: 'Y'}.get(n, ex)
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
        ks = sorted(kids[cur], key=lambda c: c)
        chain.append([[c, METH.get(c)] for c in ks])
        if len(ks) > 1: break
        cur = ks[0]
    e['evo'] = chain
    e['g'] = sorted({a for t in e['tok'] if t[0] == 'area' for a in t[1]})
    e['id'] = '%03d' % e['n']  # National number: Kalos has three regional dexes
def key(e):
    pri = {'x': 0, 'area': 1, 'evo': 3, 'breed': 3}.get(e['tok'][0][0], 4)
    return (e['stop'], pri, e.get('lv', 99), e['n'])
entries.sort(key=key)
print(collections.Counter(e['stop'] for e in entries)); print('exclusives', collections.Counter(e['ex'] for e in entries))
# Mega Stones: [species, form, item id, place slug, timing, note]
MR = json.load(open('xy_mega_raw.json'))
TIM = [('Postgame', 'post'), ('Given to you', 'gift')]
NOTE = {'If Starter': 'starter', 'Stone Emporium': 'emporium', 'traded Ralts': 'ralts', 'gifted Lucario': 'lucario', 'Serena/Calem': 'rival', 'Behind Abomasnow': 'abomasnow',
        'Unknown Dungeon': 'dungeon', 'Cyllage Gym': 'gym', 'B3F': 'b3f'}
STONE = {3: 'venusaurite', 6: ('charizardite-x', 'charizardite-y'), 9: 'blastoisinite', 15: 'beedrillite', 18: 'pidgeotite', 65: 'alakazite', 80: 'slowbronite',
         94: 'gengarite', 115: 'kangaskhanite', 127: 'pinsirite', 130: 'gyaradosite', 142: 'aerodactylite', 150: ('mewtwonite-x', 'mewtwonite-y'), 181: 'ampharosite',
         208: 'steelixite', 212: 'scizorite', 214: 'heracronite', 229: 'houndoominite', 248: 'tyranitarite', 254: 'sceptilite', 257: 'blazikenite', 260: 'swampertite',
         282: 'gardevoirite', 302: 'sablenite', 303: 'mawilite', 306: 'aggronite', 308: 'medichamite', 310: 'manectite', 319: 'sharpedonite', 323: 'cameruptite',
         334: 'altarianite', 354: 'banettite', 359: 'absolite', 362: 'glalitite', 373: 'salamencite', 376: 'metagrossite', 380: 'latiasite', 381: 'latiosite',
         428: 'lopunnite', 445: 'garchompite', 448: 'lucarionite', 460: 'abomasite', 475: 'galladite', 531: 'audinite', 719: 'diancite'}
megas = []
ALIAS = {'Reflecting Cave': 'reflectioncave', 'Frozen Cavern': 'frostcavern', 'Cave of Emptiness': 'chamberofemptiness', 'Shabboneau Castle': 'camphriertown',
         'Cyllage Gym': 'cyllagecity', 'Pokémon Village': 'pokemonvillage'}
for n, name, loc in MR:
    if n in (257, 380, 381): continue  # event-only stones
    form = name.split()[-1] if name.split()[-1] in ('X', 'Y') else ''
    item = STONE[n] if isinstance(STONE[n], str) else STONE[n][form == 'Y']
    ver = 'X' if 'X Only' in loc else ('Y' if 'Y Only' in loc else None)
    hows = []
    for p in [p.strip() for p in loc.split('|')]:
        place = p.split(' - ')[0].strip()
        if place.startswith('Held by'): place = p.split(' - ')[1] if ' - ' in p else ''
        slug = next((v for k, v in ALIAS.items() if place.startswith(k)), None) or NAME2SLUG.get(place.replace('Pokémon', 'Pokemon'), NAME2SLUG.get(place, ''))
        hows.append({'area': slug, 'when': next((k for s_, k in TIM if s_ in p), 'start'), 'note': next((k for s_, k in NOTE.items() if s_ in p), '')})
    megas.append({'id': 'M%02d' % (len(megas) + 1), 'n': n, 'form': form, 'item': item, 'ex': ver, 'how': hows})
print('megas', len(megas), [m['item'] for m in megas if not all(h['area'] for h in m['how'])])
LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] == '6'}
LN = collections.defaultdict(dict)
for lid, lang, name, *_ in rows('location_names.csv'):
    if lid in LOCS: LN[lid][lang] = name.replace('’', "'")
byEN = {}
for d in LN.values():
    if '9' in d: byEN.setdefault(d['9'], {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d})
used = {a for e in entries for a in e['g']} | {h['area'] for m in megas for h in m['how'] if h['area']} | {
    'vanivilletown', 'santalunecity', 'cyllagecity', 'shalourcity', 'coumarinecity', 'lumiosecity', 'laverrecity', 'anistarcity', 'snowbellecity'}
names = {}
for slug in sorted(used):
    en = SLUGNAME.get(slug, slug)
    alt = en
    names[slug] = dict(en=en, **byEN.get(alt, {}))
print('untranslated', [names[s]['en'] for s in names if len(names[s]) == 1])
out = {'entries': [{k: e[k] for k in ('id', 'n', 'dex', 'stop', 'tok', 'g', 'evo', 'ex')} for e in entries], 'stops': STOPS, 'megas': megas, 'areas': names}
json.dump(out, open('xy_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes', len(json.dumps(out, ensure_ascii=False)), 'megas', len(megas))
