# Parse Serebii Pokéarth Unova area pages: B2W2 wild tables -> {area: [[method, season, ver, lvmin, species...]]}
# Layout: "Pokémon Black 2 | <Method> | Spring - January, May, September | Mon | Mon | 70% | 30% | Level | Level | 5 - 15 | ... | Summer - ... | ..."
import re, html, json, sys, glob, os, csv
SPECIES = {r[2] for r in list(csv.reader(open('dl/pokemon_species_names.csv')))[1:] if r[1] == '9'}
VER = re.compile(r'^Pokémon (Black|White)(?: Version)? 2$')
OTHERVER = re.compile(r'^Pokémon (Black|White)(?: Version)?$')
def parse(path):
    s = open(path, 'rb').read().decode('latin-1')
    a = s.find('Wild Pok')
    t = html.unescape(re.sub(r'<[^>]+>', ' | ', s[a if a > 0 else 0:]))
    toks = [x.strip() for x in re.sub(r'\s+', ' ', t).split('|') if x.strip()]
    out, ver, meth, season, cur = [], None, None, '', None
    def flush():
        if cur and cur['mons']: out.append([meth, season, ver, min(cur['lv']) if cur['lv'] else 0] + cur['mons'])
    i = 0
    while i < len(toks):
        x = toks[i]
        if x in ('Trainers', 'Items'): break
        m = VER.match(x)
        if m or OTHERVER.match(x):
            flush(); cur = None
            ver = ('Black 2' if m.group(1) == 'Black' else 'White 2') if m else None
            nxt = toks[i + 1] if i + 1 < len(toks) else ''
            season = ''
            if nxt in SPECIES:  # "<Method> | Pokémon Black 2 | Mon | ..." (no seasons): the method came first
                prev = toks[i - 1] if i else ''
                if not re.match(r'^(\d|Level$|Pokémon )', prev) and prev not in SPECIES: meth = prev
                i += 1; continue
            meth = nxt; i += 2; continue
        if ver and re.match(r'^(Spring|Summer|Autumn|Winter) - ', x):
            flush(); season = x.split(' - ')[0]; cur = {'mons': [], 'lv': [], 'done': False}; i += 1; continue
        if ver:
            if cur is None: cur = {'mons': [], 'lv': [], 'done': False}
            if re.match(r'^([\d.]+|Common|Rare|-)%$', x) or x == 'Level': cur['done'] = True
            elif re.match(r'^\d+ - \d+$', x): cur['lv'].append(int(x.split(' - ')[0]))
            elif not cur['done'] and not re.match(r'^\d', x): cur['mons'].append(x)
            elif cur['done'] and not re.match(r'^[\d.]+%?$', x) and x != 'Level':  # next block without a season label
                flush(); cur = {'mons': [x], 'lv': [], 'done': False}
        i += 1
    flush()
    return out
if __name__ == '__main__':
    res = {}
    for f in sorted(glob.glob(sys.argv[1] + '/*.html')):
        res[os.path.basename(f)[:-5]] = parse(f)
    json.dump(res, open('b2_area.json', 'w'), ensure_ascii=False)
    print(len(res))
