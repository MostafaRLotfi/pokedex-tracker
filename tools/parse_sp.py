import re,html,json,os,sys,collections
D='web/sp'; out={}; icons=collections.Counter()
def clean(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
for f in sorted(os.listdir(D)):
  slug=f[:-5]; s=open(os.path.join(D,f),'rb').read().decode('latin-1')
  r={}
  a=s.find('name="location"'); b=s.find('Flavor Text',a); loc=s[a:b] if a>0 else ''
  m=re.search(r'>Legends: Z-A</td>\s*<td[^>]*>(.*?)</td>',loc,re.S)
  r['za']=clean(m.group(1)) if m else None
  m=re.search(r'>Legends: Z-A Mega Dimension</td>\s*<td[^>]*>(.*?)</td>',loc,re.S)
  r['md']=clean(m.group(1)) if m else None
  i=s.find('class="evochain"'); j=s.find('</table></td>',i)
  chain=s[i:j] if i>0 else ''
  # icon immediately preceding each pkmn link
  evo={}
  for m in re.finditer(r'evoicon/([^"]+?)\.png[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-sv/([^"/]+)',chain,re.S):
    evo.setdefault(m.group(2),[]).append(m.group(1)); icons[m.group(1)]+=1
  r['evo']=evo
  out[slug]=r
json.dump(out,open('sp.json','w'),indent=0)
print(len(out)); print(icons.most_common())
