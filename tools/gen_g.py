# usage: gen_g.py <repo> <slug>   — assembles <repo>/<slug>/index.html for the older games from
#   <slug>_data.json (build_g.py), <slug>_game.json (game texts, 7 languages), common_i18n.json, g_template.html, g_core.js,
# and registers the game's save code in Copy all games on every page (ALL_KEYS + CODE_RE), idempotently.
import sys, json, glob, re, csv, math, os
R, slug = sys.argv[1], sys.argv[2]
D = json.load(open(slug + '_data.json')); G = json.load(open(slug + '_game.json')); C = json.load(open('common_i18n.json'))
LANGS = [["en","English"],["ja","日本語"],["fr","Français"],["de","Deutsch"],["ko","한국어"],["zh-Hant","繁體中文"],["zh-Hans","简体中文"]]
L = {'9': 'en', '1': 'ja', '5': 'fr', '6': 'de', '3': 'ko', '4': 'zh-Hant', '12': 'zh-Hans'}
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
# names
ns = {e['n'] for e in D['entries']} | {l['n'] for l in D['legs']}
NAMES = {l: {} for l in L.values()}
for sid, lang, name, *_ in rows('pokemon_species_names.csv'):
    if lang in L and int(sid) in ns: NAMES[L[lang]][sid] = name
ITEMS_W = ['dusk-stone', 'fire-stone', 'ice-stone', 'leaf-stone', 'moon-stone', 'shiny-stone', 'sun-stone', 'thunder-stone', 'water-stone', 'dawn-stone',
           'kings-rock', 'metal-coat', 'upgrade', 'dubious-disc', 'oval-stone', 'razor-claw', 'razor-fang', 'electirizer', 'magmarizer', 'protector', 'reaper-cloth',
           'dragon-scale', 'prism-scale', 'deep-sea-tooth', 'deep-sea-scale']
iid = {r[1]: r[0] for r in rows('items.csv')}; iid['upgrade'] = iid['up-grade']
ITEMS = {l: {} for l in L.values()}
for i, lang, name in rows('item_names.csv'):
    for k in ITEMS_W:
        if iid.get(k) == i and lang in L: ITEMS[L[lang]][k] = name
MOVES_W = {'ancientpower': 'ancient-power', 'doublehit': 'double-hit', 'mimic': 'mimic', 'rollout': 'rollout', 'stomp': 'stomp', 'taunt': 'taunt'}
mid = {r[1]: r[0] for r in rows('moves.csv')}
MOVES = {l: {} for l in L.values()}
for i, lang, name in rows('move_names.csv'):
    for k, v in MOVES_W.items():
        if mid[v] == i and lang in L: MOVES[L[lang]][k] = name
tid = {r[0]: r[1].capitalize() for r in rows('types.csv')}
TYPES = {l: {} for l in L.values()}
for i, lang, name in rows('type_names.csv'):
    if lang in L and int(i) <= 18: TYPES[L[lang]][tid[i]] = name
names_json = json.dumps({'NAMES': NAMES, 'ITEMS': ITEMS, 'MOVES': MOVES, 'TYPES': TYPES}, ensure_ascii=False, separators=(',', ':'))
# i18n: shared strings + this game's strings
I = {}
for lang, _ in LANGS:
    c, g = C[lang], G[lang]
    I[lang] = {'lv': c['lv'], 'sep': c['sep'], 'ui': {**c['ui'], **g.get('ui', {})}, 'how': {**c['how'], **g.get('how', {})}, 'cond': {**c['cond'], **g.get('cond', {})},
               'stopT': g['stopT'], 'tips': g.get('tips', {}), 'x': g.get('x', {}), 'req': g.get('req', {})}
I['en']['stopDefs'] = G['stopDefs']
if len(D['vers']) == 3:  # three versions: the first picker option reads "All versions"
    ALLV = {'ja': 'すべてのバージョン', 'fr': 'Toutes les versions', 'de': 'Alle Editionen', 'ko': '모든 버전', 'zh-Hant': '所有版本', 'zh-Hans': '所有版本'}
    for lang, v in ALLV.items(): I[lang]['ui']['verBoth'] = v
i18n_js = ('/* ---------- i18n ----------\n   Static English text lives in the HTML; dynamic English and every other language are below.\n'
           '   Shared strings come from the other trackers; Pokémon, item, type and place names come from PokeAPI (N, D.areas). */\n'
           'const LANGS = ' + json.dumps(LANGS, ensure_ascii=False) + ';\nconst I18N = ' + json.dumps(I, ensure_ascii=False, separators=(',', ':')) + ';\nI18N.en.stops = D.stops;\n')
