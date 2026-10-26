# usage: place_cjk.py <repo>  — run after any page generation (with menu.py).
# Fills the Japanese, Korean and Chinese place names the PokeAPI tables lack, from the games' own location text
# (PKHeX's per-language tables in pkhex/, line-aligned with English). Only adds missing languages, never overwrites.
import sys, re, glob, json, unicodedata
R = sys.argv[1]
CJK = ['ja', 'ko', 'zh-Hant', 'zh-Hans']
# each page's tables first, then the rest as fallback
GAME = {'sv': ['sv'], 'la': ['la'], 'bdsp': ['bdsp', 'hgss'], 'swsh': ['swsh'], 'b2w2': ['bw2'], 'bw': ['bw2'], 'hgss': ['hgss'], 'dppt': ['bdsp', 'hgss'],
        'frlg': ['rsefrlg'], 'rse': ['rsefrlg'], 'gsc': ['gsc', 'hgss'], 'rby': ['rsefrlg', 'gsc'], 'oras': ['xy', 'rsefrlg'], 'usum': ['sm'], 'sm': ['sm'], 'xy': ['xy']}
ORDER = ['sv', 'la', 'bdsp', 'swsh', 'gg', 'sm', 'xy', 'bw2', 'hgss', 'rsefrlg', 'gsc']
FILES = {'sv': ['text_sv_00000', 'text_sv_30000'], 'la': ['text_la_00000'], 'bdsp': ['text_bdsp_00000', 'text_bdsp_30000'], 'swsh': ['text_swsh_00000', 'text_swsh_30000'],
         'bw2': ['text_bw2_00000', 'text_bw2_30000'], 'hgss': ['text_hgss_00000', 'text_hgss_02000'], 'rsefrlg': ['text_rsefrlg_00000'], 'gsc': ['text_gsc_00000'],
         'gg': ['text_gg_00000'], 'sm': ['text_sm_00000', 'text_sm_30000'], 'xy': ['text_xy_00000', 'text_xy_30000']}
# page names that differ from the in-game English (or are tracker groupings)
ALIAS = {'Kanto Power Plant': 'Power Plant', 'Team Aqua Hideout': 'Aqua Hideout', 'Team Magma Hideout': 'Magma Hideout', 'SS Tidal': 'S.S. Tidal',
         'Coastlands Base Camp': 'Coastlands Camp', 'Heights Base Camp': 'Heights Camp'}
# tracker groupings and the odd place missing from the tables, written by hand
REG = {'Kanto': ['カントー', '관동', '關都', '关都'], 'Johto': ['ジョウト', '성도', '城都', '城都'], 'Hoenn': ['ホウエン', '호연', '豐緣', '丰缘'], 'Sinnoh': ['シンオウ', '신오', '神奧', '神奥']}
HAND = {'Roaming ' + r: {'ja': '徘徊（%s）' % v[0], 'ko': '배회 (%s)' % v[1], 'zh-Hant': '徘徊（%s）' % v[2], 'zh-Hans': '徘徊（%s）' % v[3]} for r, v in REG.items()}
HAND['Lost Tower'] = {'ja': 'ロストタワー', 'ko': '로스트타워'}
def norm(s): return unicodedata.normalize('NFKC', s.replace('﻿', '')).strip()
def key(s): return re.sub(r'[^a-z0-9]', '', re.sub(r' \((FRLG|E|RS|DP|Pt|HGSS)\)$', '', norm(s)).lower().replace('é', 'e'))
TAB = {}
for g in ORDER:
    t = {}
    for f in FILES[g]:
        en = open('pkhex/%s_en.txt' % f, encoding='utf-8').read().split('\n')
        other = {l: open('pkhex/%s_%s.txt' % (f, l), encoding='utf-8').read().split('\n') for l in CJK}
        for i, e in enumerate(en):
            k = key(e)
            if not k or k in t: continue
            row = {l: norm(other[l][i]) for l in CJK if i < len(other[l]) and norm(other[l][i]) and not re.fullmatch(r'[-－—\s]*', norm(other[l][i]))}
            if row: t[k] = row
    TAB[g] = t
def look(en, games):
    if en in HAND: return HAND[en]
    en = ALIAS.get(en, en)
    cands = [en, re.sub(r'^Sea Route', 'Route', en)]
    for g in games + [x for x in ORDER if x not in games]:
        for c in cands:
            if key(c) in TAB[g]: return TAB[g][key(c)]
    return None
# some table entries carry per-game variants, "A (SM) / B (USUM)"; keep the one for this page and drop the tag
TAGS = {'usum': ['USUM'], 'sm': ['SM'], 'b2w2': ['B2W2'], 'bw': ['BW'], 'rse': ['E', 'RSE', '绿宝石', '綠寶石'], 'frlg': ['FRLG', '火红叶绿', '火紅葉綠'], 'rby': ['FRLG', '火红叶绿', '火紅葉綠']}
def pick(v, slug):
    parts = [re.match(r'^(.*?)(?: ?\(([^)]+)\))?$', p.strip()).groups() for p in v.split(' / ')]
    for name, tag in parts:
        if tag and tag in TAGS.get(slug, []): return name
    return parts[0][0]
pat = re.compile(r'\{"en":"([^"]+)"((?:,"[a-zA-Z-]+":"[^"]*")*)\}')           # {"en":..., "fr":...}
pat2 = re.compile(r'"([^"{}]+)":\{("fr":"[^"]*","de":"[^"]*"(?:,"[a-zA-Z-]+":"[^"]*")*)\}')  # "English":{"fr":...}
report = {}
for f in sorted(glob.glob(R + '/*/index.html')):
    slug = f.split('/')[-2]
    if slug not in GAME: continue
    s = open(f, encoding='utf-8').read(); miss = set(); added = [0]
    def fill(en, body):
        have = set(re.findall(r'"([a-zA-Z-]+)":', body))
        if not ({'fr', 'de'} & have): return body
        need = [l for l in CJK if l not in have]
        if not need: return body
        row = look(en, GAME[slug])
        if not row: miss.add(en); return body
        add = ''.join(',%s:%s' % (json.dumps(l), json.dumps(pick(row[l], slug), ensure_ascii=False)) for l in need if l in row)
        if add: added[0] += 1
        return body + add
    s2 = pat.sub(lambda m: '{"en":%s%s}' % (json.dumps(m.group(1), ensure_ascii=False), fill(m.group(1), m.group(2))), s)
    s2 = pat2.sub(lambda m: '%s:{%s}' % (json.dumps(m.group(1), ensure_ascii=False), fill(m.group(1), m.group(2))), s2)
    if s2 != s: open(f, 'w', encoding='utf-8').write(s2)
    report[slug] = (added[0], sorted(miss))
for k, (n, m) in report.items(): print(k, 'filled', n, 'missing', len(m), m)
