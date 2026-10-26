# Gold / Silver / Crystal: Johto Pokédex (251) through Johto's eight Gyms, then Kanto; encounters and evolutions from PokeAPI.
import build_g as b, pokeapi_ar as p
ids = [int(l) for l in open('gs_ids.txt')]
AR = p.tables({'4': 'G', '5': 'S', '6': 'C'})
p.area_names(list(AR) + ['mahogany-town', 'indigo-plateau', 'saffron-city', 'lavender-town'], 'gs_all_areas.txt')
SP = {n: {'evo': []} for n in ids}
J = lambda *n: ['johto-route-%d' % x for x in n]
K = lambda *n: ['kanto-route-%d' % x for x in n]
cfg = dict(slug='gsc', ids=ids, sp=SP, ar=AR, dex=3, areas_file='gs_all_areas.txt', region=[2, 1], vers=['G', 'S', 'C'], prefix='PGSC1-', key='pgsc',
  stops=['start', 'falkner', 'bugsy', 'whitney', 'morty', 'chuck', 'jasmine', 'pryce', 'clair', 'kanto', 'post', 'special'],
  loc=[['new-bark-town', 'cherrygrove-city', 'violet-city', 'sprout-tower'] + J(29, 30, 31),
       ['ruins-of-alph', 'union-cave', 'azalea-town', 'slowpoke-well'] + J(32, 33),
       ['ilex-forest', 'goldenrod-city'] + J(34),
       ['national-park', 'ecruteak-city', 'burned-tower', 'roaming-johto'] + J(35, 36, 37),
       ['olivine-city', 'cianwood-city', 'johto-sea-route-40', 'johto-sea-route-41'] + J(38, 39),
       [], [],
       ['mt-mortar', 'mahogany-town', 'lake-of-rage', 'team-rocket-hq', 'bell-tower'] + J(42, 43),
       ['ice-path', 'blackthorn-city', 'dragons-den', 'dark-cave', 'whirl-islands', 'tohjo-falls', 'kanto-victory-road-1', 'indigo-plateau'] + J(44, 45, 46) + K(26, 27),
       ['pallet-town', 'viridian-city', 'pewter-city', 'cerulean-city', 'vermilion-city', 'celadon-city', 'fuchsia-city', 'saffron-city', 'lavender-town',
        'cinnabar-island', 'rock-tunnel', 'mt-moon', 'digletts-cave', 'kanto-power-plant', 'kanto-sea-route-19', 'kanto-sea-route-20', 'kanto-sea-route-21']
        + K(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 22, 24, 25),
       ['mt-silver'] + K(28),
       []],
  gates=[('old-rod', 1), ('headbutt', 2), ('rock-smash', 3), ('squirt-bottle', 3), ('surf', 4), ('good-rod', 4), ('super-rod', 9), ('swarm-yes', 9)],
  special={152: 'starter', 155: 'starter', 158: 'starter', 251: 'celebi', 151: 'event', 123: 'contest', 127: 'contest'},
  spstop={'starter': 0, 'celebi': 11, 'event': 11, 'contest': 3},
  notok=['starter', 'celebi', 'event'], allvers=['starter', 'event', 'contest'],
  ex={251: ['C'], 172: None, 173: None, 174: None, 238: None, 239: None, 240: None},  # babies breed in every version; Crystal also has the Odd Egg
  evo_pokeapi=True, default_x='tradeold',
  hleg=[243, 244, 245, 249, 250, 251, 144, 145, 146, 150, 151],
  legs=[],
  used=['new-bark-town', 'violet-city', 'azalea-town', 'goldenrod-city', 'ecruteak-city', 'cianwood-city', 'olivine-city', 'mahogany-town', 'blackthorn-city'],
  extra={'startA': 'new-bark-town', 'startB': 'violet-city', 'magnetic': '', 'mossrock': '', 'icerock': '', 'charmPlace': 'goldenrod-city'})
b.build(cfg)
