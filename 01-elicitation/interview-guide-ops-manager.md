# Interview Guide — Operations Manager

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).

**Purpose:** Understand the current reporting workflow and its cost, where definitions conflict
across teams, and what manual-review volume the operation can realistically sustain.
**Format:** ~15 minutes, semi-structured. **Interviewer:** Deepak Nepram (BA).
**Persona:** Runs the team that produces ad-hoc data pulls and would staff any manual-review
queue; pain is constant re-pulls, reconciling conflicting numbers, and limited review capacity.

## Questions
1. **Walk me through what happens when leadership asks for a number.**
   *Listening for:* the as-is reporting process and its hand-offs — input for the BPMN map.
2. **How many ad-hoc data pulls do you handle per week, and what do they cost you?**
   *Listening for:* the size of the problem the dashboard removes (the adoption metric).
3. **Where do definitions conflict across teams today?**
   *Listening for:* the case for a single governed KPI dictionary (e.g. charge-off denominator,
   whether approval rate excludes expired listings).
4. **What volume of manual reviews is operationally sustainable for your team?**
   *Listening for:* the capacity ceiling that the review-flag thresholds must respect — the
   other half of the Credit-vs-Ops trade-off.
5. **Which filters would your team actually use day to day?**
   *Listening for:* the real self-serve filter set (year, grade, purpose, term, state).
6. **What's the worst reporting failure you've seen here, and what caused it?**
   *Listening for:* the validation/release discipline to require before the dashboard goes live.

## Close
Confirm the sustainable review volume and the filter set, note the definition conflicts to
resolve in the dictionary, and state the next step (estimate the review-queue size implied by
candidate thresholds). Thank the interviewee.
