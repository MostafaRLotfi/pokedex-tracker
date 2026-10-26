import re,html,json
clean=lambda x: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
out={}
for line in open('la_urls.txt'):
  slug=line.strip().split('/')[2]; s=open('web/sw/%s.html'%slug,'rb').read().decode('latin-1')
  a=s.find('name="location"'); b=s.find('Flavor Text',a); loc=s[a:b]
  m=re.search(r'>\s*Legends: Arceus\s*</td>\s*<td[^>]*>(.*?)</td>',loc,re.S)
  raw=m.group(1) if m else ''
  # one line per area block: split on <br>
  parts=[clean(p) for p in re.split(r'(?i)<br\s*/?>',raw) if clean(p)]
  i=s.find('class="evochain"'); j=s.find('</table></td>',i); chain=s[i:j] if i>0 else ''
  evo={}
  for mm in re.finditer(r'evoicon/([^"]+?)\.png[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-swsh/([^"/]+)',chain,re.S):
    evo.setdefault(mm.group(2),[]).append(mm.group(1))
  out[slug]={'la':parts,'evo':evo}
json.dump(out,open('la_sp.json','w'))
print(len(out))
for k in ['rowlet','shinx','sneasler','porygon','spiritomb','unown','arceus','wyrdeer','kleavor','basculegion','magnemite','electivire']:
  if k in out: print(k,out[k]['la'][:4], out[k]['evo'].get(k))
