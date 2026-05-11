# National Library of Scotland Historic Maps — Research Guide

**URL:** https://maps.nls.uk
**Operated by:** National Library of Scotland (NLS)

---

## Why Maps Matter for Genealogy

Maps are not just geographical aids — they are primary sources that name specific
farms, townships, crofts, and landmarks that appear in census records, OPR entries,
and estate papers. The NLS holds the largest collection of digitised historic maps
in the UK, nearly all free to access.

---

## Key Map Series for Scottish Genealogy

### OS 6-inch 1st Edition (1843–1882)
**series_id:** `os_6inch_1st`

The first complete, systematic large-scale survey of Scotland, carried out by the
Ordnance Survey. This is the single most useful map series for Victorian genealogy:
- Names every settlement, farm, and significant building
- Shows field boundaries, roads, tracks, and watercourses
- Coverage date aligns with the 1841 and 1851 census — you can find where an ancestor
  lived in the census and locate it precisely on this map

### OS 6-inch 2nd Edition (1892–1905)
**series_id:** `os_6inch_2nd`

Updated version of the 6-inch survey. Reflects late Victorian changes:
- New railway lines and stations
- Post-Clearance resettlement patterns
- Growth of industrial towns

### OS 25-inch / 1:2500 (1855–1900)
**series_id:** `os_25inch`

Very large-scale maps covering populated areas. Shows:
- Individual building footprints with acreages
- Room-level detail in towns
- Ideal for locating a specific house address from a census record
- Not available for all areas (mainly excludes remote rural areas)

### Scottish Parish Boundary Maps
**series_id:** `parish_maps`

These maps delineate the boundaries of historical Scottish ecclesiastical parishes —
the same parishes that maintained the OPR. Critical uses:
- Determine which parish a given farm or address belongs to
- Identify whether a location is near a parish boundary (the family may have recorded
  events in a neighbouring parish)
- Distinguish between civil and ecclesiastical parishes (they do not always match)

### County & Estate Maps (pre-OS, c.1580–1840)
**series_id:** `county_maps`

Pre-Ordnance Survey county surveys by cartographers such as:
- Blaeu's Atlas (1654) — covers all Scottish counties
- Timothy Pont's surveys (1580s–1610s) — earliest systematic mapping
- Roy's Military Survey (separate series)
- 18th-century estate plans — often show field names and tenant names

Coverage is patchy and scales vary, but invaluable for research before 1800.

### Roy Military Survey of Scotland (1747–1755)
**series_id:** `roy_military`

Commissioned after Culloden to map Scotland for military control. Covers the entire
mainland at approximately 1 inch to 1,000 yards. Key features for genealogy:
- Predates the Highland Clearances — shows pre-Clearance township layouts
- Names settlements in phonetic Gaelic transcriptions (with 18th-century English spellings)
- Excellent for mid-18th century Highland and Island research
- Shows drove roads and tracks not on later maps

---

## How to Use the Tools

### Finding coordinates for a location

If you know the place name but not the coordinates:
1. Use the NLS viewer at https://maps.nls.uk/geo/explore/ to search for the place
2. Note the latitude/longitude shown in the URL or location bar
3. Pass those coordinates to `get_nls_map_url()`

Scottish coordinate ranges:
- Latitude: 54.5°N (Mull of Galloway) to 60.9°N (Unst, Shetland)
- Longitude: -8.0°W (western Hebrides) to -0.7°W (Berwickshire coast)

### Zoom levels

| Series | Useful zoom | What you see |
|---|---|---|
| parish_maps | 10–12 | Parish boundaries across a county |
| os_6inch_1st / 2nd | 13–15 | Individual farms and buildings |
| os_25inch | 15–17 | Individual buildings with detail |
| roy_military | 12–14 | Township clusters |

### WMS vs XYZ tiles

- **XYZ tiles** work in any modern web mapping tool (Leaflet, MapLibre, QGIS, etc.)
  using the template URL returned by `get_nls_map_url()`
- **WMS GetMap** produces a single image for a defined bounding box
- **NLS viewer URL** opens the location directly in the NLS browser viewer — the
  easiest option for quick viewing

---

## Research Applications

**Locating a census address:** Take the address from the 1851 or 1901 census and use
the OS 6-inch 1st or 2nd edition to find the exact location.

**Identifying a parish:** Use the parish boundary maps to confirm which parish register
covers a given farm or village.

**Pre-Clearances research:** Use Roy (1747–1755) to see townships that were later cleared
and renamed or abandoned.

**Estate research:** County and estate maps often name individual tenants' holdings —
cross-reference with valuation rolls for the same period.
