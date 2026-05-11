"""Scotland Archives MCP — Scottish genealogy research tools."""

from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

import httpx
from fastmcp import FastMCP

mcp = FastMCP(
    "Scotland Archives",
    instructions=(
        "Tools for researching Scottish genealogy records. "
        "ScotlandsPeople is the primary source for most Scottish records (OPR, statutory registers, census, wills, etc.). "
        "NLS Historic Maps provides georeferenced maps for locating Scottish parishes and estates. "
        "Archives Hub gives access to institutional archive descriptions from Scottish repositories. "
        "Use list_record_types() first to identify which records suit the date range, then build search URLs with search_scotlandspeople()."
    ),
)

GUIDES_DIR = Path(__file__).parent / "guides"


# ── ScotlandsPeople — record type registry ─────────────────────────────────────

RECORD_TYPES: dict[str, dict] = {
    "opr_births": {
        "label": "Old Parish Registers — Births & Baptisms",
        "coverage": "c.1553–1854",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=opr_births",
        "tip": (
            "Spelling of surnames varied hugely — try MacDonald, McDonald, and M'Donald. "
            "Many parishes only start in the 1700s or later; check the parish catalogue for exact start dates."
        ),
    },
    "opr_marriages": {
        "label": "Old Parish Registers — Marriages & Banns",
        "coverage": "c.1553–1854",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=opr_marriages",
        "tip": (
            "Search on both bride and groom surnames. "
            "Banns (proclamations) were recorded weeks before the marriage date."
        ),
    },
    "opr_deaths": {
        "label": "Old Parish Registers — Deaths & Burials",
        "coverage": "c.1553–1854",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=opr_deaths",
        "tip": (
            "OPR death entries are sparse — many parishes recorded very few burials. "
            "If missing, check the statutory registers (post-1855) or Kirk Session minutes."
        ),
    },
    "stat_births": {
        "label": "Statutory Registers — Births",
        "coverage": "1855–present (recent years restricted)",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=stat_births",
        "tip": (
            "From 1855 these include full address, father's occupation, and informant name. "
            "Access to recent births (within ~100 years) is restricted."
        ),
    },
    "stat_marriages": {
        "label": "Statutory Registers — Marriages",
        "coverage": "1855–present",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=stat_marriages",
        "tip": "Both spouses' parents are named from 1855 — very useful for tracing two generations at once.",
    },
    "stat_deaths": {
        "label": "Statutory Registers — Deaths",
        "coverage": "1855–present (recent years restricted)",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=stat_deaths",
        "tip": (
            "Cause of death and usual residence recorded. "
            "Parents named even for elderly decedents — often the only record of parents for those born pre-1855."
        ),
    },
    "census": {
        "label": "Census Records",
        "coverage": "1841, 1851, 1861, 1871, 1881, 1891, 1901, 1911, 1921",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=census",
        "tip": (
            "Search all census years — family members may appear in different households. "
            "1841 only shows approximate ages (rounded down to nearest 5 for adults)."
        ),
    },
    "wills": {
        "label": "Wills & Testaments",
        "coverage": "1513–1925",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=wills",
        "tip": (
            "Scottish testaments were confirmed in Commissary Courts (pre-1823) then Sheriff Courts. "
            "They name executors and beneficiaries — useful for mapping family networks."
        ),
    },
    "valuation_rolls": {
        "label": "Valuation Rolls",
        "coverage": "1855–1989",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=valuation_rolls",
        "tip": (
            "Lists all property occupiers annually — excellent for tracking families between census years. "
            "Shows tenant name, proprietor name, and annual property value."
        ),
    },
    "catholic_registers": {
        "label": "Catholic Parish Registers",
        "coverage": "c.1703–1993",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=catholic_registers",
        "tip": (
            "Coverage is uneven; many Highland and Hebridean parishes have significant gaps. "
            "Useful for Irish immigrant communities in industrial Lowlands from the 1840s onward."
        ),
    },
    "church_records": {
        "label": "Church Records (non-OPR denominations)",
        "coverage": "Varies, c.1700s–1900s",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=church_records",
        "tip": (
            "Includes Free Church (post-1843 Disruption), United Presbyterian, Reformed Presbyterian, and Episcopalian registers. "
            "Essential for areas with strong Dissenting traditions."
        ),
    },
    "military": {
        "label": "Military Records & Soldiers' Wills",
        "coverage": "Various",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=soldiers_wills",
        "tip": "Soldiers' wills are brief field documents; cross-reference with service records at The National Archives (Kew) for full service history.",
    },
    "prison_records": {
        "label": "Prison Registers",
        "coverage": "1657–1939",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=prison_registers",
        "tip": "Often note place of birth, occupation, and physical description — useful for identifying individuals with common names.",
    },
    "poor_relief": {
        "label": "Poor Relief & Migration Records",
        "coverage": "c.1700s–1900s",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=poor_relief",
        "tip": (
            "Kirk Session poor relief records often predate statutory records by decades. "
            "Removal orders can reveal a person's place of origin when they moved parish."
        ),
    },
    "coats_of_arms": {
        "label": "Coats of Arms",
        "coverage": "1672–present",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=coats_of_arms",
        "tip": "Maintained by Lord Lyon King of Arms. Legally heritable in Scotland; grants name the recipient's lineage.",
    },
    "divorces": {
        "label": "Divorce Records",
        "coverage": "1984–present (Sheriff Court); Court of Session pre-1984",
        "search_path": "/record-results?search_type=PEOPLE&record_type[]=divorces",
        "tip": "Pre-1984 divorce records are held at the Court of Session; contact NRS for access.",
    },
}

