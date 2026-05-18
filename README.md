# Scotland Archives MCP

A [Model Context Protocol](https://modelcontextprotocol.io/) server for Scottish genealogy research. Provides structured access to ScotlandsPeople, NLS Historic Maps, and Archives Hub — the three primary sources for tracing Scottish ancestors.

## Tools

### ScotlandsPeople

| Tool | Description |
|---|---|
| `list_record_types` | All available record types with date coverage and research tips |
| `search_scotlandspeople` | Build a ScotlandsPeople search URL filtered by record type, surname, forename, year range, county, and parish |
| `list_scottish_counties` | All 33 historical Scottish counties as used in genealogy records |

Supported record types: OPR births/marriages/deaths, statutory registers, census (1841–1921), wills & testaments, valuation rolls, Catholic parish registers, non-established church records, military/soldiers' wills, prison registers, poor relief, coats of arms, divorces.

### NLS Historic Maps

| Tool | Description |
|---|---|
| `list_nls_map_series` | Available historic map series with date coverage |
| `get_nls_map_url` | WMS, XYZ tile, and NLS viewer deep-links for any Scottish location |

Available map series: OS 6-inch 1st edition (1843–1882), OS 6-inch 2nd edition (1892–1905), OS 25-inch/1:2500 (1855–1900), Scottish Parish Boundary Maps, County & Estate Maps (pre-1840), Roy Military Survey (1747–1755).

### Archives Hub

| Tool | Description |
|---|---|
| `search_archives_hub` | Search Archives Hub for archive descriptions from Scottish repositories. Returns a direct search URL and exact search terms to enter — the SRU API is currently blocked by Cloudflare bot protection. |
| `get_archives_hub_record` | Get a direct browser link to a specific finding aid by its identifier |

## Resources

Static research guides served as MCP resources:

| Resource URI | Content |
|---|---|
| `scotland-archives://guide` | Overview of all sources covered |
| `scotland-archives://record-types` | Full reference for all record types |
| `scotland-archives://archives/scotlandspeople` | ScotlandsPeople research guide |
| `scotland-archives://archives/nls` | NLS Historic Maps guide |
| `scotland-archives://archives/archives-hub` | Archives Hub guide |
| `scotland-archives://counties` | Historical Scottish counties reference |

## Prompts

| Prompt | Description |
|---|---|
| `research_ancestor` | Structured research plan for a named ancestor |
| `find_church_records` | Research plan for a specific parish and denomination |
| `trace_emigration` | Plan for tracing a Scottish emigrant ancestor |

## Installation

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/your-username/Scotland-geneology-mcp
cd Scotland-geneology-mcp
uv sync
```

### Add to Claude Code

```bash
claude mcp add scotland-archives -- uv --directory "/path/to/Scotland-geneology-mcp" run fastmcp run src/scotland_archives/server.py
```

### Add to Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "scotland-archives": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/Scotland-geneology-mcp",
        "run", "fastmcp", "run", "src/scotland_archives/server.py"
      ]
    }
  }
}
```

## Development

```bash
uv sync --extra dev
uv run pytest tests/ -v
```

## Sources

- **ScotlandsPeople** — scotlandspeople.gov.uk — official Scottish government genealogy site, operated by National Records of Scotland. Free index search; images require subscription.
- **NLS Historic Maps** — maps.nls.uk — National Library of Scotland georeferenced historic map archive. Entirely free.
- **Archives Hub** — archiveshub.jisc.ac.uk — finding aids from 350+ UK institutions. Free to search; contact repositories for original documents.
