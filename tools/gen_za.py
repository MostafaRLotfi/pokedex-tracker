import re,sys
S,R=sys.argv[1],sys.argv[2]
lg=open(R+'/letsgo/index.html').read()
style=lg[lg.index('<style>')+7:lg.index('</style>')].strip()
t=open(S+'/za_template.html').read()
i18n=''.join(open(S+'/'+f).read() for f in ('za_i18n_en.js','za_i18n_jafr.js','za_i18n_deko.js','za_i18n_zh.js'))
out=(t.replace('__STYLE__',style).replace('__DATA__',open(S+'/za_data.json').read())
      .replace('__NAMES__',open(S+'/za_names.json').read()).replace('__I18N__',i18n).replace('__CORE__',open(S+'/za_core.js').read()))
import os; os.makedirs(R+'/za',exist_ok=True)
open(R+'/za/index.html','w').write(out); print(len(out))
