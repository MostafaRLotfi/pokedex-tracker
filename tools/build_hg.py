# HeartGold / SoulSilver: Johto Pokédex route through Johto's eight Gyms, then Kanto, then the post-game.
import json, glob, os
import build_g as b
ids = [int(l) for l in open('hg_ids.txt')]
V = {'Pokémon HeartGold': ['HG'], 'Pokémon SoulSilver': ['SS'], 'Pokémon HeartGold & Pokémon SoulSilver': ['HG', 'SS']}
# area list: Johto pages plus Serebii's Kanto pages for this generation (kanto/4th)
with open('hg_all_areas.txt', 'w') as f:
    for l in open('hg_areas.txt'): f.write(l)
    for l in open('kanto_areas.txt'):
        if '/kanto/4th/' in l and 'index' not in l: f.write(l.replace('/kanto/4th/', '/kanto4/'))
AR = {}
for p in glob.glob('web/hg/areas/*.html') + glob.glob('web/kanto/4th/*.html'):
    AR[os.path.basename(p)[:-5]] = b.parse_area(p, V)
SP = b.parse_species(ids, 'web/dp/sp', {'HG': 'heartgold', 'SS': 'soulsilver'})
KANTO = ['pallettown', 'route1', 'viridiancity', 'route2', 'viridianforest', 'pewtercity', 'route3', 'mt.moon', 'route4', 'ceruleancity', 'route24', 'route25',
         'route5', 'route6', 'vermilioncity', "diglett'scave", 'route11', 'route9', 'route10', 'rocktunnel', 'powerplant', 'lavendertown', 'route8', 'route7',
         'celadoncity', 'saffroncity', 'route16', 'route17', 'route18', 'fuchsiacity', 'route12', 'route13', 'route14', 'route15', 'route19', 'route20',
         'seafoamislands', 'route21', 'cinnabarisland', 'route22', 'undergroundpath5-6', 'undergroundpath7-8', 'pokemontower', 'receptiongate']
cfg = dict(slug='hgss', ids=ids, sp=SP, ar=AR, dex=7, areas_file='hg_all_areas.txt', region=[2, 1], vers=['HG', 'SS'], prefix='PHGSS1-', key='phgss',
  stops=['start', 'falkner', 'bugsy', 'whitney', 'morty', 'chuck', 'jasmine', 'pryce', 'clair', 'kanto', 'post', 'special'],
  loc=[['newbarktown', 'route29', 'cherrygrovecity', 'route30', 'route31', 'violetcity', 'sprouttower'],
       ['route32', 'ruinsofalph', 'unioncave', 'route33', 'azaleatown', 'slowpokewell'],
       ['ilexforest', 'route34', 'goldenrodcity', 'goldenrodunderground', 'radiotower'],
       ['route35', 'nationalpark', 'route36', 'route37', 'ecruteakcity', 'burnedtower'],
       ['route38', 'route39', 'olivinecity', 'route40', 'route41', 'cianwoodcity', 'route47', 'route48', 'safarizone', 'safarizonegate', 'cliffcave',
        'cliffedgegate', 'shininglighthouse', 'pokeathlondome'],
       [], [],
       ['route42', 'mt.mortar', 'mahoganytown', 'route43', 'lakeofrage', 'rockethideout', 'bellchimetrail', 'belltower', 'tintower'],
       ['route44', 'icepath', 'blackthorncity', "dragon'sden", 'route45', 'route46', 'darkcave', 'whirlislands', 'route26', 'route27', 'tohjofalls', 'victoryroad'],
       KANTO + ['ssaqua', 'battlefrontier', 'battletower', 'frontieraccess'],
       ['mt.silver', 'route28', 'ceruleancave', 'embeddedtower', 'sinjohruins'],
       []],
  gates=[('old rod', 1), ('headbutt', 2), ('rock smash', 3), ('surf', 4), ('good rod', 4), ('super rod', 9), ('radio', 9), ('swarm', 9)],
  special={152: 'starter', 155: 'starter', 158: 'starter', 1: 'kanto', 4: 'kanto', 7: 'kanto', 175: 'togepi', 133: 'eevee', 236: 'tyrogue', 147: 'dratini',
           213: 'shuckle', 249: 'lugia', 250: 'hooh', 243: 'beasts', 244: 'beasts', 245: 'suicune', 144: 'birds', 145: 'birds', 146: 'birds', 150: 'mewtwo',
           151: 'event', 251: 'celebi', 172: 'pichu', 123: 'contest', 127: 'contest', 137: 'gamecorner', 138: 'fossil', 140: 'fossil', 142: 'fossil'},
  spstop={'starter': 0, 'kanto': 10, 'togepi': 1, 'eevee': 2, 'tyrogue': 7, 'dratini': 8, 'shuckle': 4, 'lugia': 8, 'hooh': 8, 'beasts': 4, 'suicune': 9,
          'birds': 10, 'mewtwo': 10, 'event': 11, 'celebi': 11, 'pichu': 9, 'contest': 3, 'gamecorner': 9, 'fossil': 9},
  notok=['starter', 'kanto', 'lugia', 'hooh', 'beasts', 'suicune', 'birds', 'mewtwo', 'celebi', 'event', 'pichu'],
  allvers=['starter', 'kanto', 'event', 'celebi', 'lugia', 'hooh', 'beasts', 'suicune', 'birds', 'mewtwo', 'pichu', 'togepi', 'eevee', 'tyrogue', 'dratini', 'shuckle', 'contest', 'gamecorner', 'fossil'],
  meth={134: 'waterstone', 135: 'thunderstone', 136: 'firestone', 196: 'happinessday', 197: 'happinessnight', 106: 'tyrogue20aed', 107: 'tyrogue20aed', 237: 'tyrogue20aed'},
  hleg=[250, 249, 245, 243, 244, 144, 145, 146, 150, 251, 151],
  legs=[[382, 'HG', 'embeddedtower', 'orb'], [383, 'SS', 'embeddedtower', 'orb'], [384, '', 'embeddedtower', 'jade'],
        [380, '', 'pewtercity', 'enigma'], [381, '', 'pewtercity', 'enigma'], [483, '', 'sinjohruins', 'sinjoh'], [484, '', 'sinjohruins', 'sinjoh'], [487, '', 'sinjohruins', 'sinjoh']],
  used=['newbarktown', 'violetcity', 'azaleatown', 'goldenrodcity', 'ecruteakcity', 'cianwoodcity', 'olivinecity', 'mahoganytown', 'blackthorncity', 'route29'],
  names_fix={'mt.silver': 'Mt. Silver', 'mt.mortar': 'Mt. Mortar', 'mt.moon': 'Mt. Moon', 'kanto4': ''},
  alias={'Bell Tower': 'Bell Tower', 'Mt. Silver': 'Mt. Silver'},
  extra={'startA': 'newbarktown', 'startB': 'violetcity', 'magnetic': '', 'mossrock': '', 'icerock': '', 'charmPlace': 'goldenrodcity'})
b.build(cfg)