# save-code registry: every game's prefix, storage key and code length (newest first, as on the front page)
nbytes = 1 + math.ceil(len(D['entries']) / 8) + math.ceil(len(D['legs']) / 8)
mylen = math.ceil(nbytes * 4 / 3)
reg = json.load(open('codes.json'))
if not any(r['prefix'] == D['prefix'] for r in reg): reg.append({'prefix': D['prefix'], 'key': D['key'], 're': ['%s[A-Za-z0-9_-]{%d}' % (D['prefix'], mylen)]})
json.dump(reg, open('codes.json', 'w'), indent=0)
allkeys = '[' + ','.join('["%s","%s-code"]' % (r['prefix'], r['key']) for r in reg) + ']'
codere = '/(' + '|'.join(p for r in reg for p in r['re']) + ')/g'
core = open('g_core.js').read().replace('__ALLKEYS__', allkeys).replace('__CODERE__', codere)
# template
E = G['en_static']
vopts = ''.join('\n      <option value="%d" data-i18n="ver%s">%s</option>' % (i + 1, v, G['en']['ui']['v_' + v]) for i, v in enumerate(D['vers']))
tagcss = '\n'.join('.tag.V%d{background:color-mix(in srgb,%s 16%%,transparent);color:%s}' % (i, c, c) for i, c in enumerate(G['colors']))
lg = open(R + '/letsgo/index.html').read(); style = lg[lg.index('<style>') + 7:lg.index('</style>')].strip()
t = open('g_template.html').read()
for k, v in (('__TITLE__', E['title']), ('__DESC__', E['desc']), ('__SUB__', E['sub']), ('__KDEX__', E['kDex']), ('__VEROPTS__', vopts.lstrip('\n')),
             ('__INTRO__', E['intro']), ('__SHINY__', E['shiny']), ('__LEGP__', E['legP']), ('__SEREBII__', E['serebii']), ('__PREFIX__', D['prefix']), ('__TAGCSS__', tagcss)):
    t = t.replace(k, v)
if len(D['vers']) == 3: t = t.replace('data-i18n="verBoth">Both versions<', 'data-i18n="verBoth">All versions<')
assert '__' not in t.replace('__STYLE__', '').replace('__GAMESEL__', '').replace('__DATA__', '').replace('__NAMES__', '').replace('__I18N__', '').replace('__CORE__', ''), re.findall(r'__[A-Z]+__', t)
page = (t.replace('__STYLE__', style).replace('__GAMESEL__', '<select id="gamesel"></select>').replace('__DATA__', json.dumps(D, ensure_ascii=False, separators=(',', ':')))
        .replace('__NAMES__', names_json).replace('__I18N__', i18n_js).replace('__CORE__', core))
os.makedirs(R + '/' + slug, exist_ok=True); open(R + '/' + slug + '/index.html', 'w').write(page)
open(slug + '_i18n.js', 'w').write(i18n_js)
# register this code on every other page and generated script (append to ALL_KEYS and CODE_RE once)
entry = '["%s","%s-code"]' % (D['prefix'], D['key']); alt = '%s[A-Za-z0-9_-]{%d}' % (D['prefix'], mylen)
targets = [R + '/index.html'] + [f for f in glob.glob(R + '/*/index.html') if not f.endswith('/' + slug + '/index.html')] + \
          [f for f in glob.glob('*_core.js') if not f.endswith('.v1.js') and f not in ('bd_core.js', 'g_core.js')] + ['allgames.py']
n = 0
for f in targets:
    s = open(f).read()
    if entry in s and alt in s: continue
    s2 = s if entry in s else re.sub(r'(ALL_KEYS=\[.*?\])\];', lambda m: m.group(1) + ',' + entry + '];', s, count=1)
    s2 = re.sub(r'(CODE_RE=/\(.*?)\)/g;', lambda m: m.group(1) + '|' + alt + ')/g;', s2, count=1)
    if 'CODE_RE=' not in s2: s2 = re.sub(r'(\.match\(/\(LGPE1-.*?)\)/g\)', lambda m: m.group(1) + '|' + alt + ')/g)', s2, count=1)  # front page: inline pattern
    if s2 != s: open(f, 'w').write(s2); n += 1
print(slug, 'page', len(page), 'code length', mylen, 'registered on', n, 'files')
