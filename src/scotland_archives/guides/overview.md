# Scotland Archives MCP — Overview

This server provides structured access to three Scottish genealogy platforms,
chosen because they hold records *originating in Scotland* and are the primary
resources for Scottish family history research.

---

## Sources Covered

### 1. ScotlandsPeople — scotlandspeople.gov.uk

The official Scottish government genealogy website, operated by National Records
of Scotland (NRS). The single most important source for Scottish genealogy.

**What it holds:**
- Old Parish Registers (OPR): c.1553–1854 — Church of Scotland births, marriages, burials
- Statutory Registers: 1855–present — civil registration of births, marriages, deaths
- Census Records: 1841, 1851, 1861, 1871, 1881, 1891, 1901, 1911, 1921
- Wills & Testaments: 1513–1925
- Valuation Rolls: 1855–1989
- Catholic Parish Registers: c.1703–1993
- Church Records (non-established denominations): Free Church, Episcopal, etc.
- Prison Registers, Poor Relief, Military/Soldiers' Wills, Coats of Arms

**Access model:** Free index search. Images and full transcriptions require a
pay-per-view credit system or annual subscription.

**Tools available:** `search_scotlandspeople()`, `list_record_types()`, `list_scottish_counties()`

---

### 2. NLS Historic Maps — maps.nls.uk

National Library of Scotland's georeferenced historic map archive, with free
public access via web viewer and tile/WMS APIs.

**What it holds:**
- OS 6-inch 1st edition (1843–1882): first complete survey of Scotland
- OS 6-inch 2nd edition (1892–1905): updated Victorian survey
- OS 25-inch / 1:2500 (1855–1900): very detailed, individual buildings
- Scottish Parish Boundary Maps: essential for identifying correct OPR registers
- County & Estate Maps (pre-1840): pre-Ordnance Survey coverage
- Roy Military Survey (1747–1755): mid-18th century, pre-Clearances

**Access model:** Entirely free — web viewer and API tile services.

**Tools available:** `list_nls_map_series()`, `get_nls_map_url()`

---

### 3. Archives Hub — archiveshub.jisc.ac.uk

Aggregates archive finding aids from 350+ UK institutions. Scottish repositories
well-represented include:

- National Records of Scotland (NRS), Edinburgh
- National Library of Scotland (NLS), Edinburgh
- University of Edinburgh, University of Glasgow, University of Aberdeen, University of St Andrews
- Highland Archive Centre (Inverness)
- Orkney Archive, Shetland Archive
- Many local authority, church, and specialist archives

**What it holds:** Descriptions of archival collections — not the records themselves,
but structured finding aids that tell you what exists and where to find it.
Particularly useful for: estate papers, family collections, business records, church
minute books, and records that have not been digitised to ScotlandsPeople.

**Access model:** Free to search. Contact the holding repository for access to originals.

**Tools available:** `search_archives_hub()`, `get_archives_hub_record()`

---

## Research Strategy

1. **Date range first** — call `list_record_types()` to match your ancestor's
   likely period to the right record type.

2. **Identify the parish** — if you don't know the parish, use NLS parish maps
   (`get_nls_map_url(series_id='parish_maps', ...)`) to map the area and identify
   the ecclesiastical parish, which determines which OPR registers to search.

3. **Search ScotlandsPeople** — use `search_scotlandspeople()` to build the search
   URL for the most promising record type. Start with statutory registers (post-1855)
   or OPR (pre-1855), then use census to find the family in context, then
   valuation rolls to track them between censuses.

4. **Check institutional archives** — use `search_archives_hub()` to find family
   papers, estate records, church minute books, or specialist collections that
   have not been digitised.

5. **Use the research prompts** — `research_ancestor`, `find_church_records`, and
   `trace_emigration` provide structured multi-step workflows that call the tools
   in the right sequence.
