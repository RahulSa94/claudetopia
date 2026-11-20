# Creative Intelligence: free ad creative analysis + upskill roadmap for Claude

**Know which Meta and Google ads to scale, fix or pause, which video hooks worked, and what to make next, for free.**

Creative Intelligence is a Claude skill for anyone who runs paid ads: marketers, founders, agencies, students. Give it your ad data and it returns:

- **A verdict for every creative**: Scale · Iterate · Fix-Pause · Test, judged on your own KPI target (CPL, CPA or ROAS).
- **A video hook diagnosis**: hook rate and hold rate against your account's own baseline, sorted into 5 scenarios with the fix for each.
- **Hook-type patterns**: which kinds of openings (price, testimonial, demo, location…) win in your account.
- **Next creative briefs**: 3–5 ranked ideas to brief your designer or agency, each building on a real ad.
- **A personal upskill roadmap**: 5 levels from Reader to Coach, an 8-week plan, and a "this week's skill" lesson in every report, all taught on your own ads.

## Costs nothing

| Data | Free route |
|---|---|
| Meta / Facebook / Instagram ads | Meta's official Ads MCP (`https://mcp.facebook.com/ads`), free during open beta, or a CSV export |
| Google Ads | Google's official open-source [Google Ads MCP](https://github.com/googleads/google-ads-mcp), or a CSV export |
| Reports, log, alerts | Google Sheets / Drive / Gmail connectors, or plain files in the chat |

The skill is **read-only**: it never edits, pauses or boosts anything in your ad accounts, never uses paid connectors, and never sends paid WhatsApp/SMS messages. No connector? Upload a CSV export; levels 1–3 of the roadmap work fully that way.

## Install

**Claude (web, desktop, mobile)**
1. Download [`creative-intelligence.zip`](creative-intelligence.zip).
2. In Claude, go to **Settings → Capabilities → Skills → Upload skill** and choose the zip.
3. Say: *"Set up creative intelligence."*

**Claude Code: plugin marketplace**
```
/plugin marketplace add RahulSa94/claudetopia
/plugin install creative-intelligence@claudetopia
```

**Claude Code / other agents: skills CLI**
```
npx skills add RahulSa94/claudetopia --skill creative-intelligence
```

**Manual:** copy `skills/creative-intelligence/` into `~/.claude/skills/`.

## Try it

- "Set up creative intelligence for my business."
- "Run creative analysis for last week." (with Meta Ads MCP connected, or a CSV attached)
- "Which of my Meta ads should I scale?"
- "Why is this video's hook rate low, and what should I change?"
- "Plan my upskill journey for ad creative strategy."
- "Set this up for my team of 4."

## How a run works

1. **Pre-flight**: loads your profile, checks the data source, removes excluded accounts.
2. **Pull**: Meta by optimisation goal, Google by campaign type; never mixed.
3. **Validate**: spend must reconcile within 2%; anything that fails is marked "not judged", never guessed.
4. **Verdicts**: Scale / Iterate / Fix-Pause / Test against your target, with safety checks for top performers.
5. **Hook & hold diagnosis**: 5 scenarios, e.g. "poor hook, good hold → swap only the first 3 seconds".
6. **Hook patterns**: tagged by industry hook pack; called a pattern only with ≥ 3 ads.
7. **Build next**: ranked briefs.
8. **Deliver & learn**: report, dated log (never overwritten), optional email, learnings saved for next run.

## Industries covered

Universal hook pack plus packs for real estate, e-commerce, education, B2B/SaaS, healthcare and local services. Add your own in your profile.

## License

MIT. Use it, fork it, improve it. Issues and pull requests welcome.
