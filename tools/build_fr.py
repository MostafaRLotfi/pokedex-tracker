# FireRed / LeafGreen: Kanto Pokédex (151) through the eight Gyms, then the Sevii Islands; encounters from PokeAPI.
import build_g as b, pokeapi_ar as p
ids = [int(l) for l in open('fr_ids.txt')]
AR = p.tables({'10': 'FR', '11': 'LG'})
p.area_names(list(AR) + ['pewter-city', 'cerulean-city', 'vermilion-city', 'celadon-city', 'fuchsia-city', 'saffron-city', 'cinnabar-island', 'viridian-city',
                         'pallet-town', 'kanto-pokemon-league'], 'fr_all_areas.txt')
SP = b.parse_species(ids, 'web/dp/sp', {'FR': 'firered', 'LG': 'leafgreen'})
K = lambda *n: ['kanto-route-%d' % x for x in n]
cfg = dict(slug='frlg', ids=ids, sp=SP, ar=AR, dex=2, areas_file='fr_all_areas.txt', region=1, vers=['FR', 'LG'], prefix='PFRLG1-', key='pfrlg',
  stops=['start', 'brock', 'misty', 'surge', 'erika', 'koga', 'sabrina', 'blaine', 'giovanni', 'post', 'special'],
  loc=[['pallet-town', 'viridian-city', 'viridian-forest', 'pewter-city'] + K(1, 2, 22),
       ['mt-moon', 'cerulean-city'] + K(3, 4),
       ['vermilion-city', 'ss-anne', 'digletts-cave'] + K(5, 6, 11, 24, 25),
       ['rock-tunnel', 'celadon-city', 'kanto-underground-path'] + K(7, 8, 9, 10),
       ['pokemon-tower', 'fuchsia-city', 'kanto-safari-zone'] + K(12, 13, 14, 15, 16, 17, 18),
       ['saffron-city', 'kanto-power-plant', 'seafoam-islands', 'cinnabar-island', 'pokemon-mansion', 'kanto-sea-route-19', 'kanto-sea-route-20', 'kanto-sea-route-21'],
       [],
       ['one-island', 'kindle-road', 'treasure-beach', 'mt-ember', 'cape-brink', 'bond-bridge', 'berry-forest', 'three-isle-port'],
       ['kanto-victory-road-2', 'kanto-pokemon-league'] + K(23),
       ['cerulean-cave', 'four-island', 'icefall-cave', 'five-island', 'five-isle-meadow', 'lost-cave', 'memorial-pillar', 'resort-gorgeous', 'water-labyrinth',
        'outcast-island', 'green-path', 'water-path', 'ruin-valley', 'trainer-tower', 'canyon-entrance', 'sevault-canyon', 'tanoby-ruins', 'pattern-bush',
        'kanto-altering-cave', 'roaming-kanto', 'dilford-chamber', 'liptoo-chamber', 'monean-chamber', 'rixy-chamber', 'scufib-chamber', 'viapos-chamber',
        'weepth-chamber', 'navel-rock', 'birth-island'],
       []],
  gates=[('old-rod', 2), ('good-rod', 4), ('super-rod', 4), ('surf', 5), ('rock-smash', 7), ('beat-elite-four', 9), ('national-dex', 9)],
  skip_methods=['colosseum-bonus-disc'],
  special={1: 'starter', 4: 'starter', 7: 'starter', 138: 'fossil', 140: 'fossil', 142: 'amber', 151: 'event'},
  spstop={'starter': 0, 'fossil': 5, 'amber': 5, 'event': 10},
  notok=['starter', 'event'], allvers=['starter', 'event', 'fossil', 'amber'],
  meth={134: 'waterstone', 135: 'thunderstone', 136: 'firestone', 106: 'tyrogue20aed', 107: 'tyrogue20aed'},
  hleg=[144, 145, 146, 150, 151],
  legs=[[243, '', 'roaming-kanto', 'beasts'], [244, '', 'roaming-kanto', 'beasts'], [245, '', 'roaming-kanto', 'beasts'],
        [249, '', 'navel-rock', 'mystic'], [250, '', 'navel-rock', 'mystic'], [386, '', 'birth-island', 'aurora']],
  used=['pallet-town', 'pewter-city', 'cerulean-city', 'vermilion-city', 'celadon-city', 'fuchsia-city', 'saffron-city', 'cinnabar-island', 'viridian-city'],
  extra={'startA': 'pallet-town', 'startB': 'pewter-city', 'magnetic': '', 'mossrock': '', 'icerock': '', 'charmPlace': 'celadon-city'})
b.build(cfg)
