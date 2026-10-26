# Serebii /pokedex-sm/ species pages -> Sun/Moon locations (per version) and evolution links
import re, html, json
clean = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
out = {}
for line in open('sm_ids.txt'):
    n = int(line); s = open('web/sm/%03d.html' % n, 'rb').read().decode('latin-1')
    a = s.find('name="location"'); b = s.find('Flavor Text', a); loc = s[a:b]
    r = {}
    for ver, cls in (('S', 'foosun'), ('M', 'foomoon')):
        m = re.search(r'class="%s"[^>]*>[^<]*</td>\s*<td class="fooinfo"[^>]*>(.*?)</td>' % cls, loc, re.S)
        if not m: continue
        cell = m.group(1)
        r[ver] = {'text': clean(cell), 'areas': re.findall(r'/pokearth/alola/([^".]+)\.shtml">([^<]+)</a>\s*(\([^)]*\))?', cell)}
    i = s.find('class="evochain"'); j = s.find('</table></td>', i); chain = s[i:j] if i > 0 else ''
    evo = []
    for mm in re.finditer(r'evoicon/([^"]+?)\.png"[^>]*?(?:title="([^"]*)")?[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-sm/(\d+)\.shtml"><img src="/sunmoon/pokemon/(\d+(?:-\w+)?)\.png', chain, re.S):
        evo.append([mm.group(1), mm.group(2) or '', int(mm.group(3)), mm.group(4)])
    r['evo'] = evo; out[n] = r
json.dump(out, open('sm_sp.json', 'w'), ensure_ascii=False)
print(len(out))
