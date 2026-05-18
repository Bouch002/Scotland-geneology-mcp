# Scotland Archives MCP — Claude Code Guide

## Project overview

FastMCP server for Scottish genealogy research. Wraps three public sources:
- **ScotlandsPeople** — URL builder only (no public API; generates search links)
- **NLS Historic Maps** — WMS/XYZ tile URL builder (no auth required)
- **Archives Hub** — SRU API attempted first; falls back to browser search URL + instructions when Cloudflare blocks (which it always does in practice)

## Commands

```bash
# Install all dependencies including dev tools
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Run the MCP server locally (for testing with Claude)
uv run fastmcp run src/scotland_archives/server.py
```

## Architecture

```
src/scotland_archives/
    server.py        # All tools, resources, and prompts — single file
    guides/          # Static markdown files served as MCP resources
        overview.md
        record_types.md
        scotlandspeople.md
        nls.md
        archives-hub.md
        counties.md
tests/
    test_server.py   # All tests — 21 tests, no fixtures file needed
```

## Key implementation details

**SSL on Windows** — `truststore.inject_into_ssl()` is called at module level (top of `server.py`). This patches Python's SSL to use the Windows system certificate store. Do not replace this with `certifi` — certifi's CA bundle does not include the Archives Hub issuer certificate.

**ScotlandsPeople URLs** — The site uses `/search-records/<category>/<type>` paths. Query parameters (`surname=`, `county=`, `parish=`, etc.) are appended with `?` not `&` — the paths contain no existing query string. Surname is always uppercased in the URL.

**Archives Hub** — The SRU endpoint (`archiveshub.jisc.ac.uk/sru/`) returns HTTP 403 from Cloudflare for all automated requests. The tool handles this gracefully: always returns `search_url`, `search_terms`, and `browser_instructions` so the user can run the search manually. Do not attempt to work around Cloudflare.

**Async tools** — `search_archives_hub` is async (makes an HTTP request). `get_archives_hub_record` is sync (URL generation only). All other tools are sync.

## Adding a new record type

In `server.py`, add an entry to the `RECORD_TYPES` dict:

```python
"my_type": {
    "label": "Human-readable name",
    "coverage": "date range string",
    "search_path": "/search-records/<category>/<slug>",
    "tip": "Research guidance for this record type.",
},
```

Verify the `search_path` by browsing to `scotlandspeople.gov.uk/search-records` and copying the URL of the relevant record type page.

## Adding a new NLS map series

Add an entry to `NLS_MAP_SERIES` in `server.py`. Set `xyz_template` to `None` if the series has no XYZ tile service (as with `county_maps`). The `nls_viewer_layer` value is the numeric layer ID visible in NLS viewer URLs (`layers=NNN`).

## Testing

Tests use `respx` to mock `httpx` calls — no real network requests in the test suite. The Archives Hub tests mock the SRU endpoint directly; SSL and Cloudflare behaviour is not tested (handled at runtime by `truststore`).

Run a specific test:
```bash
uv run pytest tests/test_server.py::test_search_scotlandspeople_valid_type -v
```

## Known limitations

- **ScotlandsPeople** has no public API — all tools generate search URLs only. Users need a ScotlandsPeople account to view full records and images.
- **Archives Hub SRU** is blocked by Cloudflare. The tool always falls back to browser instructions.
- **NLS WMS** tiles are free and public but can be slow at high zoom levels.
