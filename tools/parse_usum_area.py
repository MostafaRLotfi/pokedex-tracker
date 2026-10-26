# Parse Serebii Pokéarth Alola area pages: USUM wild tables -> {area: [[method, cond, ver, lvmin, species...]]}
import re, html, json, sys, glob, os
clean = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
def parse(path):
    s = open(path, 'rb').read().decode('latin-1')
    a = s.find('Wild Pokémon'.encode('utf-8').decode('latin-1'))
    if a < 0: a = s.find('Wild Pok')
    if a < 0: return []
    e = [x for x in (s.find('Island Scan', a), s.find('>Trainers<', a)) if x > 0]
    seg = s[a:min(e) if e else len(s)]  # SM tables are skipped below: only "Pokémon Ultra Sun/Moon" rows are read
    t = re.sub(r'(\| )+', '| ', re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' | ', seg))))
    out = []
    # blocks: "<Method> | - | Toggle S.O.S. Details | [Day|Night |] Pokémon Ultra Sun | Initial Slot | Lv. a-b | Mon | % | ..."
    for m in re.finditer(r'\| ([^|]+?) \| - \| Toggle S\.O\.S\. Details \|(.*?)(?=\| [^|]+? \| - \| Toggle |\Z)', t):
        meth, body = m.group(1).strip(), m.group(2)
        cond = ''
        cm = re.match(r'\s*(Day|Night)\s*\|', body)
        if cm: cond = cm.group(1)
        for vm in re.finditer(r'Pokémon (Ultra Sun|Ultra Moon) \| Initial Slot \| Lv\. (\d+)(?:-\d+)? \|(.*?)(?=Additional S\.O\.S\.|Pokémon Ultra|\Z)', body):
            mons = [x.strip() for x in vm.group(3).split('|') if x.strip() and not re.match(r'^[\d.]+%$', x.strip())]
            out.append([meth, cond, vm.group(1), int(vm.group(2))] + mons)
        for vm in re.finditer(r'Additional S\.O\.S\. Slot \| Lv\. (\d+)(?:-\d+)? \| [\d.]+% \|(.*?)(?=Additional S\.O\.S\.|Pokémon Ultra|\Z)', body):
            pass  # SOS-only species (e.g. Salamence) are added from the species pages
    return out
if __name__ == '__main__':
    res = {}
    for f in sorted(glob.glob(sys.argv[1] + '/*.html')):
        r = parse(f)
        if r is not None: res[os.path.basename(f)[:-5]] = r
    json.dump(res, open('usum_area.json', 'w'), ensure_ascii=False)
    print(len(res))