SCOTTISH_COUNTIES = [
    "Aberdeenshire", "Angus (Forfarshire)", "Argyllshire", "Ayrshire",
    "Banffshire", "Berwickshire", "Buteshire", "Caithness",
    "Clackmannanshire", "Dumfriesshire", "Dunbartonshire", "East Lothian (Haddingtonshire)",
    "Fife", "Inverness-shire", "Kincardineshire", "Kinross-shire",
    "Kirkcudbrightshire", "Lanarkshire", "Midlothian (Edinburghshire)", "Moray (Elginshire)",
    "Nairnshire", "Orkney", "Peeblesshire", "Perthshire",
    "Renfrewshire", "Ross and Cromarty", "Roxburghshire", "Selkirkshire",
    "Shetland (Zetland)", "Stirlingshire", "Sutherland", "West Lothian (Linlithgowshire)",
    "Wigtownshire",
]

SCOTLANDSPEOPLE_BASE = "https://www.scotlandspeople.gov.uk"


@mcp.tool
def list_record_types() -> list[dict]:
    """List all Scottish genealogy record types available on ScotlandsPeople, with date coverage and research tips."""
    return [
        {"id": k, "label": v["label"], "coverage": v["coverage"], "tip": v["tip"]}
        for k, v in RECORD_TYPES.items()
    ]


@mcp.tool
def search_scotlandspeople(
    record_type: str,
    surname: str = "",
    forename: str = "",
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    county: str = "",
    parish: str = "",
) -> dict:
    """Build a ScotlandsPeople search URL for Scottish genealogy records.

    record_type: one of opr_births, opr_marriages, opr_deaths, stat_births,
    stat_marriages, stat_deaths, census, wills, valuation_rolls,
    catholic_registers, church_records, military, prison_records,
    poor_relief, coats_of_arms, divorces.

    Returns a direct URL to the ScotlandsPeople search results page plus
    contextual tips for that record type. ScotlandsPeople requires a
    subscription or pay-per-view account to view full records and images.
    """
    if record_type not in RECORD_TYPES:
        valid = ", ".join(RECORD_TYPES.keys())
        return {"error": f"Unknown record_type '{record_type}'. Valid values: {valid}"}

    info = RECORD_TYPES[record_type]
    params: list[str] = []

    if surname:
        params.append(f"surname={surname.upper()}")
    if forename:
        params.append(f"forename={forename}")
    if year_from is not None:
        params.append(f"year_from={year_from}")
    if year_to is not None:
        params.append(f"year_to={year_to}")
    if county:
        params.append(f"county={county}")
    if parish:
        params.append(f"parish={parish}")

    base = f"{SCOTLANDSPEOPLE_BASE}{info['search_path']}"
    url = f"{base}&{'&'.join(params)}" if params else base

    return {
        "url": url,
        "record_type": info["label"],
        "coverage": info["coverage"],
        "tip": info["tip"],
        "subscription_note": (
            "ScotlandsPeople requires a paid subscription or pay-per-view credits "
            "to view full records and images. Index searches are free."
        ),
    }


