# Adds the Mightiest Mark (7-star Tera Raid event) list to sv_data.json and any missing names to sv_names.json.
# Oldest first: the save code stores one bit per raid in this order, so new events are only ever appended.
import json, csv
RAIDS = [  # [species, form, tera type, version (S/V) or '', first run YYYY-MM]
 [6, '', 'Dragon', '', '2022-12'], [815, '', 'Fighting', '', '2022-12'], [658, '', 'Poison', '', '2023-01'], [25, '', 'Water', '', '2023-02'],
 [724, '', 'Flying', '', '2023-03'], [503, '', 'Bug', '', '2023-03'], [157, '', 'Ghost', '', '2023-04'], [818, '', 'Ice', '', '2023-04'],
 [652, '', 'Rock', '', '2023-05'], [655, '', 'Fairy', '', '2023-07'], [812, '', 'Normal', '', '2023-07'], [150, '', 'Psychic', '', '2023-09'],
 [724, 'hisui', 'Grass', '', '2023-10'], [157, 'hisui', 'Fire', '', '2023-11'], [133, '', 'Normal', '', '2023-11'], [503, 'hisui', 'Water', '', '2023-11'],
 [991, '', 'Ice', '', '2023-12'], [257, '', 'Flying', '', '2024-01'], [395, '', 'Ice', '', '2024-02'], [3, '', 'Ground', '', '2024-02'],
 [9, '', 'Steel', '', '2024-03'], [154, '', 'Psychic', '', '2024-04'], [730, '', 'Fairy', '', '2024-05'], [260, '', 'Poison', '', '2024-05'],
 [500, '', 'Electric', '', '2024-06'], [254, '', 'Dragon', '', '2024-06'], [977, '', 'Water', '', '2024-07'], [149, '', 'Normal', '', '2024-08'],
 [727, '', 'Dark', '', '2024-09'], [497, '', 'Grass', '', '2024-09'], [392, '', 'Rock', '', '2024-10'], [160, '', 'Dark', '', '2024-11'],
 [389, '', 'Ground', '', '2024-11'], [908, '', 'Grass', '', '2025-02'], [911, '', 'Fire', '', '2025-03'], [914, '', 'Water', '', '2025-03'],
 [248, '', 'Ghost', '', '2025-03'], [373, '', 'Flying', '', '2025-04'], [376, '', 'Steel', '', '2025-05'], [445, '', 'Ground', '', '2025-05'],
 [233, '', 'Normal', '', '2025-06'], [998, '', 'Ice', '', '2025-06'], [784, '', 'Fighting', '', '2025-07'], [1005, '', 'Dragon', 'S', '2025-10'],
 [1006, '', 'Fairy', 'V', '2025-10'], [635, '', 'Poison', '', '2025-11'], [706, '', 'Water', '', '2025-11'], [887, '', 'Dragon', '', '2025-12'],
 [129, '', 'Dragon', '', '2026-07'], [970, '', 'Grass', '', '2026-08'], [979, '', 'Ghost', '', '2026-08'], [981, '', 'Fairy', '', '2026-08'],
 [983, '', 'Dark', '', '2026-08']]
rows = lambda f: list(csv.reader(open('dl/' + f)))[1:]
EN = {int(r[0]): r[2] for r in rows('pokemon_species_names.csv') if r[1] == '9'}
FIX = {991: 'Iron Bundle', 981: 'Farigiraf'}
for r in RAIDS:
    if r[0] in FIX: assert EN[r[0]] == FIX[r[0]], (r[0], EN[r[0]])
print([EN[r[0]] for r in RAIDS])
d = json.load(open('sv_data.json'))
d['raids'] = [{'id': 'R%02d' % (i + 1), 'n': n, 'form': f, 'tera': ty, 'ex': v or None, 'date': dt} for i, (n, f, ty, v, dt) in enumerate(RAIDS)]
json.dump(d, open('sv_data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
L = {'9': 'en', '1': 'ja', '5': 'fr', '6': 'de', '3': 'ko', '4': 'zh-Hant', '12': 'zh-Hans'}
N = json.load(open('sv_names.json')); added = 0
for sid, lang, name, *_ in rows('pokemon_species_names.csv'):
    if lang in L and int(sid) in {r[0] for r in RAIDS} and sid not in N['NAMES'][L[lang]]: N['NAMES'][L[lang]][sid] = name; added += 1
json.dump(N, open('sv_names.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('raids', len(RAIDS), 'names added', added)
