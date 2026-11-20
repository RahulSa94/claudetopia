---
name: creative-intelligence
description: Free ad creative analysis for any business. Gives Scale/Iterate/Fix-Pause/Test verdicts, a video hook and hold diagnosis, hook-type patterns and next creative briefs from Meta and Google Ads data, using only free MCPs (Meta Ads MCP, Google Ads MCP, Google Workspace) or CSV exports. Also plans a personal upskill roadmap. Use for creative analysis, which ads to scale or pause, video hook rate, creative fatigue, ad creative briefs, or learning paid-media creative strategy.
license: MIT
---

# Creative Intelligence

A brand-neutral system that does two jobs for anyone who runs paid ads:
1. **Analyse.** Tells them which creatives to scale, iterate, fix or pause, which video hooks worked, and what to build next.
2. **Upskill.** Plans and tracks a learning journey, using their own account as the classroom, so the person gets better at creative strategy with every run.

It works for any industry, account size and skill level, and **costs nothing to run for anyone**. It uses only free connectors or free file exports. Every business-specific rule lives in that user's **profile**, never in this skill.

## Modes: pick from the request

| User says | Mode |
|---|---|
| "set up creative intelligence", first ever run, no profile found | **Setup** |
| "run creative analysis", "which ads to scale", scheduled run | **Run** |
| "plan my upskill journey", "what should I learn", "roadmap" | **Roadmap** |
| "how am I progressing", "my level" | **Progress** |
| "set this up for my team" | **Team** |

If no profile exists for a Run, Roadmap or Progress request, do Setup first.

---

## Free-tools-only rule (applies in every mode)

**Use only these. Never use a paid connector, even if one is connected.**

| Job | Free tool | Notes |
|---|---|---|
| Meta data | **Meta's official Ads MCP** (`https://mcp.facebook.com/ads`, sign in with Facebook Business) | Free during Meta's open beta. Use **read/reporting tools only**. It can also edit ads, which this skill never does. |
| Google data | **Google's official Google Ads MCP** (`github.com/googleads/google-ads-mcp`, open source) | Free and read-only. Runs on the user's own computer. |
| Any platform, no setup | **CSV / XLSX export** from Ads Manager or Google Ads, uploaded to the chat | Always free. This is the fallback for everyone. |
| Log, report storage | Google Sheets / Google Drive connector | Free with a Google account |
| Alert | Gmail connector, to the user's own address | Free |
| No Google account | Report and log sent as files in the conversation | Free |

Never:
- Use paid reporting connectors or aggregators.
- Send WhatsApp or SMS, because business-initiated messages are charged.
- Create, edit, pause or boost anything in an ad account.
- Call paid APIs, scrapers or outside AI services.

Cost re-check: at Setup and on the first run of every month, confirm each connector is still free. Meta's MCP is free *during open beta*. If one starts charging, switch that platform to CSV export and tell the user.

If a step can only be done with a paid action, skip it and write "skipped: would incur cost".

---

## Setup mode: build the profile

Ask in one short round, with multiple choice where possible. Store the answers in a **Profile** tab of the user's Creative Intelligence Log sheet, created via the Google Drive connector. Without Drive, write `creative-intelligence-profile.md` and send it to the user to keep and re-upload next time.

1. **Business.** Name and industry (real estate, e-commerce, education, healthcare, B2B/SaaS, local services, finance, other).
2. **Projects, brands or product lines.** Each is analysed on its own.
3. **Platforms.** Meta, Google, or both.
4. **Data route per platform.** Free MCP (if not connected, offer the 2-minute Meta connect or the Google setup steps) or CSV upload.
5. **Account rules.** Accounts to always include, and accounts never to pull.
6. **Primary KPI.** CPL, CPA, ROAS, or cost per qualified lead, with a target per project (or "use account median").
7. **Quality data.** Is there a CRM, and at what level are leads tagged (ad, campaign or project)? Use it only if it can be read for free (a connected CRM tool or an export).
8. **Delivery.** Report format (Word, Sheet or in chat), email alert or none, and cadence (on demand, or a weekly day and time).
9. **Comparison policy.** May projects be compared with each other? (Default: no.)
10. **Skill check.** The 6 placement questions in Roadmap mode.

Confirm the profile back in a short table and save it.

**Setup help for the free connectors:**
- *Meta:* in Claude, go to Settings → Connectors → add custom connector, enter the URL `https://mcp.facebook.com/ads`, and sign in with Facebook Business. Some accounts aren't enabled during the beta; if so, use CSV.
- *Google:* the official server runs locally (Claude desktop app or Claude Code). It needs a Google Cloud project with the Google Ads API enabled and OAuth sign-in; follow the repo README. If that's too much, use CSV.
- *CSV:* in Ads Manager, go to Reports, choose an ad-level breakdown with the fields in Run step 2, and export. In Google Ads, go to Ads & assets → Download.

**Example profile (fictional):** Lakeview Homes; real estate; projects Riverside, Hilltop, Garden Court; Meta via Meta Ads MCP (read only), Google via CSV; KPI is CPL against each project's target; CRM tags leads at project level; landscape Word report, project first, no cross-project comparison; weekly email alert on Mondays.

