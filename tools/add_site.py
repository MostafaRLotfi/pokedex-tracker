# usage: add_site.py <repo> <slug>  — adds the game to the menu (menu.py), the front page card list and the README, from <slug>_site.json. Idempotent.
import sys, json, re, subprocess
R, slug = sys.argv[1], sys.argv[2]
S = json.load(open(slug + '_site.json'))
# menu.py: GAMES list (append at the end = oldest so far) and menu label translations
p = 'menu.py'; s = open(p).read()
if '("%s",' % slug not in s:
    s = re.sub(r'(GAMES=\[.*?)\]\n', lambda m: m.group(1) + ',("%s","%s","%s")]\n' % (slug, S['gkey'], S['label']['en']), s, count=1)
    s = s.replace("GKEYS={", "GKEYS={'%s':%s," % (S['gkey'], json.dumps({k: v for k, v in S['label'].items() if k != 'en'}, ensure_ascii=False)), 1)
    open(p, 'w').write(s)
# front page: card after the last card, plus its translations
p = R + '/index.html'; s = open(p).read()
nk, dk = S['cardkey'] + 'Name', S['cardkey'] + 'Desc'
if 'href="%s/"' % slug not in s:
    i = s.rindex('<span class="go" data-i18n="open">Open tracker →</span>\n    </a>\n') + len('<span class="go" data-i18n="open">Open tracker →</span>\n    </a>\n')
    card = ('    <a class="card" href="%s/">\n      <span class="gname" data-i18n="%s">%s</span>\n      <span class="gdesc" data-i18n="%s">%s</span>\n'
            '      <span class="go" data-i18n="open">Open tracker →</span>\n    </a>\n') % (slug, nk, S['name']['en'], dk, S['desc']['en'])
    s = s[:i] + card + s[i:]
    for lang, head in (('ja', ' ja:{'), ('fr', ' fr:{'), ('de', ' de:{'), ('ko', ' ko:{'), ('zh-Hant', ' "zh-Hant":{'), ('zh-Hans', ' "zh-Hans":{')):
        k = s.find('\n' + head); assert k > 0, head
        j = k + 1 + len(head)
        s = s[:j] + '%s:%s,%s:%s,' % (nk, json.dumps(S['name'][lang], ensure_ascii=False), dk, json.dumps(S['desc'][lang], ensure_ascii=False)) + s[j:]
    open(p, 'w').write(s)
# README: games table row after the last row, endgame sentence, prefix list, sources
p = R + '/README.md'; s = open(p).read()
if '/pokedex-tracker/%s/)' % slug not in s:
    rows = [m for m in re.finditer(r'^\| Pokémon .*\|$', s, re.M)]
    j = rows[-1].end() + 1
    s = s[:j] + S['readme_row'] + '\n' + s[j:]
    m = re.search(r'(- \*\*Endgame goals\.\*\*.*?)\n', s); s = s[:m.end(1)] + ' ' + S['readme_goal'] + s[m.end(1):]
    m = re.search(r"(- Each game's save code has its own prefix \(.*?)\)\.", s); s = s[:m.end(1)] + ', `%s` for %s' % (S['prefix'], S['label']['en']) + s[m.end(1):]
    m = re.search(r'(come from \[Serebii\]\(https://www\.serebii\.net/blackwhite/\)\.[^\n]*?)(?= Pokédex order)', s)
    if S['readme_src']: k = s.index(' Pokédex order and localized'); s = s[:k] + ' ' + S['readme_src'] + s[k:]
    open(p, 'w').write(s)
subprocess.run(['python3', '-I', 'menu.py', R], check=True, capture_output=True)
print('site updated for', slug)
