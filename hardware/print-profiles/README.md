<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Bambu Lab P1S Print Profiles

Bambu Studio process and filament presets for OpenPet parts. Export each preset from Bambu Studio (*File → Export → Export Preset Bundle*, or the user-preset JSON) into this folder so they are versioned with the parts.

| Preset file (to add) | Material | Use | Key settings |
|---|---|---|---|
| `openpet-petg-structural.json` | PETG | Frame, brackets, leg links | 0.2 mm layers, 4 walls, 5 top/bottom, 30% gyroid, 0.4 mm nozzle |
| `openpet-plaplus-structural.json` | PLA+ | Frame parts away from heat, maquette | 0.2 mm layers, 3 walls, 25% gyroid |
| `openpet-plaplus-maquette.json` | PLA+ | P1 low-detail maquette | 0.28 mm layers, 2 walls, 10% infill |
| `openpet-asa-heat.json` | ASA | Parts near the Pi and servos | 0.2 mm layers, 4 walls, enclosure closed, no aux fan |
| `openpet-tpu95a.json` | TPU 95A | Paw pads, bumpers | External spool (not AMS), slow outer walls, 3 walls |
| `openpet-cosmetic-0.2nozzle.json` | PLA+/PETG | Fine shell details (optional 0.2 mm nozzle) | 0.1 mm layers |

Near-limit parts (over 240 mm in X or Y) also need the full plate area and no brim; they are flagged in the BOM.
