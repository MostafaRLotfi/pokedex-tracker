# Ruby / Sapphire / Emerald: Hoenn Pokédex (202) through the eight Gyms; encounters from PokeAPI.
import build_g as b, pokeapi_ar as p
ids = [int(l) for l in open('rs_ids.txt')]
AR = p.tables({'7': 'R', '8': 'S', '9': 'E'})
p.area_names(list(AR) + ['oldale-town', 'mauville-city', 'fallarbor-town', 'verdanturf-town', 'hoenn-pokemon-league'], 'rs_all_areas.txt')
SP = b.parse_species(ids, 'web/dp/sp', {'R': 'ruby', 'S': 'sapphire', 'E': 'emerald'})
H = lambda *n: ['hoenn-route-%d' % x for x in n]
cfg = dict(slug='rse', ids=ids, sp=SP, ar=AR, dex=4, areas_file='rs_all_areas.txt', region=3, vers=['R', 'S', 'E'], prefix='PRSE1-', key='prse',
  stops=['start', 'roxanne', 'brawly', 'wattson', 'flannery', 'norman', 'winona', 'tateliza', 'sootopolis', 'post', 'special'],
  loc=[['littleroot-town', 'oldale-town', 'petalburg-city', 'petalburg-woods', 'rustboro-city'] + H(101, 102, 103, 104),
       ['rusturf-tunnel', 'dewford-town', 'granite-cave'] + H(106, 116),
       ['slateport-city', 'mauville-city', 'verdanturf-town'] + H(109, 110, 111, 112, 117, 118),
       ['fiery-path', 'meteor-falls', 'jagged-pass', 'lavaridge-town', 'fallarbor-town'] + H(113, 114, 115),
       ['mirage-tower'],
       ['fortree-city', 'new-mauville', 'abandoned-ship'] + H(105, 107, 108, 119, 120),
       ['hoenn-safari-zone', 'lilycove-city', 'mt-pyre', 'mossdeep-city', 'shoal-cave', 'team-aqua-hideout', 'team-magma-hideout'] + H(121, 122, 123, 124, 125, 127, 128),
       ['sootopolis-city', 'seafloor-cavern', 'pacifidlog-town', 'cave-of-origin', 'sky-pillar'] + H(126, 129, 130, 131, 132, 133, 134),
       ['hoenn-victory-road', 'ever-grande-city', 'hoenn-pokemon-league'],
       ['hoenn-battle-frontier', 'southern-island', 'desert-ruins', 'island-cave', 'ancient-tomb', 'marine-cave', 'terra-cave', 'artisan-cave', 'desert-underpass',
        'roaming-hoenn', 'hoenn-altering-cave', 'navel-rock', 'birth-island', 'faraway-island', 'mirage-island'],
       []],
  gates=[('old-rod', 1), ('good-rod', 2), ('rock-smash', 3), ('surf', 5), ('devon-scope', 5), ('super-rod', 6), ('seaweed', 7), ('dive', 7), ('hall-of-fame', 9), ('wailmer-pail', 9)],
  skip_methods=['colosseum-bonus-disc', 'pokemon-channel'],
  special={252: 'starter', 255: 'starter', 258: 'starter', 345: 'fossil', 347: 'fossil', 374: 'beldum', 385: 'event', 386: 'event'},
  spstop={'starter': 0, 'fossil': 4, 'beldum': 9, 'event': 10},
  notok=['starter', 'event'], allvers=['starter', 'event', 'fossil', 'beldum'],
  meth={134: 'waterstone', 135: 'thunderstone', 136: 'firestone', 106: 'tyrogue20aed', 107: 'tyrogue20aed', 237: 'tyrogue20aed'},
  names_fix={'mirage-island': 'Mirage Island'},
  minstop={27: 4, 28: 4, 328: 4, 329: 4, 330: 4, 331: 4, 332: 4, 343: 4, 344: 4},  # Route 111's desert needs the Go-Goggles
  hleg=[377, 378, 379, 380, 381, 382, 383, 384, 385, 386],
  legs=[[249, 'E', 'navel-rock', 'mystic'], [250, 'E', 'navel-rock', 'mystic'], [151, 'E', 'faraway-island', 'oldsea']],
  used=['littleroot-town', 'rustboro-city', 'dewford-town', 'mauville-city', 'lavaridge-town', 'petalburg-city', 'fortree-city', 'mossdeep-city', 'sootopolis-city'],
  extra={'startA': 'littleroot-town', 'startB': 'rustboro-city', 'magnetic': 'new-mauville', 'mossrock': '', 'icerock': '', 'charmPlace': 'lilycove-city'})
b.build(cfg)