@mcp.tool
def list_scottish_counties() -> list[str]:
    """List all historical Scottish counties as used in genealogy records and ScotlandsPeople searches."""
    return SCOTTISH_COUNTIES


# ── NLS Historic Maps ──────────────────────────────────────────────────────────

NLS_MAP_SERIES: dict[str, dict] = {
    "os_6inch_1st": {
        "name": "OS 6-inch 1st edition (1843–1882)",
        "description": (
            "First complete large-scale survey of Scotland. Ideal for locating farms, "
            "crofts, and villages in the mid-Victorian era. Shows field boundaries and "
            "named buildings."
        ),
        "wms_layer": "os_6inch",
        "xyz_template": "https://mapseries-tilesets.s3.amazonaws.com/6inch/{z}/{x}/{y}.png",
        "nls_viewer_layer": "168",
        "min_zoom": 10,
        "max_zoom": 16,
    },
    "os_6inch_2nd": {
        "name": "OS 6-inch 2nd edition (1892–1905)",
        "description": (
            "Updated large-scale survey. Shows late Victorian/Edwardian changes — "
            "railway lines, new townships, post-Clearance resettlements."
        ),
        "wms_layer": "os_6inch_2nd",
        "xyz_template": "https://mapseries-tilesets.s3.amazonaws.com/6inch_2nd/{z}/{x}/{y}.png",
        "nls_viewer_layer": "169",
        "min_zoom": 10,
        "max_zoom": 16,
    },
    "os_25inch": {
        "name": "OS 25-inch / 1:2500 (1855–1900)",
        "description": (
            "Very detailed maps covering populated areas. Shows individual buildings, "
            "field boundaries, and acreages. Best for locating specific houses and farmsteads."
        ),
        "wms_layer": "os_25inch",
        "xyz_template": "https://mapseries-tilesets.s3.amazonaws.com/25inch/{z}/{x}/{y}.png",
        "nls_viewer_layer": "171",
        "min_zoom": 12,
        "max_zoom": 18,
    },
    "parish_maps": {
        "name": "Scottish Parish Boundary Maps",
        "description": (
            "Maps delineating historical Scottish civil and ecclesiastical parish boundaries. "
            "Essential for determining which OPR registers to search for a given location."
        ),
        "wms_layer": "parish_maps",
        "xyz_template": "https://mapseries-tilesets.s3.amazonaws.com/parish/{z}/{x}/{y}.png",
        "nls_viewer_layer": "193",
        "min_zoom": 8,
        "max_zoom": 14,
    },
    "county_maps": {
        "name": "County & Estate Maps (pre-OS, c.1580–1840)",
        "description": (
            "Pre-Ordnance Survey county surveys and estate plans. Coverage is patchy "
            "but invaluable for early modern and 18th-century research. Named farms "
            "and settlements often differ from later OS names."
        ),
        "wms_layer": "county_maps",
        "xyz_template": None,
        "nls_viewer_layer": "3",
        "min_zoom": 7,
        "max_zoom": 13,
    },
    "roy_military": {
        "name": "Roy Military Survey of Scotland (1747–1755)",
        "description": (
            "First systematic survey of Scotland, made after Culloden. Shows settlements, "
            "roads, and land use in the mid-18th century — predates the Clearances. "
            "Excellent for pre-1800 Highland research."
        ),
        "wms_layer": "roy",
        "xyz_template": "https://mapseries-tilesets.s3.amazonaws.com/roy/{z}/{x}/{y}.png",
        "nls_viewer_layer": "179",
        "min_zoom": 8,
        "max_zoom": 16,
    },
}

NLS_WMS_BASE = "https://gis.nls.uk/wms/historical"


