# Shared data builder for the older games (HGSS, DPPt, FRLG, RSE, …), driven by a per-game config dict.
import csv, json, re, html, glob, os, collections
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
SPECIES = set(EN.values())
N2EN = {v.lower(): k for k, v in EN.items()}
parent = {int(r[0]): (int(r[3]) if r[3] else None) for r in rows('pokemon_species.csv')}
clean = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?i)<br\s*/?>', ' || ', re.sub(r'<(?!br)[^>]+>', ' ', x)))).strip()
TIME = re.compile(r'^(Morning|Day|Night|Spring|Summer|Autumn|Winter|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b')

def parse_species(ids, spdir, classes, page='pokedex-dp'):
    """classes: {version code: css class of its row on the species page}"""
    out = {}
    for n in ids:
        s = open('%s/%03d.html' % (spdir, n), 'rb').read().decode('latin-1')
        a = s.find('name="location"'); b = s.find('Flavour', a)
        if b < 0: b = s.find('Flavor', a)
        loc = s[a:b]; r = {}
        for v, cls in classes.items():
            m = re.search(r'class="%s"[^>]*>[^<]*</td>\s*<td class="fooinfo"[^>]*>(.*?)</td>' % cls, loc, re.S)
            if m: r[v] = clean(m.group(1))
        i = s.find('class="evochain"'); j = s.find('</table></td>', i); chain = s[i:j] if i > 0 else ''
        evo = []
        for mm in re.finditer(r'evoicon/([^"]+?)\.png"[^>]*?(?:title="([^"]*)")?[^>]*>(?:(?!evoicon).)*?<a href="/%s/(\d+)\.shtml"' % page, chain, re.S):
            evo.append([mm.group(1), mm.group(2) or '', int(mm.group(3))])
        r['evo'] = evo; out[n] = r
    return out

def parse_area(path, verlabels):
    """verlabels: {'Pokémon HeartGold': ['HG'], 'Pokémon HeartGold & Pokémon SoulSilver': ['HG', 'SS'], ...}.
    Tables read "<Method> | [time] | Pokémon X | Mon | Mon | 40% | … | Level | … | 2 - 4 | …"."""
    s = open(path, 'rb').read().decode('latin-1')
    a = s.find('Wild Pok')
    t = html.unescape(re.sub(r'<[^>]+>', ' | ', s[a if a > 0 else 0:]))
    toks = [x.strip() for x in re.sub(r'\s+', ' ', t).split('|') if x.strip()]
    out, meth, cur, vers = [], '', None, None
    if 'Anchors' in toks:  # the anchor menu lists each table's title; the first table follows it without its own title
        k = toks.index('Anchors') + 1
        if k < len(toks): meth = toks[k]
        while k < len(toks) and toks[k] not in verlabels and not TIME.match(toks[k]): k += 1
        toks = toks[:toks.index('Anchors')] + toks[k:]
    def flush():
        if cur and cur['mons'] and vers:
            for v in vers: out.append([meth, v, min(cur['lv']) if cur['lv'] else 0] + cur['mons'])
    for i, x in enumerate(toks):
        if x in ('Trainers', 'Items', 'Pokémon of the Week'): break
        if x in verlabels:
            flush(); cur = {'mons': [], 'lv': [], 'done': False}; vers = verlabels[x]; continue
        if x.startswith('Pokémon ') and x not in SPECIES:  # another game's table
            flush(); cur = None; vers = None; continue
        isdata = re.match(r'^([\d.]+|Common|Rare|-+)%$', x) or x == 'Level' or re.match(r'^[\d -]+$', x)
        if cur is not None and vers:
            if x in SPECIES and not cur['done']: cur['mons'].append(x); continue
            if isdata:
                cur['done'] = True
                if re.match(r'^\d+ - \d+$', x): cur['lv'].append(int(x.split(' - ')[0]))
                elif re.match(r'^\d+$', x): cur['lv'].append(int(x))
                continue
        if not isdata and x not in SPECIES and not TIME.match(x) and len(x) < 50:
            flush(); cur = None; meth = x
    flush()
    return out

