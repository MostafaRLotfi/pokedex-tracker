import re,html,json,collections
clean=lambda x: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?i)<br\s*/?>',' || ',x)))).strip()
out={}
for line in open('swsh_urls.txt'):
  slug=line.strip().split('/')[2]; s=open('web/sw/%s.html'%slug,'rb').read().decode('latin-1')
  a=s.find('name="location"'); b=s.find('Flavor Text',a); loc=s[a:b]
  r={'base':{},'ioa':{},'ct':{}}; sec='base'
  for row in re.findall(r'<tr>(.*?)</tr>',loc,re.S):
    if 'Brilliant Diamond' in row or 'Legends: Arceus' in row: break
    if re.search(r'>\s*(The )?Isle of Armor\s*<',row): sec='ioa'
    if re.search(r'>\s*(The )?Crown Tundra\s*<',row): sec='ct'
    m=re.search(r'class="(foox|fooy)"[^>]*>\s*(Sword|Shield)\s*</td>\s*<td class="fooinfo"[^>]*>(.*?)</td>',row,re.S)
    if m: r[sec][m.group(2)]=clean(m.group(3))
  i=s.find('class="evochain"'); j=s.find('</table></td>',i); chain=s[i:j] if i>0 else ''
  evo={}
  for mm in re.finditer(r'evoicon/([^"]+?)\.png[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-swsh/([^"/]+)',chain,re.S):
    evo.setdefault(mm.group(2),[]).append(mm.group(1))
  r['evo']=evo; out[slug]=r
json.dump(out,open('swsh_sp.json','w'))
