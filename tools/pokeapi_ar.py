# Wild encounter tables for the Gen 1–4 games from PokeAPI's CSVs, in the shape build_g.build() expects:
#   AR = {location identifier: [[method, version code, min level, species name, ...], ...]}
# The method string carries any condition that matters for timing, e.g. "walk", "surf", "walk+radar-on", "walk+slot2-ruby".
import csv, collections
rows = lambda f: list(csv.reader(open(f)))[1:]
EN = {int(r[0]): r[2] for r in rows('dl/pokemon_species_names.csv') if r[1] == '9'}
SPEC = {int(r[0]): int(r[2]) for r in rows('dl/pokemon.csv')}            # pokemon id -> species id
LA = {r[0]: r[1] for r in rows('dl2/location_areas.csv')}                # location area -> location
LOC = {r[0]: r[2] for r in rows('dl/locations.csv')}                     # location id -> identifier
METH = {r[0]: r[1] for r in rows('dl2/encounter_methods.csv')}
SLOT = {r[0]: r[2] for r in rows('dl2/encounter_slots.csv')}             # slot -> method id
CVAL = {r[0]: r[2] for r in rows('dl2/encounter_condition_values.csv')}
COND = collections.defaultdict(list)
for eid, cv in rows('dl2/encounter_condition_value_map.csv'): COND[eid].append(CVAL[cv])
KEEP = ('radar-on', 'swarm-yes', 'slot2-', 'radio-hoenn', 'radio-sinnoh', 'story-progress-national-dex', 'story-progress-hall-of-fame',
        'story-progress-beat-elite-four-round-two', 'story-progress-beat-red', 'other-received-kanto-starter')

def tables(vers):
    """vers: {PokeAPI version id: our code}, e.g. {'12': 'D', '13': 'P', '14': 'Pt'}"""
    out = collections.defaultdict(lambda: collections.defaultdict(lambda: [999, set()]))
    for eid, vid, la, slot, pid, mn, mx in rows('dl2/encounters.csv'):
        if vid not in vers: continue
        conds = [c for c in COND.get(eid, []) if c.startswith(KEEP)]
        meth = '+'.join([METH[SLOT[slot]]] + sorted(conds))
        key = (meth, vers[vid])
        cell = out[LOC[LA[la]]][key]; cell[0] = min(cell[0], int(mn)); cell[1].add(EN[SPEC[int(pid)]])
    return {loc: [[m, v, lv] + sorted(mons) for (m, v), (lv, mons) in d.items()] for loc, d in out.items()}

def area_names(locs, path):
    """Writes "<fake url>|<English name>" lines for build_g (it reads slug -> name from the URL's file name)."""
    names = {r[0]: r[2] for r in rows('dl/location_names.csv') if r[1] == '9'}
    ids = {v: k for k, v in LOC.items()}
    with open(path, 'w') as f:
        for l in sorted(locs): f.write('/x/%s.shtml|%s\n' % (l, names.get(ids.get(l, ''), l).replace('’', "'")))
