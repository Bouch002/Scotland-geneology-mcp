"""Tests for Scotland Archives MCP server tools."""

import pytest
import respx
import httpx

from scotland_archives.server import (
    list_record_types,
    search_scotlandspeople,
    list_scottish_counties,
    list_nls_map_series,
    get_nls_map_url,
    search_archives_hub,
    get_archives_hub_record,
    RECORD_TYPES,
    NLS_MAP_SERIES,
    ARCHIVES_HUB_SRU,
)


# ── list_record_types ──────────────────────────────────────────────────────────

def test_list_record_types_returns_all():
    result = list_record_types()
    assert len(result) == len(RECORD_TYPES)


def test_list_record_types_structure():
    result = list_record_types()
    for item in result:
        assert "id" in item
        assert "label" in item
        assert "coverage" in item
        assert "tip" in item


# ── search_scotlandspeople ─────────────────────────────────────────────────────

def test_search_scotlandspeople_valid_type():
    result = search_scotlandspeople(
        record_type="opr_births",
        surname="MacDonald",
        forename="John",
        year_from=1800,
        year_to=1854,
        county="Inverness-shire",
    )
    assert "url" in result
    assert "scotlandspeople.gov.uk" in result["url"]
    assert "MACDONALD" in result["url"]
    assert "1800" in result["url"]
    assert "tip" in result
    assert "subscription_note" in result


def test_search_scotlandspeople_unknown_type():
    result = search_scotlandspeople(record_type="unknown_type")
    assert "error" in result


def test_search_scotlandspeople_no_filters():
    result = search_scotlandspeople(record_type="census")
    assert "url" in result
    assert "error" not in result


def test_search_scotlandspeople_surname_uppercased():
    result = search_scotlandspeople(record_type="stat_births", surname="smith")
    assert "SMITH" in result["url"]


def test_search_scotlandspeople_all_record_types_valid():
    for record_type in RECORD_TYPES:
        result = search_scotlandspeople(record_type=record_type)
        assert "error" not in result, f"Unexpected error for record_type={record_type}"
        assert "url" in result


# ── list_scottish_counties ─────────────────────────────────────────────────────

def test_list_scottish_counties_returns_list():
    result = list_scottish_counties()
    assert isinstance(result, list)
    assert len(result) == 33


def test_list_scottish_counties_includes_key_counties():
    result = list_scottish_counties()
    joined = " ".join(result)
    assert "Lanarkshire" in joined
    assert "Inverness" in joined
    assert "Shetland" in joined


# ── list_nls_map_series ────────────────────────────────────────────────────────

def test_list_nls_map_series_returns_all():
    result = list_nls_map_series()
    assert len(result) == len(NLS_MAP_SERIES)


def test_list_nls_map_series_structure():
    result = list_nls_map_series()
    for item in result:
        assert "id" in item
        assert "name" in item
        assert "description" in item
        assert "min_zoom" in item
        assert "max_zoom" in item
        assert "has_xyz_tiles" in item


# ── get_nls_map_url ────────────────────────────────────────────────────────────

def test_get_nls_map_url_valid():
    # Inverness: approx 57.48°N, -4.22°E
    result = get_nls_map_url(
        series_id="os_6inch_1st",
        latitude=57.48,
        longitude=-4.22,
        zoom=13,
    )
    assert "url" not in result or "error" not in result
    assert "wms_get_map" in result
    assert "nls_overlay_url" in result
    assert "nls_sheet_finder_url" in result
    assert "xyz_tile_url" in result
    assert "maps.nls.uk" in result["nls_overlay_url"]


def test_get_nls_map_url_unknown_series():
    result = get_nls_map_url(series_id="nonexistent", latitude=57.0, longitude=-4.0)
    assert "error" in result


