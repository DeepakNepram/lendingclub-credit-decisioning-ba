# Process Maps — As-Is and To-Be

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).
>
> These Mermaid diagrams render natively on GitHub and serve as the blueprint for the BPMN
> swimlane versions in draw.io (`as-is-lending-process.png`, `to-be-decisioning-process.png`).
> The actor for each step is shown in **[brackets]**; in draw.io each actor becomes a swimlane.

## As-Is — current lending & servicing process

```mermaid
flowchart TD
    A([Borrower submits application]) --> B["Platform: capture application data"]
    B --> C["Credit Policy: screen vs policy"]
    C --> D{Meets credit policy?}
    D -->|No| E([Rejected — recorded in rejected file])
    D -->|Yes| F["Credit Policy: assign grade A–G & interest rate"]
    F --> G["Investors: list for funding"]
    G --> H{Funded in window?}
    H -->|No| I([Expired — not issued])
    H -->|Yes| J["Platform: issue loan"]
    J --> K["Servicing: collect repayments"]
    K --> L{Repaid in full?}
    L -->|Yes| M([Fully Paid])
    L -->|No| N["Servicing: delinquency & collections"]
    N --> O([Charged Off — recoveries attempted])

    G1>"Insight gap: no unified approval-rate view"] -.-> C
    G2>"Insight gap: charge-off concentrations invisible"] -.-> K
    G3>"Insight gap: KPI definitions undocumented & inconsistent"] -.-> F

    classDef gap fill:#fff3f3,stroke:#d33,color:#900,stroke-dasharray:4 3;
    class G1,G2,G3 gap;
```

**Swimlanes for draw.io (5 lanes):** Borrower · Platform · Credit Policy · Investors · Servicing.
Annotate the three insight gaps in red text where they occur (these are the gaps the project
closes, and the gap paragraph that goes into the BRD).

## To-Be — decisioning dashboard + risk-review loop

```mermaid
flowchart TD
    A([Borrower submits application]) --> B["Platform: capture application data"]
    B --> RULE{"Rule flags application?<br/>DTI &gt; 40 · grade E–G & 60mo"}
    RULE -->|Yes| Q["Ops: manual review queue"]
    RULE -->|No| D{Meets credit policy?}
    Q --> D
    D -->|No| E([Rejected])
    D -->|Yes| F["Credit Policy: assign grade & rate"]
    F --> G["Investors: list for funding"]
    G --> H{Funded in window?}
    H -->|No| I([Expired])
    H -->|Yes| J["Platform: issue loan"]
    J --> K["Servicing: collect repayments"]
    K --> L{Repaid in full?}
    L -->|Yes| M([Fully Paid])
    L -->|No| N["Servicing: delinquency & collections"]
    N --> O([Charged Off])

    subgraph DA ["Data & Analytics layer (new)"]
        P1["Monthly pipeline: prepare_data.py"] --> P2[("KPI store — governed definitions")]
        P2 --> P3[["Decisioning & Portfolio Dashboard"]]
    end

    E -. rejected data .-> P1
    K -. loan outcomes .-> P1
    P3 -. charge-off concentrations .-> TUNE["Threshold tuning<br/>(governed via change control)"]
    TUNE -. updates thresholds .-> RULE

    classDef new fill:#eef7ff,stroke:#268,color:#024;
    class DA,P1,P2,P3,TUNE new;
```

**What's new vs as-is (the three additions to make in draw.io):**
1. A **Data & Analytics lane**: monthly pipeline → governed KPI store → Decisioning & Portfolio
   Dashboard, fed by both issued-loan outcomes and rejected applications.
2. A **rule-flag gateway** before the policy decision that routes flagged applications
   (DTI > 40, or grade E–G on 60-month terms) into an **Ops manual-review queue**.
3. A **feedback loop**: the dashboard surfaces charge-off concentrations → threshold tuning →
   updated rules, all **governed via change control** (this is where CR-001 will enter later).