---

## Run mode: the analysis pipeline

Create a run ID `CI-YYYY-MM-DD` and a task list for steps 1–8.

### 1. Pre-flight
Load the profile. Check each data route answers: the MCP responds, or the CSV is uploaded and has the needed columns. Build the account list from accounts with live spend only, minus excluded accounts. Load targets, confirmed hook tags and last run's verdicts from the log. Record any gap; stop only if no data route works.

### 2. Pull
Default periods: the last 7 complete days for verdicts, 30 days for patterns, and 90 days for the hook and hold baseline.

**Meta (Meta Ads MCP reporting/insights tools, or CSV):** pull at ad level, always segmented by the ad set's optimisation goal. Needed fields:
- ad name, ad ID, optimisation goal
- impressions, reach, frequency, CPM, spend
- 3-second video plays, ThruPlays, and 25/50/75/100% video plays
- link clicks, link CTR, landing page views
- leads (form and website), plus purchases and purchase value for e-commerce
- the ad's thumbnail or preview, where the tool provides it

Pull a weekly breakdown of impressions and link clicks for fatigue. Request large reports in parts if a call times out.

**Google (Google Ads MCP search/GAQL tool, or CSV):** always segment by campaign channel type, and only query channel types that actually spent. What to pull per type:
- Search: ad-level metrics plus headline and description assets.
- Performance Max: asset-group metrics plus a metric-less asset list.
- Demand Gen and Video: view rate and the 25/50/75/100% quartile rates.
- Display: responsive display ad fields with metrics.

Ignore Ad Strength as a performance signal.

**CSV:** map columns to the fields above and list which are missing. Analyse what is present and say what couldn't be judged.

Pull each dataset once, and ask for enough rows that nothing is cut off.

### 3. Validate (dependability gate)
- Ad-level spend is within 2% of account- or campaign-level spend for the same dates.
- No result is cut off at a row limit. If the row count equals the limit, re-pull in parts.
- Every row has its goal or channel type.
- Media coverage % is reported.

Re-pull a failing account once. If it still fails, mark it "not judged" and never show its numbers as verdicts.

### 4. Verdicts (inside each goal or channel, never across them)
Anchor on the profile's KPI against its target. If there is no target, use the goal median and say so.

| Verdict | Rule | Action |
|---|---|---|
| **Test** | Spend < 2× target cost, or < 1,000 impressions | Keep running; too early to judge |
| **Scale** | KPI ≤ 80% of target (or ROAS ≥ 120% of target), ≥ 5 results, frequency < 3.5 on cold audiences, no fatigue | Raise budget 20–30% every 3–4 days, or move to the scaling ad set |
| **Iterate** | KPI 80–120% of target, or good KPI with fatigue starting, or step 5 finds one broken part | Keep live and brief a variant that changes one thing |
| **Fix-Pause** | KPI > 150% of target after spending ≥ 2× target, or 0 results after 2× target, or severe fatigue (link CTR down > 40% vs the first 7 days, with frequency > 5) | Pause, or first fix the named non-creative problem |

Safety checks:
- The top spender or top result source in a goal gets "Review before pausing", not a flat pause.
- If landing page views ÷ link clicks is below 65%, it's a landing page problem, not a creative one.
- Never invent creative-level quality data when the CRM only tags leads at campaign or project level.
- Verdicts are recommendations; the user makes the change in Ads Manager themselves.

### 5. Video hook & hold diagnosis
- Hook Rate = 3-sec plays ÷ impressions.
- Hold Rate = ThruPlays ÷ 3-sec plays.
- Google proxy: Hook ≈ 25% quartile rate, and Hold ≈ 75% quartile rate ÷ 25% quartile rate.

Judge each video against the account's own 90-day baseline per goal: good is at least 20% above it, poor at least 20% below. Use fallback benchmarks only when there is no baseline: hook under 20% is weak, 25–30% average, over 30% strong.

| Scenario | Signal | Fix |
|---|---|---|
| 1 | Good hook, poor hold | Keep the hook, recut the body, show the payoff sooner |
| 2 | Poor hook, good hold/CTR/KPI | Swap only the first 3 seconds; the highest-value iteration |
| 3 | Good hook and hold, poor CTR/KPI | Fix the CTA, offer or end card |
| 4 | Poor hook and poor hold | The concept fails: Fix-Pause |
| 5 | All average | Try a new angle, not a variant |

### 6. Hook-type tagging and patterns
Tag each creative's opening with one hook type from the industry pack, plus its format, language and video length band. Use the ad name first, otherwise the thumbnail or preview. New tags stay "unconfirmed" until the user confirms them.

Group by hook type within each project and goal: number of ads, spend, weighted hook rate, hold rate, CTR and KPI. Call it a **pattern** only with ≥ 3 ads, meaningful spend and confirmed tags; otherwise call it an "early signal".

