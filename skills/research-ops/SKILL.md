# Research Ops

> Do not answer current questions from stale memory when fresh search is cheap.

## When to activate

Trigger on: research requests, comparisons, lookups, "find the latest on X," "what's the current state of Y," market analysis, competitive intelligence, trend tracking, or any question that depends on current public information.

## Non-negotiables

1. **Fresh over stale** — if the answer depends on current information, search first. Do not rely on training data for time-sensitive facts.
2. **Separate evidence types** — clearly label what is sourced fact, user-provided context, inference, and recommendation.
3. **Date everything** — time-sensitive claims must include the date of the source.
4. **Lightest path first** — don't launch a heavyweight research pass when a quick search answers the question.
5. **Flag recurring needs** — if a user asks the same type of question repeatedly, suggest setting up a monitoring workflow instead of manual lookups.

## Process

### 1. Normalize inputs
Take user-supplied material and sort into:
- **Known facts** — verified, can be used as-is
- **Claims needing verification** — check against current sources
- **Open questions** — need research

### 2. Classify the ask

| Type | Description | Approach |
|------|-------------|----------|
| Factual lookup | "What is X's revenue?" | Quick search, single source sufficient |
| Comparison | "How does X compare to Y?" | Multi-source, structured comparison table |
| Enrichment | "Tell me more about X" | Deep research, synthesize multiple sources |
| Trend/monitoring | "What's happening in X industry?" | Broad search, pattern extraction, signal identification |
| Targeting | "Find companies doing X" | Lead intelligence, filtered list with criteria |

### 3. Execute research

**Quick lookup**: Single search, verify, report.

**Deep research**: 
1. Search 3-5 sources minimum
2. Cross-reference key claims
3. Identify consensus and disagreements
4. Synthesize into structured findings

**Market research**:
1. Define scope (geography, segment, timeframe)
2. Identify key players, trends, data points
3. Build comparison framework
4. Rank findings by relevance and reliability

### 4. Structure output

```
## Findings
[Sourced facts with citations and dates]

## Context
[User-provided information used as background]

## Analysis
[Inference and pattern recognition — clearly labeled as interpretation]

## Recommendations
[Actionable suggestions — clearly labeled as opinion]

## Sources
[All sources with dates and URLs]

## Freshness note
[When this research was conducted and how quickly it may become stale]
```

### 5. Post-research

- Store findings in knowledge base if reusable
- Flag if this topic should become a recurring monitor
- Note any gaps that couldn't be filled

## Integration with knowledge base

After research, route findings to appropriate storage:
- Reusable facts → knowledge base / wiki pages
- Project-specific findings → project notes
- Recurring topics → suggest monitoring workflow

## Guardrails

- Never present inference as sourced fact
- Never omit source dates for time-sensitive claims
- Never run heavyweight research when a quick search suffices
- Never ignore existing local documentation before searching externally
- Always tell the user when you couldn't verify something
