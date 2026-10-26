#!/bin/sh
# Downloads the reference tables the build reads (kept out of git):
#   dl/, dl2/  PokeAPI CSVs: names of Pokémon, items, moves, types and places; Gen 1–4 encounters
#   pkhex/     PKHeX location text: Japanese, Korean and Chinese place names PokeAPI lacks
set -e
cd "$(dirname "$0")"
API=https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv
PKH=https://raw.githubusercontent.com/kwsch/PKHeX/master/PKHeX.Core/Resources/text/locations
mkdir -p dl dl2 pkhex
for f in evolution_triggers item_names items location_names locations move_names moves pokedex_prose pokedexes pokemon pokemon_dex_numbers \
         pokemon_evolution pokemon_form_names pokemon_forms pokemon_species pokemon_species_names type_names types version_groups; do
  curl -sSfL -o dl/$f.csv $API/$f.csv
done
for f in encounter_condition_value_map encounter_condition_values encounter_methods encounter_slots encounters location_areas versions; do
  curl -sSfL -o dl2/$f.csv $API/$f.csv
done
for t in gen2/text_gsc_00000 gen3/text_rsefrlg_00000 gen4/text_hgss_00000 gen4/text_hgss_02000 gen5/text_bw2_00000 gen5/text_bw2_30000 \
         gen6/text_xy_00000 gen6/text_xy_30000 gen7/text_sm_00000 gen7/text_sm_30000 gen7/text_gg_00000 gen8/text_swsh_00000 gen8/text_swsh_30000 \
         gen8a/text_la_00000 gen8b/text_bdsp_00000 gen8b/text_bdsp_30000 gen9/text_sv_00000 gen9/text_sv_30000; do
  for l in en ja ko zh-Hans zh-Hant; do curl -sSfL -o pkhex/$(basename $t)_$l.txt $PKH/${t}_$l.txt; done
done
echo "reference data downloaded"