def _deg_to_tile(lat: float, lon: float, z: int) -> tuple[int, int]:
    n = 2**z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int(
        (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi)
        / 2.0
        * n
    )
    return x, y


@mcp.tool
def list_nls_map_series() -> list[dict]:
    """List NLS historic map series available for Scotland, with descriptions and date coverage."""
    return [
        {
            "id": k,
            "name": v["name"],
            "description": v["description"],
            "min_zoom": v["min_zoom"],
            "max_zoom": v["max_zoom"],
            "has_xyz_tiles": v["xyz_template"] is not None,
        }
        for k, v in NLS_MAP_SERIES.items()
    ]


@mcp.tool
def get_nls_map_url(
    series_id: str,
    latitude: float,
    longitude: float,
    zoom: int = 13,
) -> dict:
    """Get NLS historic map tile and viewer URLs for a Scottish location.

    series_id: one of os_6inch_1st, os_6inch_2nd, os_25inch, parish_maps,
               county_maps, roy_military.
    latitude / longitude: WGS84 decimal degrees.
      Scotland spans approx 54.5–60.9°N, -8.0– -0.7°E.
    zoom: tile zoom level (higher = more detail). Clamped to the series range.

    Returns WMS GetMap URL, XYZ tile URL (where available), and an NLS viewer
    deep-link so the location can be opened directly in the browser.
    """
    if series_id not in NLS_MAP_SERIES:
        valid = ", ".join(NLS_MAP_SERIES.keys())
        return {"error": f"Unknown series_id '{series_id}'. Valid: {valid}"}

    series = NLS_MAP_SERIES[series_id]
    zoom = max(series["min_zoom"], min(zoom, series["max_zoom"]))
    tx, ty = _deg_to_tile(latitude, longitude, zoom)

    half_lon = 0.02
    half_lat = 0.01
    bbox = f"{longitude - half_lon},{latitude - half_lat},{longitude + half_lon},{latitude + half_lat}"

    result: dict = {
        "series": series["name"],
        "wms_capabilities": f"{NLS_WMS_BASE}?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities",
        "wms_get_map": (
            f"{NLS_WMS_BASE}?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap"
            f"&LAYERS={series['wms_layer']}&CRS=EPSG:4326"
            f"&BBOX={bbox}&WIDTH=800&HEIGHT=600&FORMAT=image/png"
        ),
        "nls_viewer_url": (
            f"https://maps.nls.uk/geo/find/#zoom={zoom}"
            f"&lat={latitude}&lon={longitude}&layers={series['nls_viewer_layer']}"
        ),
        "zoom": zoom,
        "tile_x": tx,
        "tile_y": ty,
    }

    if series["xyz_template"]:
        result["xyz_tile_url"] = (
            series["xyz_template"]
            .replace("{z}", str(zoom))
            .replace("{x}", str(tx))
            .replace("{y}", str(ty))
        )
        result["xyz_template"] = series["xyz_template"]

    return result


# ── Archives Hub — SRU search ──────────────────────────────────────────────────

ARCHIVES_HUB_SRU = "https://archiveshub.jisc.ac.uk/sru/"


