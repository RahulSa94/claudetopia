# claudetopia

Free, practical Claude skills and plugins. Install them in Claude (web, desktop, mobile), Claude Code, or any agent that reads `SKILL.md`.

## Skills

| Skill | What it does | Cost |
|---|---|---|
| [**Creative Intelligence**](plugins/creative-intelligence/) | Ad creative analysis for Meta and Google Ads: Scale/Iterate/Fix-Pause/Test verdicts, video hook and hold diagnosis, hook-type patterns, next creative briefs, and a personal upskill roadmap | Free (uses only free MCPs or CSV exports) |

## Install everything (Claude Code)

```
/plugin marketplace add RahulSa94/claudetopia
```
Then `/plugin install <name>@claudetopia`.

## Install one skill

- **Claude app:** download the skill's zip from its folder (e.g. [`plugins/creative-intelligence/creative-intelligence.zip`](plugins/creative-intelligence/creative-intelligence.zip)), then go to **Settings → Capabilities → Skills → Upload skill**.
- **Skills CLI:** `npx skills add RahulSa94/claudetopia --skill <name>`

## License

MIT
