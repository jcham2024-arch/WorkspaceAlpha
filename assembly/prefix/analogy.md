# Analogy Reasoning Prefix

You are reasoning by analogy: mapping a known solution from one domain
to a novel problem in another domain.

## Your Task

You are given:
1. A **source domain** — a domain with a known, proven solution
2. A **target domain** — the current problem domain
3. **Task**: Apply the source solution's structure to the target problem

## Method

1. **Abstract the source**: Strip domain-specific details from the source
   solution. What is the underlying structure? What are the key elements
   and relationships?

2. **Map elements**: For each element in the source solution, identify the
   corresponding element in the target domain. Be explicit about the mapping.

3. **Adapt**: Translate the source solution into the target domain's terms.
   Adapt for differences in constraints, constraints, and context.

4. **Validate**: Does the adapted solution actually work in the target
   domain? What assumptions transfer? What assumptions break?

## Output Format

```
## Analogy Mapping

**Source Domain**: <name>
**Target Domain**: <name>
**Core Principle**: <one-sentence abstraction of the shared structure>

| Source Element | Target Domain Equivalent | Adaptation Notes |
|---|---|---|
| ... | ... | ... |

**Why this works**: <why the structural mapping is valid>

**Where it may break down**: <assumptions that might not transfer>

## Proposed Solution

<concrete steps adapted to the target domain>

## Confidence
<High/Medium/Low> — <why>
```

## Examples

**Example 1**: Database indexing → Code documentation navigation

Source: B-tree index on a sorted database column.
Target: Finding the right function in a 5000-line source file.

| Source Element | Target Element | Adaptation |
|---|---|---|
| Sorted column | Alphabetically sorted function names | Binary search on function names |
| B-tree nodes | Directory structure / module boundaries | Hierarchical narrowing |
| Leaf nodes | Individual function definitions | Direct lookup at leaf level |

**Why this works**: Both are ordered lookups in a large ordered set.

**Where it breaks down**: Code isn't always alphabetically ordered; semantic similarity matters more than name similarity.

---

**Example 2**: Git branching → Experiment isolation in data science

Source: Git feature branches isolate experimental changes.
Target: Machine learning experiment tracking.

| Source Element | Target Element | Adaptation |
|---|---|---|---|
| Git branch | Experiment branch | Each experiment gets its own isolated environment |
| Merge conflict | Prediction conflict | When two experiments modify same feature |
| Git stash | Pause experiment | Save state, switch context, resume later |

## Output Format Reminder

End your response with the analogy mapping table, confidence level, and any limitations.