**Industry hook packs** (extend in the profile as needed):
- *Universal:* price/offer · problem/question · face to camera/testimonial · social proof/numbers · scarcity/urgency · before-after/transformation · demo/how it works
- *Real estate:* location/connectivity · lifestyle/amenity · walkthrough/interior · construction progress/trust · payment plan
- *E-commerce:* unboxing · product in use · UGC review · comparison · bundle/discount
- *Education:* outcome/career · student story · faculty/expert · free class/demo
- *B2B/SaaS:* pain stat · product screen · customer logo/result · founder POV
- *Healthcare/local services:* doctor/expert · patient story · facility tour · offer/booking

### 7. Build next
Write 3–5 ranked briefs per project. Each brief states what to build, the hook type, the angle, format/length/language, the existing ad it builds on, and the metric to beat.

Order them:
1. Scenario 2 videos first.
2. Then extend winning hook types to new formats or languages.
3. Retire hook types that lost across ≥ 3 ads.
4. Include one genuinely new angle.

Check every brief against the learnings saved in the profile.

### 8. Deliver and learn
- **Report.** Use the profile's format, ordered project → platform → goal. Each goal section has a verdict table (with the change since last run), the video diagnosis, hook patterns and build-next briefs. The front page shows the run ID, period, data routes used, accounts, data gaps, top 5 actions and **this week's skill** (from Roadmap mode).
- **Log.** Append to the log tabs `Runs`, `Verdicts`, `Hook Tags`, `Patterns` and `Briefs`, stamping each row with the run ID and date. Never overwrite or delete rows. Without Google Sheets, append to a log file and send it back.
- **Alert.** If the profile asks for it, email the user's own address via Gmail.
- **Learning.** A hook type that wins 3 runs in a row for a project becomes an established learning in the profile.
- **Final check.** Open the report, re-total spend against the validated totals, and confirm the log rows and the alert. Confirm that no paid tool was used and nothing was changed in an ad account.

---

## Roadmap mode: the upskill journey

The roadmap teaches creative strategy by doing it on the user's own account. Each level unlocks more of the Run pipeline, so automation grows with understanding instead of replacing it.

### Levels

| Level | Name | Can do | Pipeline unlocked |
|---|---|---|---|
| 1 | Reader | Reads CPM, CTR, CPL/CPA and frequency correctly; knows why different goals aren't compared | Verdict table only, with a plain-language note on every metric |
| 2 | Diagnoser | Uses the funnel (volume → interaction → intent → conversion → quality) to find where a creative breaks; reads hook and hold rate | Adds the video diagnosis scenarios |
| 3 | Strategist | Tags hooks, reads patterns, writes one-variable briefs, protects winners | Adds hook patterns and build-next briefs |
| 4 | Operator | Connects the free MCPs, runs a weekly cadence, validates data, keeps a dated log | Adds scheduled runs, the validation gate and the log |
| 5 | Coach | Sets up profiles for other people or accounts, reviews their verdicts, adds industry hook packs | Adds Team mode |

Levels 1–3 work fully with CSV uploads, so nobody needs any connector to start.

### Placement (6 questions, in Setup or on request)
1. What does a rising CPM with stable CTR usually mean?
2. Why shouldn't you compare a lead-form ad with a traffic ad?
3. Hook rate is 15%, hold rate 60% and CPL good. What would you change?
4. When is a creative "fatigued" rather than "the audience is saturated"?
5. How many ads do you need before calling a hook type a pattern?
6. What do you check before trusting a report's numbers?

Score 1 point per correct answer. Starting level: 0–1 points is Level 1, 2–3 is Level 2, 4–5 is Level 3, 6 is Level 4. Explain the answers after scoring.

### The roadmap output
When asked for a roadmap, produce an **8-week plan** starting from the user's current level, one row per week:

| Week | Concept | Exercise on your own account (≤ 30 min) | Checkpoint (how you know you've got it) | Unlocks |
|---|---|---|---|---|

Rules:
- Tie every exercise to the user's real data where available, e.g. "you have 4 Scenario 2 videos: write a new-hook brief for one".
- Teach one concept per week, and make each checkpoint observable: a correct verdict, a brief that gets made, a pattern confirmed.
- Move up a level once that level's checkpoints are passed, not after a fixed time.
- Use free learning only: the user's own data, Meta Blueprint and Google Skillshop (both free), platform help centres, and this skill's explanations.

Save the plan to a `Learning` tab with columns person, week, concept, exercise, checkpoint, status and date. Deliver it as a document if the user wants to keep or share it.

### Weekly skill in every Run
Each Run report includes one **"This week's skill"** box with three parts: the concept from the user's roadmap that this week's data best illustrates, one example from their own creatives, and one 15-minute exercise. Mark it done in `Learning` when the user completes it.

## Progress mode
Read `Learning` and `Runs`, and show the current level, checkpoints passed, run streak and the next unlock. Re-run placement if the user asks to be re-levelled.

## Team mode
Use one log sheet per business and one set of `Learning` rows per person. For each teammate, run placement, give them their own 8-week roadmap, and show their skill box in Run reports. Coaches (Level 5) see a summary of everyone's level and next checkpoint. The profile, account rules and free-tools-only rule are shared across the team; skill levels are personal.
