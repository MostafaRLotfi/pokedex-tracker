# Red / Blue / Yellow: Kanto Pokédex (151) through the eight Gyms; encounters and evolutions from PokeAPI.
import build_g as b, pokeapi_ar as p
ids = [int(l) for l in open('fr_ids.txt')]
AR = p.tables({'1': 'R', '2': 'B', '3': 'Y'})
p.area_names(list(AR) + ['pewter-city', 'lavender-town', 'indigo-plateau'], 'rb_all_areas.txt')
SP = {n: {'evo': []} for n in ids}
K = lambda *n: ['kanto-route-%d' % x for x in n]
cfg = dict(slug='rby', ids=ids, sp=SP, ar=AR, dex=2, areas_file='rb_all_areas.txt', region=1, vers=['R', 'B', 'Y'], prefix='PRBY1-', key='prby',
  stops=['start', 'brock', 'misty', 'surge', 'erika', 'koga', 'sabrina', 'blaine', 'giovanni', 'post', 'special'],
  loc=[['pallet-town', 'viridian-city', 'viridian-forest', 'pewter-city'] + K(1, 2, 22),
       ['mt-moon', 'cerulean-city'] + K(3, 4),
       ['vermilion-city', 'digletts-cave'] + K(5, 6, 11, 24, 25),
       ['rock-tunnel', 'celadon-city', 'kanto-underground-path', 'lavender-town'] + K(7, 8, 9, 10),
       ['pokemon-tower', 'fuchsia-city', 'kanto-safari-zone'] + K(12, 13, 14, 15, 16, 17, 18),
       ['saffron-city', 'kanto-power-plant', 'seafoam-islands', 'cinnabar-island', 'pokemon-mansion', 'kanto-sea-route-19', 'kanto-sea-route-20', 'kanto-sea-route-21'],
       [], [],
       ['kanto-victory-road-2', 'indigo-plateau'] + K(23),
       ['cerulean-cave'],
       []],
  gates=[('old-rod', 2), ('good-rod', 4), ('super-rod', 4), ('surf', 5)],
  special={151: 'event'}, spstop={'event': 10}, notok=['event'], allvers=['event'],
  evo_pokeapi=True,
  hleg=[144, 145, 146, 150, 151], legs=[],
  used=['pallet-town', 'pewter-city', 'cerulean-city', 'vermilion-city', 'celadon-city', 'fuchsia-city', 'saffron-city', 'cinnabar-island', 'viridian-city'],
  extra={'startA': 'pallet-town', 'startB': 'pewter-city', 'magnetic': '', 'mossrock': '', 'icerock': '', 'charmPlace': 'celadon-city'})
b.build(cfg)
