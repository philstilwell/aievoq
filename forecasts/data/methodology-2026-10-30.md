# AIEVOQ forecast register

The October 30, 2026 register is a workshop draft for the Q4 issue. It is public, dated, and not a finalized issue forecast. Probabilities are provisional editorial judgments, not fitted estimates or personal predictions attributed to Phil. The outcome window is not the date of creation.

Preserve this file and every dated register. At finalization, publish a new version with a real `locked_at` date, source cutoff, original wording, probability, resolution rules and reference to the previous draft. Finalization must precede the forecast window; never backdate it. If that deadline is missed, create a later-window forecast instead. Announce withdrawals and replacements; do not quietly remove a candidate that has become inconvenient.

Each forecast has a stable ID, horizon, topic, claim, probability, baseline, rationale, contrary case, outcome window, evidence cutoff and resolution rule. Records distinguish a forecast of a public disclosure from a forecast of independently verified capability. Baselines retain observation and release dates. Draft 0.28 does not refresh the underlying statistics.

## Resolution

- Resolve only locked issue forecasts in the official scorecard. Keep the October 27 E-01–E-03 pilot cohort separate, with its original wording and no retrospectively assigned probability.
- Save an outcome record citing the dated evidence, actual observation, reviewer, verdict and reason. Outcomes are `yes`, `no`, `pending` or `unresolvable`; missing data never means no. For measurable statistics, preserve the source version used at review and any later corrections separately. Only publications dated on or before the cutoff qualify. For a live measure with a revision window, follow the forecast's stated capture rule. A late review does not extend the cutoff.
- A changed population, question, measurement definition, discontinued measure or unusable comparable period makes the affected forecast unresolvable unless its original rule explicitly handles that change. A survey threshold concerns the published point estimate, not a statistically established population increase. Record uncertainty beside it.
- Agent forecasts count providers, not documents; Google and DeepMind count as one. Repeated claims do not count twice. The rule is about eligible dated public reports, not proof that the underlying improvement works.
- For revenue, use the named release's same-quarter prior-year comparable, in reported currency. Acquisitions do not automatically invalidate total company revenue; disclose them and avoid organic-growth or AI-causation claims. If any of the three annual watchlist comparables is missing or incompatible at cutoff, mark that whole forecast unresolvable, even if a partial outcome looks favorable.
- December 2027 Statcounter data must be captured after its 45-day revision window, with a review by March 31, 2028. Retain platform, geography, denominator and definitions. This forecast concerns the share of tracked identifiable chatbot-sent website visits, not users, queries or absolute visit volume.

## Recurring scorecard

Show cohort and review date, locked/open/resolved/unresolvable counts, hits and misses, hit-rate numerator and denominator, mean binary Brier error and number scored. Report quarter and annual horizons separately. Count each original locked forecast once. Related forecasts share a topic and may be correlated; they are not independent experiments. Do not compare raw quarterly averages as evidence of improving skill when event difficulty or composition changes.

A hit means the more likely outcome occurred: probability above 0.5 predicts yes; below 0.5 predicts no. An exactly 0.5 forecast has no directional call and is excluded from hit rate but included in probability scoring. Binary Brier error is `(p - y)^2`, with y=1 for yes and y=0 for no; average it across resolved, eligible forecasts. Range 0–1, lower is better. This one-event convention is half the two-category sum in Brier's original formulation. Do not turn `1 - Brier` into an accuracy percentage. A constant 50% reference gives 0.25 for each binary event; it is a simple reference, not a sophisticated rival forecast. Use equal weights established in advance.

With no eligible outcomes, hit rate and Brier error are null/not yet available, not zero. Show pending and unresolvable records with reasons rather than hiding them. Calibration asks whether stated probabilities match event frequencies over many predictions. Delay a calibration chart until confidence groups contain enough outcomes to make a useful comparison; display counts and uncertainty and do not claim calibration from a handful of cases. This is an editorial display judgment, not a scientific threshold.

Every issue should reopen due envelopes and include: the original wording; what happened and its source; where the reasoning held or failed; and the revised outlook as a new dated forecast. Identify premature forecasts that later came true, without changing their original missed-deadline verdict. Sources 126 and 127 explain the scoring background, not the probabilities assigned here.
