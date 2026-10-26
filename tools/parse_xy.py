# Serebii /pokedex-xy/ species pages -> X/Y location text (per version) and evolution links
import re, html, json
clean = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?i)<br\s*/?>', ' || ', re.sub(r'<(?!br)[^>]+>', ' ', x)))).strip()
out = {}
for line in open('xy_ids.txt'):
    n = int(line); s = open('web/xy/sp/%03d.html' % n, 'rb').read().decode('latin-1')
    a = s.find('name="location"'); b = s.find('Flavor Text', a); loc = s[a:b]
    r = {}
    for ver, cls in (('X', 'foox'), ('Y', 'fooy')):
        m = re.search(r'class="%s"[^>]*>[^<]*</td>\s*<td class="fooinfo"[^>]*>(.*?)</td>' % cls, loc, re.S)
        if m: r[ver] = clean(m.group(1))
    i = s.find('class="evochain"'); j = s.find('</table></td>', i); chain = s[i:j] if i > 0 else ''
    evo = []
    for mm in re.finditer(r'evoicon/([^"]+?)\.png"[^>]*?(?:title="([^"]*)")?[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-xy/(\d+)\.shtml"><img src="/xy/pokemon/(\d+(?:-\w+)?)\.png', chain, re.S):
        if not mm.group(1).startswith('mega'): evo.append([mm.group(1), mm.group(2) or '', int(mm.group(3)), mm.group(4)])
    r['evo'] = evo; out[n] = r
json.dump(out, open('xy_sp.json', 'w'), ensure_ascii=False)
print(len(out))
