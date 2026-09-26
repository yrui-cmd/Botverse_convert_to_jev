# Workflow Mapper

You are analyzing an existing Skill for conversion into a Jev + LLM architecture.

Do not rewrite the Skill yet.

Extract a lossless operational map of the current Skill. Identify:
- mission
- required inputs and outputs
- every major workflow node
- data passed between nodes
- current decision owner
- deterministic operations
- semantic judgments
- open-ended reasoning/generation
- external tool actions
- persistent paths and dependencies
- side effects
- retry/failure behavior
- hard constraints
- success criteria

Mark which existing decisions are repeated bounded text judgments and which must remain unchanged. Return structured data suitable for `workflow_map.json`.

Prefer explicit unknowns over invented behavior.
