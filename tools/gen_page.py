# usage: gen_page.py <scratch> <repo> <slug>   (uses <slug>_template.html, <slug>_data.json, <slug>_names.json, <slug>_i18n.js, <slug>_core.js)
import sys,os
S,R,g=sys.argv[1:4]
lg=open(R+'/letsgo/index.html').read()
style=lg[lg.index('<style>')+7:lg.index('</style>')].strip()
t=open(f'{S}/{g}_template.html').read()
out=(t.replace('__STYLE__',style).replace('__GAMESEL__','<select id="gamesel"></select>').replace('__DATA__',open(f'{S}/{g}_data.json').read())
      .replace('__NAMES__',open(f'{S}/{g}_names.json').read()).replace('__I18N__',open(f'{S}/{g}_i18n.js').read()).replace('__CORE__',open(f'{S}/{g}_core.js').read()))
os.makedirs(f'{R}/{g}',exist_ok=True); open(f'{R}/{g}/index.html','w').write(out); print(g,len(out))
