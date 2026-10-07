# Windshield Diopter Map, Version 2

## Files

- `WindShield-DioptorMap-ZOS.py`: main ZOS-API script
- `zrd_processing.py`: source control, NSC ray trace, and ZRD direction extraction
- `diopter_map.py`: angular-distortion calculation, diopter conversion, CSV export, and plotting
- `requirements.txt`: Python dependencies
- `.gitignore`: excludes generated ZRD, CSV, PNG, and cache files

## Before running

1. Keep all three `.py` files in the same project folder.
2. Confirm `testFile` in the main script points to `Windshield_Diopter.zmx`.
3. Confirm the five source objects are NCE objects 1 through 5.
4. Confirm `detector_object_number = 7` matches the actual detector row.
5. Confirm ray numbering is consistent across the five 10 x 10 source grids.

## Calculation

For each corresponding ray number, the script calculates the input-to-output deflection angle for center source M and each of the four surrounding M-prime sources. It selects the maximum absolute angular difference and divides by `0.012 m` to obtain optical power in diopters.

## Outputs

The script creates these files next to the Zemax model:

- five source-specific `.ZRD` files
- `windshield_diopter_map.csv`
- `windshield_diopter_map.png`

## Commit as Version 2

```powershell
git status
git add WindShield-DioptorMap-ZOS.py zrd_processing.py diopter_map.py requirements.txt .gitignore README.md
git commit -m "Version 2 - generate TL 957 windshield diopter map"
git log --oneline
```
