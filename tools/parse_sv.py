import re,html,json,os
clean=lambda x: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
out={}
for line in open('sv_urls.txt'):
  slug=line.strip().split('/')[2]; s=open('web/sp/%s.html'%slug,'rb').read().decode('latin-1')
  a=s.find('name="location"'); b=s.find('Flavor Text',a); loc=s[a:b]
  r={'base':{},'tm':{},'id':{}}; sec='base'
  for row in re.findall(r'<tr>(.*?)</tr>',loc,re.S):
    if 'Legends: Z-A' in row: break
    if 'The Teal Mask' in row: sec='tm'
    elif 'The Indigo Disk' in row: sec='id'
    m=re.search(r'class="(scarlet|violet)"[^>]*>\s*(Scarlet|Violet)\s*</td>\s*<td class="fooinfo"[^>]*>(.*?)</td>',row,re.S)
    if m: r[sec][m.group(2)]=clean(m.group(3))
  i=s.find('class="evochain"'); j=s.find('</table></td>',i); chain=s[i:j] if i>0 else ''
  evo={}
  for m in re.finditer(r'evoicon/([^"]+?)\.png[^>]*>(?:(?!evoicon).)*?<a href="/pokedex-sv/([^"/]+)',chain,re.S):
    evo.setdefault(m.group(2),[]).append(m.group(1))
  r['evo']=evo; out[slug]=r
json.dump(out,open('sv_sp.json','w'))
print(len(out))
for k in ['lechonk','larvitar','sprigatito','koraidon','ekans','dipplin','terapagos','wochien','gimmighoul','snom']:
  if k in out: print(k, {s:out[k][s] for s in ('base','tm','id')})
