# Serebii /pokedex-bw/ species pages -> Black 2 / White 2 location text and evolution links
import re, html, json
clean = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?i)<br\s*/?>', ' || ', re.sub(r'<(?!br)[^>]+>', ' ', x)))).strip()
out = {}
for line in open('b2_ids.txt'):
    n = int(line); s = open('web/b2/sp/%03d.html' % n, 'rb').read().decode('latin-1')
    a = s.find('name="location"'); b = s.find('Flavor Text', a); loc = s[a:b]
    r = {}
    for ver, label in (('B', 'Black 2'), ('W', 'White 2')):
        m = re.search(r'class="foo(?:black|white)"[^>]*>\s*%s\s*</td>\s*<td class="fooinfo"[^>]*>(.*?)</td>' % label, loc, re.S)
        if m: r[ver] = clean(m.group(1))
    i = s.find('class="evochain"'); j = s.find('</table></td>', i); chain = s[i:j] if i > 0 else ''
    evo = []
    for mm in re.finditer(r'evoicon/([^"]+?)\.png"[^>]*?(?:title="([^"]*)")?[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-bw/(\d+)\.shtml"><img src="/pokedex-bw/evo/(\d+(?:-\w+)?)\.png', chain, re.S):
        evo.append([mm.group(1), mm.group(2) or '', int(mm.group(3)), mm.group(4)])
    r['evo'] = evo; out[n] = r
json.dump(out, open('b2_sp.json', 'w'), ensure_ascii=False)
print(len(out))
