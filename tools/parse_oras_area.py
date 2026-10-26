# Parse Serebii Pokéarth Hoenn area pages: ORAS wild tables -> {area: [[method, '', ver, lvmin, species...]]}
import re, html, json, sys, glob, os
def parse(path):
    s = open(path, 'rb').read().decode('latin-1')
    t = re.sub(r'(\| )+', '| ', re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' | ', s))))
    out = []
    # "<Method> | Pokémon Omega Ruby | Mon | Mon | 40% | ... | Level | Level | 2 - 5 | ... | Pokémon Alpha Sapphire | ..."  (RSE tables say "Pokémon Ruby" and are skipped)
    for m in re.finditer(r'\| ([^|]+?) \| Pokémon Omega Ruby \|(.*?)\| Pokémon Alpha Sapphire \|(.*?)(?=\| [^|]+? \| Pokémon Omega Ruby \||\| Trainers \||\| Gen III \||\Z)', t):
        meth = m.group(1).strip()
        for ver, body in (('Omega Ruby', m.group(2)), ('Alpha Sapphire', m.group(3))):
            body = re.split(r'\| (?:Trainers|Items|Wild Pokémon|Anchors) \|', body)[0]  # stop before trainer and item tables
            toks = [x.strip() for x in body.split('|') if x.strip()]
            mons = []
            for x in toks:
                if re.match(r'^([\d.]+|Common|Rare|-)%$', x) or x == 'Level': break
                mons.append(x)
            lv = [int(x.split('-')[0]) for x in toks if re.match(r'^\d+ - \d+$', x)]
            if mons: out.append([meth, '', ver, min(lv) if lv else 0] + mons)
    return out
if __name__ == '__main__':
    res = {}
    for f in sorted(glob.glob(sys.argv[1] + '/*.html')):
        res[os.path.basename(f)[:-5]] = parse(f)
    json.dump(res, open('oras_area.json', 'w'), ensure_ascii=False)
    print(len(res))