def build(cfg):
    ids = cfg['ids']
    SP = cfg['sp']; AR = cfg['ar']
    dexno = {int(sid): int(no) for sid, did, no in rows('pokemon_dex_numbers.csv') if did == str(cfg['dex'])}
    SLUGNAME = {u.split('/')[-1][:-6]: n.strip().replace('Pokemon', 'Pokémon') for u, n in (l.rstrip('\n').split('|') for l in open(cfg['areas_file']))}
    SLUGNAME.update(cfg.get('names_fix', {}))
    NAME2SLUG = {v: k for k, v in SLUGNAME.items()}
    LOC = {}
    for st, slugs in enumerate(cfg['loc']):
        for sl in slugs: LOC[sl] = st
    def gate(meth):
        m = meth.lower()
        return max([st for sub, st in cfg['gates'] if sub in m] or [0])
    VERS = cfg['vers']
    wild = collections.defaultdict(list)
    for slug, tabs in AR.items():
        if slug not in LOC: continue
        for meth, ver, lv, *mons in tabs:
            if any(k in meth.lower() for k in cfg.get('skip_methods', [])): continue
            st = max(LOC[slug], gate(meth))
            for m in mons:
                n = N2EN.get(m.lower())
                if n: wild[n].append((st, meth, lv, slug, ver))
    SPECIAL = cfg['special']; SPSTOP = cfg['spstop']
    def text_areas(txt):
        out = []
        if re.search(r'Inserted|Dual.?Slot|in the DS|GBA', txt or '', re.I): return out  # whole entry is a dual-slot encounter
        for part in re.split(r' , |, | \|\| |\|\|', txt or ''):
            part = part.strip()
            if re.search(r'slot|insert|FireRed|LeafGreen|Ruby|Sapphire|Emerald|Radar|Swarm|Mass Outbreak', part, re.I): continue  # dual-slot, Poké Radar, swarms
            nm = max((k for k in NAME2SLUG if part.startswith(k)), key=len, default=None)
            if nm and NAME2SLUG[nm] in LOC and NAME2SLUG[nm] not in out: out.append(NAME2SLUG[nm])
        return out
    tr = lambda x: bool(re.match(r'(Trade|Migrate|Transfer|Pal Park|Poké ?Transfer|Unobtainable|Not available|N/A)', x or '', re.I))
    entries = []
    for n in ids:
        s = SP[n]; e = {'n': n, 'dex': dexno[n]}
        av = [v for v in VERS if any(x[4] == v for x in wild[n]) or (s.get(v) and not tr(s.get(v)) and text_areas(s.get(v)))]
        e['ex'] = av if av and len(av) < len(VERS) else None
        tok = []; stop = None
        w = sorted(wild[n])
        if w:
            stop = w[0][0]; seen = []
            for st, meth, lv, slug, ver in w:
                if slug not in seen: seen.append(slug)
            tok.append(['area', seen]); e['lv'] = min(x[2] for x in w if x[0] == stop)
        extra = []
        for v in VERS: extra += [a for a in text_areas(s.get(v)) if a not in extra and (not w or a not in [x[3] for x in w])]
        if extra:
            if tok: tok[0][1] += extra
            else: tok.append(['area', extra])
            st = min(LOC[a] for a in extra)
            if stop is None: stop = st  # page text has no method, so it never overrides the gated wild tables
        if n in SPECIAL:
            k = SPECIAL[n]; tok = [['x', k]] + (tok if k not in cfg.get('notok', ['starter']) else []); stop = SPSTOP[k]
            if k in cfg.get('allvers', ['starter', 'event']): e['ex'] = None
        e['ex'] = cfg.get('ex', {}).get(n, e['ex'])
        e['tok'] = tok; e['stop'] = stop
        entries.append(e)
    by_n = {e['n']: e for e in entries}
    METH = {}
    for n, s in SP.items():
        for icon, title, child in s['evo']:
            if child not in METH and not icon.endswith('not') and not icon.startswith('mega'): METH[child] = icon
    if cfg.get('evo_pokeapi'):  # Gen 1–2: evolution methods from PokeAPI's table instead of Serebii's icons
        items = {r[0]: r[1] for r in rows('items.csv')}
        hdr = list(csv.reader(open('dl/pokemon_evolution.csv')))[0]
        for r in list(csv.reader(open('dl/pokemon_evolution.csv')))[1:]:
            v = dict(zip(hdr, r)); child = int(v['evolved_species_id'])
            if child in METH: continue
            trig = v['evolution_trigger_id']; it = items.get(v['trigger_item_id'], ''); held = items.get(v['held_item_id'], '')
            if trig == '1':
                if v['relative_physical_stats']: m = 'tyrogue20aed'
                elif v['minimum_happiness']: m = 'happiness' + {'day': 'day', 'night': 'night'}.get(v['time_of_day'], '')
                elif v['minimum_level']: m = 'l' + v['minimum_level']
                else: m = None
            elif trig == '2': m = 'trade' + ({'kings-rock': "king'srock", 'up-grade': 'upgrade'}.get(held, held.replace('-', '')))
            elif trig == '3': m = it.replace('-', '')
            else: m = None
            METH[child] = m
    METH.update(cfg.get('meth', {}))
    GATE = cfg.get('evogate', {})
    changed = True
    while changed:
        changed = False
        for e in entries:
            p = parent.get(e['n'])
            if p in by_n and by_n[p]['stop'] is not None and e['n'] not in SPECIAL:
                if not any(t[0] == 'evo' for t in e['tok']): e['tok'] = e['tok'] + [['evo', p, METH.get(e['n'])]]
                cand = max(by_n[p]['stop'], GATE.get(METH.get(e['n']), 0))
                if e['stop'] is None or cand < e['stop']: e['stop'] = cand; changed = True
        for e in entries:
            if e['stop'] is None and e['n'] not in SPECIAL:
                ks = [k for k, p in parent.items() if p == e['n'] and k in by_n and by_n[k]['stop'] is not None]
                if ks:
                    k = min(ks, key=lambda k: by_n[k]['stop']); e['stop'] = by_n[k]['stop']; e['tok'] = [['breed', k]] + e['tok']; changed = True
    MIN = cfg.get('minstop', {})  # e.g. desert Pokémon that need the Go-Goggles
    for e in entries:
        if e['n'] in MIN and e['stop'] is not None and e['stop'] < MIN[e['n']]: e['stop'] = MIN[e['n']]
    changed = True
    while changed:  # an evolution can't come before its pre-evolution; and it can be had in every version its pre-evolution can
        changed = False
        for e in entries:
            p = parent.get(e['n'])
            if p not in by_n or e['n'] in SPECIAL: continue
            q = by_n[p]
            if q['stop'] is not None and e['stop'] is not None and e['stop'] < q['stop'] and not any(t[0] == 'area' for t in e['tok']):
                e['stop'] = q['stop']; changed = True
            if e['ex'] is not None:
                av = sorted(set(e['ex']) | set(q['ex'] or VERS), key=VERS.index)
                av = None if len(av) == len(VERS) else av
                if av != e['ex']: e['ex'] = av; changed = True
    last = len(cfg['stops']) - 1
    for e in entries:
        if e['stop'] is None: e['stop'] = last; e['tok'] = e['tok'] or [['x', cfg.get('default_x', 'event')]]
    kids = collections.defaultdict(list)
    for e in entries:
        p = parent.get(e['n'])
        if p in by_n: kids[p].append(e['n'])
    for e in entries:
        chain = []; cur = e['n']
        while kids.get(cur):
            ks = sorted(kids[cur]); chain.append([[c, METH.get(c)] for c in ks])
            if len(ks) > 1: break
            cur = ks[0]
        e['evo'] = chain
        e['g'] = sorted({a for t in e['tok'] if t[0] == 'area' for a in t[1]})
        e['id'] = '%03d' % e['dex']
    pri = {'x': 0, 'area': 1, 'evo': 3, 'breed': 3}
    entries.sort(key=lambda e: (e['stop'], pri.get(e['tok'][0][0], 4), e.get('lv', 99), e['dex']))
    legs = [{'id': 'L%02d' % (i + 1), 'n': n, 'ex': [v] if v else None, 'area': a, 'req': q} for i, (n, v, a, q) in enumerate(cfg.get('legs', []))]
    regions = [str(x) for x in (cfg['region'] if isinstance(cfg['region'], list) else [cfg['region']])]
    LOCS = {r[0]: r[2] for r in rows('locations.csv') if r[1] in regions}
    LN = collections.defaultdict(dict)
    for lid, lang, name, *_ in rows('location_names.csv'):
        if lid in LOCS: LN[lid][lang] = name.replace('’', "'")
    byEN = {}
    for d in LN.values():
        if '9' in d: byEN.setdefault(d['9'], {l: d[c] for l, c in (('fr', '5'), ('de', '6'), ('ja', '11'), ('ko', '3'), ('zh-Hant', '4'), ('zh-Hans', '12')) if c in d})
    used = {a for e in entries for a in e['g']} | {l['area'] for l in legs} | set(cfg.get('used', []))
    names = {}
    for slug in sorted(used):
        en = SLUGNAME.get(slug, slug)
        names[slug] = dict(en=en, **byEN.get(cfg.get('alias', {}).get(en, en), {}))
    out = {'entries': [{k: e[k] for k in ('id', 'n', 'dex', 'stop', 'tok', 'g', 'evo', 'ex')} for e in entries], 'stops': cfg['stops'], 'legs': legs,
           'areas': names, 'vers': VERS, 'prefix': cfg['prefix'], 'key': cfg['key'], 'hleg': cfg.get('hleg', [])}
    out.update(cfg.get('extra', {}))
    json.dump(out, open(cfg['slug'] + '_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print(cfg['slug'], 'entries', len(entries), 'stops', dict(sorted(collections.Counter(e['stop'] for e in entries).items())),
          'ex', collections.Counter(tuple(e['ex']) if e['ex'] else None for e in entries).most_common(6), 'untranslated', [names[s]['en'] for s in names if len(names[s]) == 1][:12])
    return out
