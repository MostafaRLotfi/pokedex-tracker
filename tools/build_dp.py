# Diamond / Pearl / Platinum: Platinum's Sinnoh Pokédex (210) through the eight Gyms in Platinum order, encounters from PokeAPI.
import build_g as b, pokeapi_ar as p
ids = [int(l) for l in open('dp_ids.txt')]
AR = p.tables({'12': 'D', '13': 'P', '14': 'Pt'})
p.area_names(list(AR) + ['iron-ruins', 'iceberg-ruins', 'rock-peak-ruins', 'twinleaf-town', 'oreburgh-city', 'eterna-city', 'hearthome-city', 'veilstone-city',
                         'pastoria-city', 'canalave-city', 'snowpoint-city', 'sunyshore-city', 'fullmoon-island'], 'dp_all_areas.txt')
SP = b.parse_species(ids, 'web/dp/sp', {'D': 'diamond', 'P': 'pearl', 'Pt': 'platinum'})
R = lambda *n: ['sinnoh-route-%d' % x for x in n]
cfg = dict(slug='dppt', ids=ids, sp=SP, ar=AR, dex=6, areas_file='dp_all_areas.txt', region=4, vers=['D', 'P', 'Pt'], prefix='PDPPT1-', key='pdppt',
  stops=['start', 'roark', 'gardenia', 'fantina', 'maylene', 'wake', 'byron', 'candice', 'volkner', 'post', 'special'],
  loc=[['twinleaf-town', 'lake-verity', 'verity-lakefront', 'sandgem-town', 'jubilife-city', 'ravaged-path', 'oreburgh-gate', 'oreburgh-city', 'oreburgh-mine'] + R(201, 202, 203, 204),
       ['floaroma-town', 'floaroma-meadow', 'valley-windworks', 'eterna-forest', 'old-chateau', 'eterna-city'] + R(205),
       ['mt-coronet', 'wayward-cave', 'hearthome-city', 'amity-square'] + R(206, 207, 208, 211),
       ['lost-tower', 'solaceon-town', 'solaceon-ruins', 'veilstone-city'] + R(209, 210, 215),
       ['valor-lakefront', 'pastoria-city', 'great-marsh'] + R(212, 213, 214),
       ['celestic-town', 'fuego-ironworks', 'canalave-city', 'iron-island'] + R(218, 219) + ['sinnoh-sea-route-220', 'sinnoh-sea-route-221'] + R(221),
       ['lake-valor', 'acuity-lakefront', 'snowpoint-city', 'lake-acuity'] + R(216, 217),
       ['spear-pillar', 'distortion-world', 'sunyshore-city', 'sinnoh-sea-route-223'] + R(222),
       ['sinnoh-victory-road', 'sinnoh-pokemon-league'],
       ['fight-area', 'survival-area', 'resort-area', 'stark-mountain', 'turnback-cave', 'sendoff-spring', 'trophy-garden', 'snowpoint-temple', 'newmoon-island',
        'fullmoon-island', 'flower-paradise', 'roaming-sinnoh', 'sinnoh-hall-of-origin-1', 'iron-ruins', 'iceberg-ruins', 'rock-peak-ruins', 'ruin-maniac-cave',
        'maniac-tunnel', 'sinnoh-pokemart'] + R(224, 225, 227, 228, 229) + ['sinnoh-sea-route-226', 'sinnoh-sea-route-230'],
       []],
  gates=[('rock-smash', 1), ('good-rod', 3), ('surf', 5), ('super-rod', 9), ('radar-on', 9), ('swarm-yes', 9), ('national-dex', 9), ('hall-of-fame', 9)],
  skip_methods=['slot2-ruby', 'slot2-sapphire', 'slot2-emerald', 'slot2-firered', 'slot2-leafgreen', 'pokemon-ranger'],
  special={387: 'starter', 390: 'starter', 393: 'starter', 408: 'fossil', 410: 'fossil', 489: 'event', 490: 'event', 491: 'event', 492: 'event', 493: 'event'},
  spstop={'starter': 0, 'fossil': 2, 'event': 10},
  notok=['starter', 'event'], allvers=['starter', 'event'],
  ex={408: ['D', 'Pt'], 410: ['P', 'Pt']},
  meth={134: 'waterstone', 135: 'thunderstone', 136: 'firestone', 196: 'happinessday', 197: 'happinessnight', 470: 'mossrock', 471: 'icerock', 106: 'tyrogue20aed', 107: 'tyrogue20aed', 237: 'tyrogue20aed'},
  evogate={'mossrock': 1, 'icerock': 6, 'levelcoronet': 2},
  hleg=[480, 481, 482, 483, 484, 487, 479],
  legs=[[485, '', 'stark-mountain', 'heatran'], [486, '', 'snowpoint-temple', 'regigigas'], [488, '', 'fullmoon-island', 'cresselia'],
        [377, 'Pt', 'rock-peak-ruins', 'regis'], [378, 'Pt', 'iceberg-ruins', 'regis'], [379, 'Pt', 'iron-ruins', 'regis'],
        [144, 'Pt', 'roaming-sinnoh', 'birds'], [145, 'Pt', 'roaming-sinnoh', 'birds'], [146, 'Pt', 'roaming-sinnoh', 'birds'],
        [491, '', 'newmoon-island', 'darkrai'], [492, '', 'flower-paradise', 'shaymin'], [493, '', 'sinnoh-hall-of-origin-1', 'arceus']],
  used=['twinleaf-town', 'oreburgh-city', 'eterna-city', 'hearthome-city', 'veilstone-city', 'pastoria-city', 'canalave-city', 'snowpoint-city', 'sunyshore-city',
        'sinnoh-route-201', 'mt-coronet', 'eterna-forest', 'sinnoh-route-217'],
  extra={'startA': 'twinleaf-town', 'startB': 'oreburgh-city', 'magnetic': 'mt-coronet', 'mossrock': 'eterna-forest', 'icerock': 'sinnoh-route-217', 'charmPlace': 'hearthome-city'})
b.build(cfg)
