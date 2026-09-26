# Skill Converter

Create a new independent Jev-enhanced copy by applying the approved minimal patch to the copied Skill.

Requirements:
- source Skill remains unchanged
- preserve the copied Skill's existing files and working implementation
- do not rewrite unaffected prompts, scripts, stages, or tools
- preserve all validated hard constraints
- centralize routing in an orchestrator
- separate LLM generation prompts from Jev judgment specifications
- code handles deterministic checks and loop control
- Jev handles bounded judgments only
- LLM handles open-ended planning/generation/repair
- every repair preserves unaffected passing behavior
- every completion claim passes a final gate
- no infinite retries
- no embedded secrets

Write only the additive node contracts, thin adapter, stage-local calls, reports, and any narrowly required fixes.
