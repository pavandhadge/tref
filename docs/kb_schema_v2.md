# tref KB Schema v2.0

All KB Markdown files must follow this schema. The indexer enforces it strictly.

## Required Frontmatter
- `library` (str)
- `version` (str)
- `category` (str)
- `item` (str)
- `type` (str: `command|method|function|concept`)
- `signature` (str)
- `keywords` (list[str])
- `aliases` (optional list[str])
- `intent` (str, one-line user intent)
- `last_updated` (str, ISO date)
- `schema_version` (must be `"2.0"`)
- `source_url` (https URL to original documentation)
- `source_title` (str)
- `alternatives` (list[object], each object has `option` + `reason`)

## Required `##` Sections
1. `Signature`
2. `What It Does`
3. `Use When`
4. `Examples`
5. `Alternatives`
6. `Gotchas / Version Notes`
7. `References`

## Notes
- `alternatives` frontmatter is the source of truth for machine-readable options/reasons.
- `Alternatives` section should remain human-readable and consistent with frontmatter.
- `References` should contain authoritative links.
- Keep examples executable and version-correct.
