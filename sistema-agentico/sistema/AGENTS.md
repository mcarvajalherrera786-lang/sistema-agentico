# AGENTS.md

## Project
3D scene + render/animation pipeline ("Simpsons house" gag, Spanish-named objects). Scene: `simpsons_house.blend`. Source model: `src_model/source/casa nouuu.blend`.

## Commands
- No build/lint/test pipeline. Verify by running bpy scripts and checking their printed markers, then the output files.
- Motor 3D v5.2.
- Headless run: `python <script>.py` (uses the engine's bundled Python, `import bpy`).

## Gotchas
- Scripts hardcode absolute paths (`D:\Users\Asus\Desktop\...`; source has a space: `casa nouuu.blend`). Moving the repo means rewriting paths in every script.
- Render/save scripts call `bpy.ops.wm.save_as_mainfile` → overwrite `simpsons_house.blend`. Backups exist: `simpsons_house.blend1`, `simpsons_house_BACKUP.blend`.
- Frame ranges: car anim 1–96 (keyframes at 1/12/72/96); renders 97–192 → `anim/f_*.png` (1280x720 PNG, Freestyle on, 24 fps); video frames 1–96 + intro audio → `simpsons_garage_entry.mp4`.
- Behavior is keyed off object name prefixes: `Coche_*`, `Cam_*`, `Luz_*`, `Arbusto_*`, `Seto_Frontal`, `TH_*`, `BBQ_*`, `Columpio_*`, `Porche_*`, `TextoNoGirls`, `Garaje_*`.

## Outputs
- Frames: `anim/f_0001.png` … ; views: `simpsons_house_exterior.png`, `simpsons_house_treehouse.png`, `simpsons_house_salon.png`; video: `simpsons_garage_entry.mp4`.

## Environment quirks
- Windows + PowerShell: no `&&`, no `head`/`grep`/`which`; `ls -la` is invalid. Use separate calls / `Get-ChildItem`, `Get-Content -TotalCount N`.
- Shell cwd resets to repo root between calls; use `cd <dir>; pwd` in one command when you need to be elsewhere.

## OpenCode
- No `opencode.json` in repo; MCP del motor 3D disponible via opencode.