def test_get_nls_map_url_zoom_clamped():
    # Request zoom=99, should be clamped to series max
    result = get_nls_map_url(
        series_id="os_6inch_1st",
        latitude=56.0,
        longitude=-3.5,
        zoom=99,
    )
    assert result["zoom"] <= NLS_MAP_SERIES["os_6inch_1st"]["max_zoom"]


def test_get_nls_map_url_county_maps_no_xyz():
    # county_maps has no XYZ tiles
    result = get_nls_map_url(
        series_id="county_maps",
        latitude=57.0,
        longitude=-4.0,
    )
    assert "xyz_tile_url" not in result
    assert "wms_get_map" in result


# ── search_archives_hub ────────────────────────────────────────────────────────

SRU_RESPONSE_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<searchRetrieveResponse xmlns="http://www.loc.gov/zing/srw/">
  <numberOfRecords>1</numberOfRecords>
  <records>
    <record>
      <recordData>
        <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                   xmlns:dc="http://purl.org/dc/elements/1.1/">
          <dc:title>Papers of the Mackenzie Family of Seaforth</dc:title>
          <dc:creator>Mackenzie family</dc:creator>
          <dc:date>1650–1900</dc:date>
          <dc:description>Estate and family papers from Ross and Cromarty, Scotland.</dc:description>
          <dc:identifier>gb234-seaforth-001</dc:identifier>
        </oai_dc:dc>
      </recordData>
    </record>
  </records>
</searchRetrieveResponse>
"""


@pytest.mark.asyncio
@respx.mock
async def test_search_archives_hub_success():
    respx.get(ARCHIVES_HUB_SRU).mock(
        return_value=httpx.Response(200, text=SRU_RESPONSE_XML)
    )
    result = await search_archives_hub(query="Mackenzie Seaforth")
    assert result["total_results"] == 1
    assert len(result["records"]) == 1
    assert result["records"][0]["title"] == "Papers of the Mackenzie Family of Seaforth"
    assert "archiveshub.jisc.ac.uk/search/" in result["search_url"]
    assert "Mackenzie Seaforth" in result["search_terms"]


@pytest.mark.asyncio
@respx.mock
async def test_search_archives_hub_cloudflare_blocked():
    respx.get(ARCHIVES_HUB_SRU).mock(return_value=httpx.Response(403, text="Forbidden"))
    result = await search_archives_hub(query="anything")
    assert "archiveshub.jisc.ac.uk/search/" in result["search_url"]
    assert "browser_instructions" in result
    assert "anything" in result["search_terms"]
    assert result["records"] == []


@pytest.mark.asyncio
@respx.mock
async def test_search_archives_hub_network_error():
    respx.get(ARCHIVES_HUB_SRU).mock(side_effect=httpx.ConnectError("Connection refused"))
    result = await search_archives_hub(query="anything")
    assert "error" in result
    assert "archiveshub.jisc.ac.uk/search/" in result["search_url"]
    assert "browser_instructions" in result
    assert result["records"] == []


@pytest.mark.asyncio
@respx.mock
async def test_search_archives_hub_max_results_capped():
    respx.get(ARCHIVES_HUB_SRU).mock(
        return_value=httpx.Response(200, text=SRU_RESPONSE_XML)
    )
    result = await search_archives_hub(query="test", max_results=999)
    call = respx.calls[0]
    assert "maximumRecords=25" in str(call.request.url)


@pytest.mark.asyncio
@respx.mock
async def test_search_archives_hub_scottish_filter_appended():
    respx.get(ARCHIVES_HUB_SRU).mock(
        return_value=httpx.Response(200, text=SRU_RESPONSE_XML)
    )
    await search_archives_hub(query="Campbell", scottish_only=True)
    call = respx.calls[0]
    assert "Scotland" in str(call.request.url)


def test_get_archives_hub_record():
    result = get_archives_hub_record("gb234-seaforth-001")
    assert "record_url" in result
    assert "gb234-seaforth-001" in result["record_url"]
    assert "archiveshub.jisc.ac.uk" in result["record_url"]