def _parse_sru_xml(xml_text: str) -> dict:
    """Parse an SRU searchRetrieve XML response into a plain dict."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return {"error": f"XML parse error: {exc}", "records": [], "total_results": 0}

    ns = {
        "srw": "http://www.loc.gov/zing/srw/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    }

    total_el = root.find(".//srw:numberOfRecords", ns)
    total = int(total_el.text) if total_el is not None and total_el.text else 0

    records: list[dict] = []
    for rec in root.findall(".//srw:record", ns):
        data_el = rec.find(".//oai_dc:dc", ns)
        if data_el is None:
            continue
        entry: dict[str, object] = {}
        for child in data_el:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            text = child.text or ""
            if tag in entry:
                existing = entry[tag]
                if isinstance(existing, list):
                    existing.append(text)
                else:
                    entry[tag] = [existing, text]
            else:
                entry[tag] = text
        records.append(entry)

    return {"total_results": total, "records": records}


@mcp.tool
async def search_archives_hub(
    query: str,
    scottish_only: bool = True,
    max_results: int = 10,
) -> dict:
    """Search Archives Hub for archive descriptions from Scottish repositories.

    Archives Hub aggregates finding aids from 350+ UK institutions including NRS,
    NLS, Scottish universities, Highland Archive Centre, and local authority archives.

    query: search terms — names, places, topics. Supports CQL operators AND / OR / NOT.
    scottish_only: if True appends 'AND Scotland' to the query to focus on Scottish records.
    max_results: results to return (1–25).

    Returns matching archive descriptions with title, creator, date range, and
    holding institution. Records are free to view; contact the repository for originals.
    """
    max_results = min(max(1, max_results), 25)
    cql = f'({query}) AND "Scotland"' if scottish_only else query

    params = {
        "operation": "searchRetrieve",
        "version": "1.2",
        "query": cql,
        "maximumRecords": str(max_results),
        "startRecord": "1",
        "recordSchema": "dc",
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(ARCHIVES_HUB_SRU, params=params)
            resp.raise_for_status()
        return _parse_sru_xml(resp.text)
    except httpx.HTTPError as exc:
        return {"error": f"Archives Hub request failed: {exc}", "records": [], "total_results": 0}


@mcp.tool
async def get_archives_hub_record(identifier: str) -> dict:
    """Retrieve a specific Archives Hub finding aid by its identifier.

    identifier: the identifier string returned in search_archives_hub results
    (e.g. 'gb234-coll-1234'). Returns the full Dublin Core record.
    """
    params = {
        "operation": "searchRetrieve",
        "version": "1.2",
        "query": f'rec.identifier="{identifier}"',
        "maximumRecords": "1",
        "startRecord": "1",
        "recordSchema": "dc",
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(ARCHIVES_HUB_SRU, params=params)
            resp.raise_for_status()
        return _parse_sru_xml(resp.text)
    except httpx.HTTPError as exc:
        return {"error": f"Archives Hub request failed: {exc}", "records": [], "total_results": 0}


# ── Resources — static guides ──────────────────────────────────────────────────

def _read_guide(filename: str) -> str:
    path = GUIDES_DIR / filename
    if not path.exists():
        return f"Guide not found: {filename}"
    return path.read_text(encoding="utf-8")


@mcp.resource("scotland-archives://guide")
def master_guide() -> str:
    """Overview of all Scottish genealogy archives covered by this MCP server."""
    return _read_guide("overview.md")


@mcp.resource("scotland-archives://record-types")
def record_types_guide() -> str:
    """Comprehensive reference for Scottish genealogy record types, coverage dates, and research tips."""
    return _read_guide("record_types.md")


@mcp.resource("scotland-archives://archives/{name}")
def archive_guide(name: str) -> str:
    """Detailed guide for a specific archive.
    name: scotlandspeople | nls | archives-hub
    """
    return _read_guide(f"{name}.md")


@mcp.resource("scotland-archives://counties")
def counties_resource() -> str:
    """Historical Scottish counties with notes on record coverage and alternative names."""
    return _read_guide("counties.md")


# ── Prompts — research workflows ───────────────────────────────────────────────

@mcp.prompt
def research_ancestor(
    full_name: str,
    approximate_birth_year: str = "",
    county_or_parish: str = "",
    known_facts: str = "",
) -> str:
    """Generate a structured Scottish genealogy research plan for a specific ancestor."""
    return (
        f"You are a Scottish genealogy research assistant with access to ScotlandsPeople, "
        f"NLS historic maps, and Archives Hub.\n\n"
        f"Research subject: {full_name}\n"
        f"Approximate birth year: {approximate_birth_year or 'unknown'}\n"
        f"County / Parish: {county_or_parish or 'unknown'}\n"
        f"Known facts: {known_facts or 'none provided'}\n\n"
        f"Using the available tools, create a step-by-step research plan:\n"
        f"1. Call list_record_types() to identify which records suit the approximate date range.\n"
        f"2. Call search_scotlandspeople() for the most promising record types:\n"
        f"   - Post-1855: start with stat_births / stat_marriages / stat_deaths.\n"
        f"   - Pre-1855: start with opr_births / opr_marriages, then census.\n"
        f"   - Use valuation_rolls to locate the family between census years.\n"
        f"3. If the parish is unknown, call get_nls_map_url(series_id='parish_maps', ...) "
        f"to identify the relevant parish from a rough location.\n"
        f"4. Call search_archives_hub(query='{full_name}') to find any family papers, "
        f"estate records, or institutional collections.\n"
        f"5. Summarise findings and recommend the single most productive next step.\n\n"
        f"Always note which records are free to search vs require a ScotlandsPeople subscription."
    )


@mcp.prompt
def find_church_records(
    parish_name: str,
    denomination: str = "Church of Scotland",
) -> str:
    """Generate a research plan for locating church records in a specific Scottish parish."""
    return (
        f"Help locate church records for {parish_name} parish ({denomination}).\n\n"
        f"Steps:\n"
        f"1. Call search_scotlandspeople(record_type='opr_births', parish='{parish_name}') "
        f"for birth/baptism coverage.\n"
        f"2. Call search_scotlandspeople(record_type='opr_marriages', parish='{parish_name}') "
        f"for marriage/banns records.\n"
        f"3. Call search_scotlandspeople(record_type='opr_deaths', parish='{parish_name}') "
        f"for burial records.\n"
        f"4. If Catholic records may be relevant, call "
        f"search_scotlandspeople(record_type='catholic_registers', parish='{parish_name}').\n"
        f"5. For non-established church members (Free Church, UP, Episcopalian), call "
        f"search_scotlandspeople(record_type='church_records', parish='{parish_name}').\n"
        f"6. Call search_archives_hub(query='{parish_name} parish church') to find original "
        f"Kirk Session minutes, communion rolls, or poor relief records held in repositories.\n"
        f"7. Call get_nls_map_url(series_id='parish_maps', latitude=<lat>, longitude=<lon>) "
        f"to show the parish boundary — useful if the family was near a parish border.\n\n"
        f"Note: OPR coverage varies dramatically by parish. Always check the ScotlandsPeople "
        f"parish catalogue (free) for the exact start date before assuming records are missing."
    )


@mcp.prompt
def trace_emigration(
    ancestor_name: str,
    departure_period: str,
    known_destination: str = "",
) -> str:
    """Generate a research plan for tracing a Scottish emigrant ancestor."""
    destinations_by_period = (
        "Common Scottish emigration destinations by period:\n"
        "- 1750–1850: Nova Scotia, Prince Edward Island, Upper Canada, Carolinas (USA)\n"
        "- 1800–1860: Highland Clearances forced emigration to Cape Breton, Ontario, Australia\n"
        "- 1850–1900: New Zealand, Victoria & Queensland (Australia), USA, Ontario\n"
        "- 1900–1950: Canada, Australia, New Zealand, South Africa"
    )

    return (
        f"Research plan for tracing Scottish emigrant: {ancestor_name}\n"
        f"Departure period: {departure_period}\n"
        f"Known destination: {known_destination or 'unknown'}\n\n"
        f"Steps using available tools:\n"
        f"1. Establish last Scottish address:\n"
        f"   - search_scotlandspeople(record_type='census') for the last census before departure.\n"
        f"   - search_scotlandspeople(record_type='valuation_rolls') to track address year by year.\n"
        f"2. Look for departure context:\n"
        f"   - search_scotlandspeople(record_type='poor_relief') — assisted emigration schemes "
        f"are often documented in Kirk Session or parochial board records.\n"
        f"   - search_archives_hub(query='{ancestor_name} emigration {known_destination}') "
        f"for estate or landlord papers that may document assisted passages.\n"
        f"3. Map the departure area:\n"
        f"   - get_nls_map_url(series_id='os_6inch_1st', ...) to identify the local port or "
        f"estate from which they departed.\n"
        f"4. For records at the destination (outside this MCP's scope):\n"
        f"   - Passenger lists: Findmypast (UK), Ancestry, FamilySearch\n"
        f"   - Destination immigration records vary by country and period\n"
        f"   - Highland & Islands Emigration Society records (1851–1857) at NRS reference HD4\n\n"
        f"{destinations_by_period}"
    )


if __name__ == "__main__":
    mcp.run()
