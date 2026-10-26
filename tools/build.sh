#!/bin/sh
# Rebuilds every game page from the sources in this folder (run fetch_data.sh once first).
# letsgo/index.html and the front page are edited by hand; this script only refreshes their game menus.
set -e
cd "$(dirname "$0")"
REPO=..
for x in core.js data.json i18n.js names.json template.html; do cp b2_$x b2w2_$x; done  # build_b2.py writes b2_*, the page is b2w2
python3 -I gen_za.py . $REPO
for g in sv la bdsp swsh usum sm oras xy b2w2 bw; do python3 -I gen_page.py . $REPO $g; done
for g in hgss dppt frlg rse gsc rby; do python3 -I gen_g.py $REPO $g; done
python3 -I menu.py $REPO
python3 -I place_cjk.py $REPO
