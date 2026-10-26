# KytyPS5 Studio · community catalog

A list of community **forks** and **game patches** for [KytyPS5 Studio](https://github.com/kytystudio/kytyps5-studio), as plain JSON.
It contains **metadata only**: names, descriptions, links and checksums. No emulator builds and no patch files.

## Use it in Studio
Studio is preconfigured to read this repository (`kytystudio/kytyps5-studio-catalog`, `main` branch) when you open
Settings → Community (advanced). To use another catalog, change **Catalog URL** there to its `owner/repo`.
Nothing is installed until you press Install.

## `catalog.json`
```json
{
  "schema": 1,
  "forks":   [ { "id": "my-fork", "name": "Author · Title", "repo": "owner/repo", "author": "…",
                 "description": "…", "games": ["…"], "tags": ["…"], "notes": "…", "license": "GPL-2.0" } ],
  "patches": [ { "id": "my-patch", "titleId": "PPSA00000", "game": "…", "gameVersion": "01.000.000",
                 "name": "…", "author": "…", "version": "2026-01-01", "options": 3,
                 "file": "patches/PPSA00000-my-patch.json", "sha256": "…", "description": "…" } ]
}
```
- **Forks** need a GitHub repository whose releases contain a Windows `.zip`. Studio downloads it when the user presses Install.
- **Patches** are ETAHEN-style JSON files (`{"id": "PPSA…", "mods": [ … ]}`). `file` is a path in this repository
  (or use `url`). `sha256` is required: Studio refuses a file that does not match.
- `catalog.schema.json` describes the format; `python validate.py` checks it (it also runs on every push).

## Rules
1. **Metadata only.** Do not add emulator binaries, games, firmware, keys or dumps.
2. **Patch files are not in this repository.** They are made by other people. Entries here credit the author; the
   file is hosted only if the author agrees (then add it with `git add -f patches/<file>.json`). Without it,
   users get the file from the author and put it in their Studio community folder; the checksum tells them it is the right one.
3. Descriptions must be factual: say what is claimed and by whom, and mark anything unverified. No claims of legality or safety.
4. Every fork keeps its own license; list it in `license` when known.

## Pull requests
Add an entry, run `python validate.py`, open a PR. Keep one fork or patch per PR.

## License
No license is set yet. Choose one for the catalog text (for example CC0-1.0 for metadata) before publishing.

## Fork settings (optional)

Studio shows a fork's own options under **Fork settings** (read from the build's `--help`). Many forks switch
features such as frame generation with `KYTY_*` environment variables instead; describe those here so Studio gets a
proper menu for them:

- top-level `"settings"`: shared definitions. Studio shows one only for a build whose preset or README mentions the
  variables it sets (`"needs"` overrides which ones), so it can be written once for every fork that has the feature.
- `"settings"` inside a fork entry: definitions that fork always gets.

Kinds: `choice` (`choices: [{"label", "env": {"KYTY_X": "1"}}]`), `num` (`key`, `min`, `max`), `switch` (`on`, optional `off`)
and `text` (`key`). Only `KYTY_*` variables are accepted. Variables a build documents in a README table that no entry
covers still appear in Studio as plain text fields.
