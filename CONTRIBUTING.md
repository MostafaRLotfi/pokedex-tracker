# Contributing

Thanks for helping! The most useful help right now is **translation review**. The trackers come in English, 日本語, Français, Deutsch, 한국어, 繁體中文 and 简体中文. Pokémon, item, move, type and place names come from official game data. The sentences around them (stop titles, how-to text, tips, buttons) were written without a native speaker's review, so fixes to awkward or wrong phrasing are very welcome.

Not comfortable with code? [Open a translation issue](https://github.com/MostafaRLotfi/pokedex-tracker/issues/new?template=translation.md) and paste the wrong text and your suggestion. That's enough.

## Where the text lives

Each page in a game folder (`sv/index.html` and so on) is **generated**. Don't edit those files directly, because the next rebuild overwrites them. Edit the source in `tools/` instead:

| Page | Edit this |
|---|---|
| Legends: Z-A (`za`) | `tools/za_i18n_en.js`, `za_i18n_jafr.js`, `za_i18n_deko.js`, `za_i18n_zh.js` |
| Scarlet & Violet, Legends: Arceus, Sword & Shield, Ultra Sun & Ultra Moon, Sun & Moon, Omega Ruby & Alpha Sapphire, X & Y, Black & White | `tools/<folder>_i18n.js` (for example `tools/sv_i18n.js`) |
| Brilliant Diamond & Shining Pearl | `tools/bdsp_i18n.js` |
| Black 2 & White 2 | `tools/b2_i18n.js` |
| HeartGold & SoulSilver, Diamond, Pearl & Platinum, FireRed & LeafGreen, Ruby, Sapphire & Emerald | `tools/<folder>_game.py` (for example `tools/hgss_game.py`), then run it to update `<folder>_game.json` |
| Gold, Silver & Crystal and Red, Blue & Yellow | `tools/gen12_game.py` (it builds on the HeartGold & SoulSilver and FireRed & LeafGreen texts) |
| Text shared by the older games (column headers, evolution conditions, toasts) | `tools/common_i18n.json` |
| Let's Go and the front page | `letsgo/index.html` and `index.html` directly (these are hand-written) |

English text shown before the page script runs lives in each `tools/<folder>_template.html`, in elements marked `data-i18n`.

Please don't hand-edit **official names** (Pokémon, items, moves, types, places). They come from PokeAPI and the games' own text, and a rebuild would replace your edit. If an official name is wrong, open an issue instead.

## Rebuilding the pages

You need Python 3 and `curl`.

```sh
tools/fetch_data.sh   # once: downloads the reference tables (PokeAPI CSVs, PKHeX location text)
tools/build.sh        # regenerates every game page
```

Then open the page locally (for example `python3 -m http.server` in the repo folder) and switch languages to check your change. Include the regenerated `index.html` in your pull request together with the source change.

The `tools/build_*.py`, `parse_*.py` and `names_*.py` scripts refresh the Pokédex data itself from Serebii pages saved under `tools/web/`, which isn't in the repo. Translators never need them.

## Known gaps

These place names are still in English in Japanese, Korean and Chinese, because no reliable source was found:

- Scarlet & Violet: Grasswither Shrine, Icerend Shrine, Groundblight Shrine, Firescourge Shrine, League Club Room
- Legends: Arceus: Space-time distortion
- Legends: Z-A: Vernal Avenue (every language except English) and Quasartico Inc. (every language except English and Japanese)

If you know the official in-game names, a fix is welcome. Shared place names go in the `HAND` table in `tools/place_cjk.py`; the Z-A ones are in its `za_i18n_*.js` files.

## Save codes

Never change the bit order of an existing save code. A format change gets a new prefix (like `PSV2-`) while the old prefix keeps loading, so nobody loses progress.
