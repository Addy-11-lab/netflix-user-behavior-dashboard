# OTT Growth & Retention Lab — case-study outline

## 1. The problem

An OTT Growth PM needs to understand whether churn is broad-based or concentrated in a particular customer behavior or segment—and decide which retention bet to test next.

## 2. The user and decision

**Primary user:** Growth PM / retention lead.  
**Job to be done:** “When churn is elevated, help me identify the highest-priority segment to investigate and define a measurable experiment.”

## 3. Product goal and metric tree

**North-star outcome:** retained subscribers.  
**Leading indicators:** timely first watch, meaningful watch time, weekly sessions, content interactions.  
**Guardrails:** cancellation rate, playback quality, support contacts, subscription conversion.

## 4. Data reality

The supplied 50,000-user dataset is a clean behavioral snapshot with a churn label. It supports segmentation and churn-risk analysis. It does not contain event timestamps, signup date, acquisition channel, or experiment assignment; those absences are measurement gaps, not blanks to fill with assumptions.

## 5. Analysis narrative

Use the dashboard to show:

1. Overall churn and activation-proxy baseline.
2. Churn by recency, device, plan, country, genre, and engagement segment.
3. A clearly labeled behavioral activation proxy, not a recorded event funnel.
4. Tenure-based churn comparison, not D1/D7/D30 retention.

Insert only values you can reproduce from the finished app.

## 6. Product hypothesis

Users who do not find relevant content in their first session are less likely to build a viewing habit. A genre-led personalized onboarding flow may increase first meaningful watch and improve D7 retention.

## 7. Experiment design

- **Audience:** new users, initially prioritized by a defined high-risk segment once event data exists.
- **Control:** current generic onboarding/home page.
- **Treatment:** genre choice followed by personalized titles.
- **Primary metric:** first meaningful watch within 24 hours.
- **Secondary metric:** D7 retention.
- **Guardrails:** cancellation, playback failures, and support contacts.
- **Decision:** launch only if the pre-registered primary metric improves significantly and guardrails remain stable.

## 8. Instrumentation and next steps

Implement the event dictionary in `EVENT_TRACKING_PLAN.md`; then measure actual funnel conversion, D1/D7/D30 retention, channel quality, and experiment lift. Prioritize instrumentation before scaling a treatment.

## 9. What I learned

Strong product analytics is not just charting available data. It identifies uncertainty, makes the next decision explicit, and designs the measurement needed to reduce that uncertainty.
