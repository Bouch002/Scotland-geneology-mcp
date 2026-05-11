# Archives Hub — Research Guide

**URL:** https://archiveshub.jisc.ac.uk
**Operated by:** Jisc (formerly JANET)

---

## What Archives Hub Is

Archives Hub is a national aggregator of archive finding aids from UK universities,
colleges, and learned societies. It uses the Encoded Archival Description (EAD) standard
and is searchable via both a web interface and machine-readable protocols (SRU, OAI-PMH).

It is **not** a digitised record collection — it provides structured descriptions of what
archives exist and where they are held. To see the actual records, you contact the
holding repository.

---

## Scottish Repositories on Archives Hub

Archives Hub includes descriptions from major Scottish repositories:

| Repository | Focus |
|---|---|
| National Records of Scotland (NRS) | Government, court, church, and private records |
| National Library of Scotland (NLS) | Manuscripts, maps, printed books, photographs |
| University of Edinburgh | Historical collections, medical, scientific |
| University of Glasgow | Business records, literary, medical, colonial |
| University of Aberdeen | North-east Scotland, Gaelic, theological |
| University of St Andrews | Medieval, church, literary |
| Highland Archive Centre (Inverness) | Highland estate, church, local government |
| Orkney Archive | Orkney local records, estate papers |
| Shetland Archive | Shetland local records, Norse history |
| RCAHMS / HES | Built environment, archaeology |
| Various local authority archives | Burgh and county records |

---

## What You Can Find

### Family and Estate Papers
Private papers deposited by landed families — correspondence, accounts, legal papers,
estate plans, and in some cases tenant lists. Particularly valuable for tracing
ancestors who were tenants on a specific estate.

**Example search:** `search_archives_hub(query="Campbell estate papers Argyll")`

### Church Records Not on ScotlandsPeople
Many Kirk Session minute books, communion rolls, and heritors' records have been
deposited at universities or NRS but not yet digitised for ScotlandsPeople.

**Example search:** `search_archives_hub(query="Kirk Session minutes Sutherland")`

### Business and Occupational Records
Records of specific employers — particularly useful for ancestors in mining,
textile, or shipbuilding industries.

**Example search:** `search_archives_hub(query="coal mining records Lanarkshire")`

### Medical and Institutional Records
Hospital records, lunatic asylum registers, school log books. Some pre-date
and supplement ScotlandsPeople's prison and poor relief records.

### Maps and Plans
Estate plans and architectural drawings not available through NLS.

---

## Searching Effectively

### SRU Query Syntax (CQL)

The `search_archives_hub()` tool uses the SRU/CQL protocol. Basic searches are
plain text; advanced searches use CQL operators:

```
AND  — both terms required: "MacDonald AND Skye"
OR   — either term: "crofting OR crofter"
NOT  — exclude a term: "Campbell NOT Argyll"
"…"  — phrase search: "Highland Clearances"
```

### scottish_only Parameter

Setting `scottish_only=True` (the default) appends `AND "Scotland"` to the query.
This focuses results on Scottish-related descriptions but is a text filter, not an
institutional filter — a few non-Scottish institutions with Scotland-related collections
may appear, and a few Scottish institutions whose descriptions don't mention "Scotland"
explicitly may be excluded.

### Getting Full Details

`search_archives_hub()` returns summary Dublin Core records. If a result looks relevant,
use `get_archives_hub_record(identifier)` with the identifier from the search result to
retrieve the full record, which may include more detailed scope and content notes.

---

## Accessing the Records

Finding aids on Archives Hub describe what exists. To access the originals:

1. Note the holding repository from the record
2. Contact the repository directly (email/phone)
3. Many repositories offer:
   - Reading room visits (book in advance)
   - Paid research or copying services
   - Online ordering for some digitised items

NRS (Edinburgh) has an online ordering system for some record series.
Highland Archive Centre, Orkney, and Shetland archives are also well organised for
remote researchers.
