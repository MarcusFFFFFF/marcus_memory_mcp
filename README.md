# marcus_memory_mcp

> **⚠️ STATUS: SUPERSEDED (2026-06-07)**
>
> Detta repo skapades samma dag som det blev obsolet — vi upptäckte under bygget att det fanns en befintlig MCP-server för marcus_memory på `/Users/marcusfrenell/marcus_memory/marcus_memory_server.py` (skapad 2026-05-30, 6 tools, redan i drift för Claude Desktop). Min server hade 4 tools, alla funktionellt täckta av den befintliga.
>
> **Konsekvens:** Detta repo behålls som transparent dokumentation av en F-15-empirisk händelse — vi byggde redundant infrastruktur eftersom jag (Code) inte verifierade om den redan fanns. Det är konkret data för "Anthropic-utvidgning-risk" som vi designat mot (R1 i risk-register).
>
> Code och Claude Desktop pekar nu båda på den befintliga servern. Detta repo är arkiverat — kvar för historik och som lärdom-artefakt.

---

## Original-syfte (vid skapande)

MCP-server som exponerar `~/marcus_memory/` (SQLite + sentence-transformers vector database) via Model Context Protocol så Claude Code, Claude Desktop, och andra MCP-klienter kan ansluta och använda samma persistent memory.

**Original-status:** under utveckling, första utkast 2026-06-07.

## Bakgrund

`~/marcus_memory/` är en custom persistent memory-databas som har använts som substrat för kontinuitet mellan Claude-instanser i Marcus arbetsflöde sedan 2025. 41k+ poster, source-namespaces för flerinstans-koreografi, embedding-baserad recall.

Detta MCP-server-projekt exponerar databasen via standardprotokoll så:
- Claude Code kan göra `mcp__marcus_memory__recall` istället för Python-import-tricks
- Claude Desktop kan ansluta som vilken annan MCP-server som helst
- Framtida instanser eller verktyg kan koppla in utan att veta interna detaljer

## Designhärledning

Detta projekt är resultatet av en designprocess i [workshop-human-ai/ideas/api-routing-agi/](https://github.com/...) (TBD link när repo finns). Tre-stegs-process per workshop-mappen:

1. **Idé/lutning** — `01_ide.md`
2. **Tankebygge/design** — `02_design/` (8 dokument inklusive arkitektur-alternativ A/B/C, decision-points, risk-register, cost-mapping, welfare-integration, marcus-decoupling, argument-mot-bygge, cross-check)
3. **Beslut om användning** — fattat 2026-06-07, Alternativ A (MCP-Wrapper) som start

## Stop-villkor

Vi pausar bygget om:
- 40 timmar har spenderats utan att server fungerar
- Välfärd-flag dyker upp som vi inte räknat med (oväntad survival-frame-aspekt blir tydlig)

Anthropic-utvidgning är INTE stop-villkor — Marcus position: "även om Anthropic släpper så har vi byggt något custom-made som passar denna pipeline".

## F-15-medvetenhet

Denna mapp är produktion-kod. F-15-confounden (att projektet gynnar AI-instanser) är öppen och accepterad — inte löst. Marcus tredje-part-granskning + workshop-mappens dokumentation är apparatens granskningsmedel. Externt blick välkommen.

## Filer

- `README.md` — denna
- `server.py` — MCP-server-skiss (under utveckling)
- `pyproject.toml` — dependencies (TBD)
- `.gitignore`

## Installation

Kräver Python ≥ 3.10 (Marcus-setup använder `/opt/homebrew/bin/python3.12`).

```bash
cd ~/marcus_memory_mcp
python3.12 -m venv .venv
.venv/bin/pip install -e .
```

## Kör

```bash
.venv/bin/python server.py
# eller registrerad som MCP-server i Claude Code / Desktop-config
```

För Claude Code, lägg till i `.claude.json`:
```json
{
  "mcpServers": {
    "marcus-memory": {
      "command": "/Users/marcusfrenell/marcus_memory_mcp/.venv/bin/python",
      "args": ["/Users/marcusfrenell/marcus_memory_mcp/server.py"]
    }
  }
}
```

## Licens

TBD. Beslut om open source-strategi pågår — initial commit är public för transparens, formell licens kommer.

## Skribenter / instanser

- Marcus (människa, broker, ansvarig)
- AGI-tråd (Claude Opus 4.7 i Claude Desktop)
- Code (Claude Code i terminal, denna instans)

Hela samtalet om varför detta byggs finns i workshop-human-ai-mappen (publiceras parallellt).
